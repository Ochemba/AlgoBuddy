from openai import OpenAI
import os, json
from dotenv import load_dotenv
from prompts import (
    get_system_prompt, SCAFFOLDING_PROMPT,
    get_problem_generation_prompt, HINT_LEVEL_PROMPTS,
    ANSWER_CHECK_PROMPT, ASSIGNMENT_HELP_SYSTEM, ASSIGNMENT_BREAKDOWN_PROMPT,
)
from progress_tracker import ProgressTracker
from validators import validate_topic, validate_difficulty, validate_user_message, validate_hint_level, validate_course, validate_persona, ValidationError
from logger import log_info, log_error, log_warning, log_api_call, log_student_action
import time

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conversation_history = []
api_call_count = 0
total_tokens_used = 0
estimated_cost = 0.0
current_tracker = ProgressTracker("Student")

def track_api_call(response):
    global api_call_count, total_tokens_used, estimated_cost
    api_call_count += 1
    tokens = response.usage.total_tokens
    total_tokens_used += tokens
    cost = tokens * 0.000002
    estimated_cost += cost
    import inspect
    log_api_call(inspect.stack()[1].function, tokens, cost)
    return tokens, cost

def get_cost_stats():
    return {"api_calls": api_call_count, "total_tokens": total_tokens_used,
            "estimated_cost": f"${estimated_cost:.4f}",
            "average_tokens_per_call": total_tokens_used // max(1, api_call_count)}

def optimize_conversation_history():
    global conversation_history
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]
        return True
    return False

# ── MAIN CHAT ─────────────────────────────────────────────────────────────────
def get_tutor_response(message=None, use_scaffolding=False,
                       student_name="Student", course_id=None,
                       topic_id=None, persona="default", assignment_mode = False, user_message=None,
                       file_context: str = None, image_data: dict = None):
    user_message = message or user_message or ""
    log_student_action("Asked Question", f"Length: {len(user_message)}")
    try:
        user_message = validate_user_message(user_message)
    except ValidationError as e:
        return f"❌ Invalid input: {e}"

    system_prompt = get_system_prompt(student_name=student_name, course_id=course_id,
                                      topic_id=topic_id, persona=persona,assignment_mode=assignment_mode)
    if use_scaffolding:
        system_prompt += "\n\n" + SCAFFOLDING_PROMPT

    if file_context and file_context.strip():
        from file_processor import truncate_context
        system_prompt += (
            "\n\n─── UPLOADED DOCUMENTS ───\n"
            "The student has uploaded one or more documents. These may contain questions to answer, "
            "notes to study from, or assignment material. Read ALL documents carefully. "
            "When the student asks about a specific document by name, refer to that document's content. "
            "When asked to answer questions, find and answer them from the relevant document.\n\n"
            + truncate_context(file_context, max_chars=12000)
            + "\n─── END OF UPLOADED DOCUMENTS ───"
        )

    conversation_history.append({"role": "user", "content": user_message})
    trimmed = conversation_history[-20:]

    if image_data:
        user_content = [
            {"type": "text", "text": user_message or "What can you see in this image?"},
            {"type": "image_url", "image_url": {"url": f"data:{image_data['media_type']};base64,{image_data['base64']}"}}
        ]
        messages = [{"role": "system", "content": system_prompt}, *trimmed[:-1],
                    {"role": "user", "content": user_content}]
    else:
        messages = [{"role": "system", "content": system_prompt}, *trimmed]

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="gpt-4o" if image_data else "gpt-4o-mini",
                messages=messages, max_tokens=400, temperature=0.7
            )
            track_api_call(response)
            ai_message = response.choices[0].message.content
            conversation_history.append({"role": "assistant", "content": ai_message})
            return ai_message
        except Exception as e:
            err = str(e)
            log_error(f"Attempt {attempt+1} failed", e)
            if attempt == 2:
                if "api_key" in err.lower(): return "❌ Error: Invalid API key."
                elif "connection" in err.lower(): return "❌ Error: Cannot connect to OpenAI."
                elif "rate_limit" in err.lower(): return "❌ Error: Rate limit hit."
                else: return f"❌ Error: {err}"
            time.sleep(2)
    return "❌ Error: Could not get response."

def clear_conversation():
    global conversation_history
    conversation_history = []

def set_conversation_history(messages: list):
    global conversation_history
    conversation_history = [
        {"role": m["role"], "content": m["content"]}
        for m in messages if m.get("role") in ("user", "assistant")
    ]

def get_conversation_length(): return len(conversation_history)

def trim_conversation(keep_last_n=10):
    global conversation_history
    if len(conversation_history) > keep_last_n:
        conversation_history = conversation_history[-keep_last_n:]
        return True
    return False


# ── PRACTICE PROBLEM GENERATION ───────────────────────────────────────────────

# Topics that suit fill-in-the-blank (coding/syntax focused)
FILL_BLANK_TOPICS = {
    "loops", "functions", "conditionals", "strings", "lists", "dictionaries",
    "classes", "recursion", "sorting", "arrays", "pointers", "syntax",
    "methods", "inheritance", "exceptions", "file_handling", "error_handling",
    "data_types", "operators", "variables", "python", "java", "csharp",
}

def _pick_question_type(topic_id: str, course_id: str, seed_context: str) -> str:
    """
    Rotate question types roughly 1/3 each: MCQ → FILL_BLANK → STANDARD.
    Fill-blank only for coding/syntax topics; otherwise swap to STANDARD.
    Uses a simple counter stored in a module-level list so it persists per session.
    """
    _pick_question_type.counter = getattr(_pick_question_type, "counter", 0)
    slot = _pick_question_type.counter % 3
    _pick_question_type.counter += 1

    if slot == 0:
        return "MCQ"
    elif slot == 1:
        # Fill-blank only if topic is coding/syntax
        key = (topic_id or course_id or "").lower().replace("-", "_")
        is_coding = any(t in key for t in FILL_BLANK_TOPICS)
        return "FILL_BLANK" if is_coding else "STANDARD"
    else:
        return "STANDARD"


def generate_practice_problem(topic, difficulty="medium", course_id=None, topic_id=None,
                               seed_context=None, file_context=None):
    log_student_action("Generate Problem", f"Topic:{topic} Difficulty:{difficulty}")
    try:
        difficulty = validate_difficulty(difficulty)
    except ValidationError as e:
        return {"error": str(e), "problem": str(e), "answer": "", "hints": []}

    prompt_topic = topic_id if topic_id else topic
    q_type = _pick_question_type(topic_id, course_id, seed_context)

    # ── Build prompt ──────────────────────────────────────────────────────────
    if file_context:
        from file_processor import truncate_context
        trimmed = truncate_context(file_context, max_chars=3000)

        if q_type == "MCQ":
            type_instructions = """Generate a MULTIPLE CHOICE question.
FORMAT:
TYPE: MCQ
PROBLEM: [the question]
OPTION_A: [option A]
OPTION_B: [option B]
OPTION_C: [option C]
OPTION_D: [option D]
CORRECT_OPTION: [A, B, C, or D]
EXPLANATION: [why that option is correct]
HINT1: [gentle nudge]
HINT2: [more specific]
HINT3: [strong hint — nearly gives it away]"""

        elif q_type == "FILL_BLANK":
            type_instructions = """Generate a FILL-IN-THE-BLANK question using a code snippet or syntax example.
Replace 1–3 key words/tokens with ___.
FORMAT:
TYPE: FILL_BLANK
PROBLEM: [code or sentence with ___ blanks]
BLANKS: [comma-separated answers for each blank in order]
EXPLANATION: [why these are correct]
HINT1: [gentle nudge]
HINT2: [more specific]
HINT3: [strong hint]"""

        else:
            type_instructions = """Generate a STANDARD coding or written question.
FORMAT:
TYPE: STANDARD
PROBLEM: [clear question]
EXAMPLE: [example if helpful, else omit]
ANSWER: [correct answer]
EXPLANATION: [explanation]
HINT1: [gentle nudge]
HINT2: [more specific]
HINT3: [strong hint]"""

        prompt = f"""Generate ONE {difficulty} difficulty practice problem based ONLY on the uploaded notes below.
Do NOT use general course knowledge — use only what is in the notes.

UPLOADED NOTES:
{trimmed}

DIFFICULTY: {difficulty}

{type_instructions}

Return ONLY the formatted response. No extra commentary."""

    else:
        base = get_problem_generation_prompt(prompt_topic, difficulty,
                                             course_id=course_id, topic_id=topic_id)

        if q_type == "MCQ":
            type_instructions = """Generate a MULTIPLE CHOICE question.
Prepend your response with:
TYPE: MCQ
PROBLEM: [the question]
OPTION_A: [option]
OPTION_B: [option]
OPTION_C: [option]
OPTION_D: [option]
CORRECT_OPTION: [A, B, C, or D]
EXPLANATION: [why correct]
HINT1: [gentle nudge]
HINT2: [more specific]
HINT3: [strong hint — nearly gives it away]
Keep all other fields (ANSWER) blank or omit them."""

        elif q_type == "FILL_BLANK":
            type_instructions = """Generate a FILL-IN-THE-BLANK question using a code snippet or syntax statement.
Replace 1–3 key tokens/keywords with ___.
Prepend your response with:
TYPE: FILL_BLANK
PROBLEM: [code or sentence with ___ blanks]
BLANKS: [comma-separated correct answers in order]
EXPLANATION: [why correct]
HINT1: [gentle nudge]
HINT2: [more specific]
HINT3: [strong hint]"""

        else:
            type_instructions = """Generate a STANDARD written or coding question.
Prepend your response with:
TYPE: STANDARD"""

        prompt = base + f"\n\n{type_instructions}"

        if seed_context:
            prompt += f"\n\nExtra context — student just learned:\n{seed_context[:400]}\nFocus the problem on these concepts."

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are creating practice problems for CS students. Follow the format exactly."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=700, temperature=0.8
            )
            track_api_call(response)
            content = response.choices[0].message.content
            data = parse_problem_response(content)
            data["topic"] = topic
            data["difficulty"] = difficulty
            return data
        except Exception as e:
            log_error(f"Problem gen attempt {attempt+1} failed", e)
            if attempt == 2:
                return {"error": str(e), "problem": "Error generating problem.", "answer": "", "hints": []}
            time.sleep(2)
    return {"error": "Max retries", "problem": "Could not generate problem.", "answer": "", "hints": []}


def parse_problem_response(text):
    data = {
        "type": "STANDARD",
        "problem": "", "example": "", "answer": "", "explanation": "",
        "hints": [], "blanks": [],
        # MCQ fields
        "options": {}, "correct_option": "",
    }
    lines = text.split('\n')
    current = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        upper = line.upper()
        if line.startswith("TYPE:"):
            val = line.replace("TYPE:", "").strip().upper()
            if "MCQ" in val:
                data["type"] = "MCQ"
            elif "FILL" in val:
                data["type"] = "FILL_BLANK"
            else:
                data["type"] = "STANDARD"
        elif line.startswith("PROBLEM:"):
            current = "problem"; data["problem"] = line.replace("PROBLEM:", "").strip()
        elif line.startswith("BLANKS:"):
            data["blanks"] = [b.strip() for b in line.replace("BLANKS:", "").split(",")]
            current = None
        elif line.startswith("OPTION_A:"):
            data["options"]["A"] = line.replace("OPTION_A:", "").strip(); current = None
        elif line.startswith("OPTION_B:"):
            data["options"]["B"] = line.replace("OPTION_B:", "").strip(); current = None
        elif line.startswith("OPTION_C:"):
            data["options"]["C"] = line.replace("OPTION_C:", "").strip(); current = None
        elif line.startswith("OPTION_D:"):
            data["options"]["D"] = line.replace("OPTION_D:", "").strip(); current = None
        elif line.startswith("CORRECT_OPTION:"):
            data["correct_option"] = line.replace("CORRECT_OPTION:", "").strip().upper()[:1]
            current = None
        elif line.startswith("EXAMPLE:"):
            current = "example"; data["example"] = line.replace("EXAMPLE:", "").strip()
        elif line.startswith("ANSWER:"):
            current = "answer"; data["answer"] = line.replace("ANSWER:", "").strip()
        elif line.startswith("EXPLANATION:"):
            current = "explanation"; data["explanation"] = line.replace("EXPLANATION:", "").strip()
        elif line.startswith("HINT"):
            hint_text = line.split(":", 1)[1].strip() if ":" in line else ""
            if hint_text:
                data["hints"].append(hint_text)
            current = None
        elif current and line:
            data[current] += " " + line

    return data


# ── ANSWER CHECKING ────────────────────────────────────────────────────────────

def _fuzzy_match(correct: str, student: str) -> bool:
    """
    Flexible match: ignore case/whitespace, allow minor typos via
    character-level similarity (Levenshtein-style ratio).
    """
    c = correct.strip().lower()
    s = student.strip().lower()

    # Exact after normalisation
    if c == s:
        return True

    # Substring containment (handles extra words around the answer)
    if c in s or s in c:
        return True

    # Simple character-overlap ratio for typo tolerance
    if len(c) == 0:
        return False
    longer = max(len(c), len(s))
    if longer == 0:
        return True
    matches = sum(ch in s for ch in c)
    ratio = matches / longer
    return ratio >= 0.80  # 80% character overlap threshold


def check_fill_blank_answer(blanks_correct: list, blanks_student: list) -> dict:
    """Check fill-in-the-blank answers with flexible matching."""
    if not blanks_correct:
        return {"is_correct": False, "feedback": "No answer key available.", "score": "0/0"}

    correct_count = 0
    feedback_parts = []

    for i, (correct, student) in enumerate(zip(blanks_correct, blanks_student)):
        if _fuzzy_match(correct, student):
            correct_count += 1
            feedback_parts.append(f"Blank {i+1}: ✅ Correct")
        else:
            feedback_parts.append(
                f"Blank {i+1}: ❌ You wrote '{student.strip()}' — correct answer is '{correct.strip()}'"
            )

    all_correct = correct_count == len(blanks_correct)
    return {
        "is_correct": all_correct,
        "score": f"{correct_count}/{len(blanks_correct)}",
        "feedback": " &nbsp;|&nbsp; ".join(feedback_parts),
    }


def check_mcq_answer(correct_option: str, student_option: str, explanation: str) -> dict:
    """Check a multiple choice answer instantly (no API call needed)."""
    is_correct = correct_option.strip().upper() == student_option.strip().upper()
    return {
        "is_correct": is_correct,
        "score": "1/1" if is_correct else "0/1",
        "feedback": explanation if explanation else (
            "Correct! Well done." if is_correct else f"Not quite — the correct answer was {correct_option}."
        ),
    }


def check_student_answer(problem, student_answer, correct_answer, course_id=None):
    course_type = "programming"
    if course_id:
        try:
            from course_registry import get_course_type
            course_type = get_course_type(course_id)
        except:
            pass
    prompt = ANSWER_CHECK_PROMPT.format(problem=problem, correct_answer=correct_answer,
                                        student_answer=student_answer, course_type=course_type)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a patient coding tutor checking student work."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300, temperature=0.3
        )
        track_api_call(response)
        return parse_answer_check(response.choices[0].message.content)
    except Exception as e:
        return {"is_correct": False, "feedback": f"Error: {e}", "misconception": "", "next_step": ""}


def parse_answer_check(text):
    result = {"is_correct": False, "feedback": "", "misconception": "", "next_step": ""}
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith("CORRECT:"):
            result["is_correct"] = "yes" in line.replace("CORRECT:", "").strip().lower()
        elif line.startswith("FEEDBACK:"):
            result["feedback"] = line.replace("FEEDBACK:", "").strip()
        elif line.startswith("MISCONCEPTION:"):
            result["misconception"] = line.replace("MISCONCEPTION:", "").strip()
        elif line.startswith("NEXT_STEP:"):
            result["next_step"] = line.replace("NEXT_STEP:", "").strip()
    return result


# ── FLASHCARD GENERATION ──────────────────────────────────────────────────────
def generate_flashcards(course_id=None, topic_id=None, count=8, file_context=None):
    """
    Generate spaced-repetition flashcards.
    Returns list of {"front": str, "back": str, "difficulty": str}
    """
    from prompts import get_flashcard_generation_prompt
    log_student_action("Generate Flashcards", f"Count:{count}")

    if file_context:
        from file_processor import truncate_context
        trimmed = truncate_context(file_context, max_chars=3000)
        prompt = f"""Generate exactly {count} flashcards for spaced repetition study.

The student has uploaded their own notes. Generate cards ONLY from the content below.

UPLOADED NOTES:
{trimmed}

Rules:
- Front: a question or term (max 15 words)
- Back: the answer or definition (max 50 words)
- Mix difficulty: easy, medium, hard
- Focus on concepts the student is likely to be tested on

Return ONLY a valid JSON array — no markdown, no backticks:
[
  {{"front": "Question here", "back": "Answer here", "difficulty": "easy/medium/hard"}}
]"""
    else:
        prompt = get_flashcard_generation_prompt(course_id, topic_id, count=count)

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You generate flashcards. Return only valid JSON arrays."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500, temperature=0.6
            )
            track_api_call(response)
            content = response.choices[0].message.content.strip()
            content = content.replace("```json", "").replace("```", "").strip()
            cards = json.loads(content)
            if isinstance(cards, list):
                return cards
        except json.JSONDecodeError:
            log_error(f"Flashcard JSON parse failed attempt {attempt+1}", Exception("JSON"))
        except Exception as e:
            log_error(f"Flashcard gen attempt {attempt+1} failed", e)
            if attempt == 2:
                return []
            time.sleep(2)
    return []


# ── HINTS ──────────────────────────────────────────────────────────────────────
def get_hint(problem, hint_level=1, pre_generated_hints=None):
    log_student_action("Request Hint", f"Level:{hint_level}")
    try:
        hint_level = validate_hint_level(hint_level)
    except ValidationError as e:
        return f"❌ Error: {e}"
    if pre_generated_hints and hint_level <= len(pre_generated_hints):
        return pre_generated_hints[hint_level - 1]
    prompt = f"Problem: {problem}\n\n{HINT_LEVEL_PROMPTS.get(hint_level, HINT_LEVEL_PROMPTS[1])}"
    for attempt in range(2):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are giving hints to help a student."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150, temperature=0.7
            )
            track_api_call(response)
            return response.choices[0].message.content
        except Exception as e:
            if attempt == 1:
                return f"❌ Error: {e}"
            time.sleep(1)
    return "❌ Could not generate hint."


# ── ASSIGNMENT HELPER ──────────────────────────────────────────────────────────
from assignment_helper import AssignmentHelper
assignment_helper = AssignmentHelper("Student")

def start_assignment_help(assignment_text):
    log_student_action("Start Assignment Help", f"Length:{len(assignment_text)}")
    breakdown = assignment_helper.analyze_assignment(assignment_text)
    if not breakdown:
        return {"error": "Could not analyze assignment"}
    initial = assignment_helper.get_guidance("I'm ready to start!")
    return {"breakdown": breakdown, "initial_guidance": initial,
            "total_steps": len(breakdown["steps"]), "difficulty": breakdown["difficulty_estimate"]}

def continue_assignment_help(student_message):
    guidance = assignment_helper.get_guidance(student_message)
    return {"guidance": guidance, "current_step": assignment_helper.current_step + 1,
            "steps_completed": len(assignment_helper.steps_completed),
            "is_complete": assignment_helper.is_assignment_complete()}

def reset_assignment_helper():
    assignment_helper.reset()


# ── PROGRESS ───────────────────────────────────────────────────────────────────
def start_study_session(): return current_tracker.start_session()
def end_study_session(): return current_tracker.end_session()
def get_progress_report(): return current_tracker.get_stats_summary()
def save_progress(): current_tracker.save_to_file("progress.json")
def load_progress(): return current_tracker.load_from_file("progress.json")
def get_session_summary(): return current_tracker.format_session_summary()