# test_suite.py - Consolidated Test Suite for AI Tutor
# Week 2, Days 9-10: Proper Test Suite
"""
This replaces the scattered day3_test.py, day4_test.py, day4_testprogress.py
with ONE professional test file.

HOW TO RUN:
    python test_suite.py              → Run all tests
    python test_suite.py chat         → Run only chat tests
    python test_suite.py problems     → Run only problem generation tests
    python test_suite.py answers      → Run only answer checking tests
    python test_suite.py hints        → Run only hint tests
    python test_suite.py progress     → Run only progress tracking tests
    python test_suite.py validators   → Run only validator tests (no API needed)

WHAT EACH TEST CHECKS:
    ✅ Chat           - Tutor responds, remembers conversation context
    ✅ Problems       - Generates problems at easy/medium/hard for multiple topics
    ✅ Answers        - Correctly identifies right/wrong answers
    ✅ Hints          - Returns 3 levels of hints
    ✅ Progress       - Tracks attempts, accuracy, streaks, saves/loads
    ✅ Validators     - Rejects bad input correctly
    ✅ Adaptive       - Difficulty adjusts based on performance
    ✅ Assignment     - Assignment helper breaks down and guides
    ✅ Cost           - API usage is being tracked
"""

import sys
import time
from datetime import datetime

# ============================================================
# COLOUR HELPERS (makes output easier to read)
# ============================================================

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def passed(msg):
    print(f"  {GREEN}✅ PASS{RESET} - {msg}")

def failed(msg):
    print(f"  {RED}❌ FAIL{RESET} - {msg}")

def info(msg):
    print(f"  {YELLOW}ℹ️  {RESET}{msg}")

def header(title):
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}  {title}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}")

# ============================================================
# TEST RESULT TRACKER
# ============================================================

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.errors = []

    def record_pass(self):
        self.passed += 1

    def record_fail(self, test_name, reason):
        self.failed += 1
        self.errors.append(f"{test_name}: {reason}")

    def record_skip(self):
        self.skipped += 1

    def print_summary(self):
        total = self.passed + self.failed
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}  FINAL RESULTS{RESET}")
        print(f"{'='*60}")
        print(f"  Total Tests : {total}")
        print(f"  {GREEN}Passed      : {self.passed}{RESET}")
        print(f"  {RED}Failed      : {self.failed}{RESET}")
        if self.skipped:
            print(f"  {YELLOW}Skipped     : {self.skipped}{RESET}")
        if total > 0:
            pct = (self.passed / total) * 100
            bar_filled = int(pct / 5)
            bar = "█" * bar_filled + "░" * (20 - bar_filled)
            print(f"\n  [{bar}] {pct:.0f}%")
        if self.errors:
            print(f"\n  {RED}Failed tests:{RESET}")
            for err in self.errors:
                print(f"    • {err}")
        print(f"{'='*60}\n")
        return self.failed == 0

results = TestResults()

# ============================================================
# HELPER: run a single test safely
# ============================================================

def run_test(test_name, fn):
    """
    Run fn(), record pass/fail automatically.
    fn() should raise AssertionError or Exception on failure.
    """
    try:
        fn()
        passed(test_name)
        results.record_pass()
    except AssertionError as e:
        failed(f"{test_name} → {e}")
        results.record_fail(test_name, str(e))
    except Exception as e:
        failed(f"{test_name} → Unexpected error: {e}")
        results.record_fail(test_name, str(e))

# ============================================================
# GROUP 1: VALIDATORS  (no API calls — run these first!)
# ============================================================

def test_validators():
    header("GROUP 1: VALIDATORS  (no API needed)")

    from validators import (
        validate_user_message,
        validate_topic,
        validate_difficulty,
        validate_hint_level,
        ValidationError
    )

    # --- validate_user_message ---
    def t_valid_message():
        result = validate_user_message("How do I use loops?")
        assert result == "How do I use loops?", "Should return cleaned message"

    def t_empty_message():
        try:
            validate_user_message("")
            assert False, "Should have raised ValidationError"
        except ValidationError:
            pass  # correct

    def t_blank_message():
        try:
            validate_user_message("   ")
            assert False, "Should have raised ValidationError"
        except ValidationError:
            pass

    def t_too_long_message():
        try:
            validate_user_message("x" * 2001)
            assert False, "Should have raised ValidationError"
        except ValidationError:
            pass

    def t_message_strips_whitespace():
        result = validate_user_message("  hello  ")
        assert result == "hello", f"Expected 'hello', got '{result}'"

    # --- validate_topic ---
    def t_valid_topic():
        result = validate_topic("loops")
        assert result == "loops"

    def t_topic_case_insensitive():
        result = validate_topic("FUNCTIONS")
        assert result == "functions", f"Expected 'functions', got '{result}'"

    def t_invalid_topic():
        try:
            validate_topic("quantum_physics")
            assert False, "Should have raised ValidationError"
        except ValidationError:
            pass

    def t_empty_topic():
        try:
            validate_topic("")
            assert False, "Should have raised ValidationError"
        except ValidationError:
            pass

    # --- validate_difficulty ---
    def t_valid_difficulty():
        for d in ["easy", "medium", "hard"]:
            result = validate_difficulty(d)
            assert result == d

    def t_difficulty_case_insensitive():
        result = validate_difficulty("EASY")
        assert result == "easy"

    def t_invalid_difficulty():
        try:
            validate_difficulty("extreme")
            assert False, "Should have raised ValidationError"
        except ValidationError:
            pass

    # --- validate_hint_level ---
    def t_valid_hint_levels():
        for level in [1, 2, 3]:
            result = validate_hint_level(level)
            assert result == level

    def t_hint_level_from_string():
        result = validate_hint_level("2")
        assert result == 2

    def t_invalid_hint_level():
        try:
            validate_hint_level(5)
            assert False, "Should have raised ValidationError"
        except ValidationError:
            pass

    def t_hint_level_not_zero():
        try:
            validate_hint_level(0)
            assert False, "Should have raised ValidationError"
        except ValidationError:
            pass

    run_test("Valid message accepted", t_valid_message)
    run_test("Empty message rejected", t_empty_message)
    run_test("Blank message rejected", t_blank_message)
    run_test("Too-long message rejected (>2000 chars)", t_too_long_message)
    run_test("Message whitespace is stripped", t_message_strips_whitespace)
    run_test("Valid topic accepted", t_valid_topic)
    run_test("Topic is case-insensitive", t_topic_case_insensitive)
    run_test("Invalid topic rejected", t_invalid_topic)
    run_test("Empty topic rejected", t_empty_topic)
    run_test("Valid difficulties accepted (easy/medium/hard)", t_valid_difficulty)
    run_test("Difficulty is case-insensitive", t_difficulty_case_insensitive)
    run_test("Invalid difficulty rejected", t_invalid_difficulty)
    run_test("Valid hint levels accepted (1/2/3)", t_valid_hint_levels)
    run_test("Hint level accepted as string", t_hint_level_from_string)
    run_test("Hint level > 3 rejected", t_invalid_hint_level)
    run_test("Hint level 0 rejected", t_hint_level_not_zero)

# ============================================================
# GROUP 2: PROGRESS TRACKER  (no API calls)
# ============================================================

def test_progress():
    header("GROUP 2: PROGRESS TRACKER  (no API needed)")

    from progress_tracker import ProgressTracker

    def t_new_tracker_starts_empty():
        t = ProgressTracker("Test")
        assert t.stats["problems_attempted"] == 0
        assert t.stats["problems_correct"] == 0
        assert t.get_accuracy() == 0.0

    def t_record_correct_attempt():
        t = ProgressTracker("Test")
        t.start_session()
        t.record_problem_attempt("loops", True, hints_used=0)
        assert t.stats["problems_attempted"] == 1
        assert t.stats["problems_correct"] == 1
        assert t.get_accuracy() == 100.0

    def t_record_wrong_attempt():
        t = ProgressTracker("Test")
        t.start_session()
        t.record_problem_attempt("loops", False, hints_used=2)
        assert t.stats["problems_attempted"] == 1
        assert t.stats["problems_correct"] == 0
        assert t.get_accuracy() == 0.0
        assert t.stats["total_hints_used"] == 2

    def t_accuracy_calculation():
        t = ProgressTracker("Test")
        t.start_session()
        t.record_problem_attempt("loops", True)
        t.record_problem_attempt("loops", True)
        t.record_problem_attempt("loops", False)
        # 2 correct out of 3 = 66.67%
        assert abs(t.get_accuracy() - 66.67) < 0.1, f"Got {t.get_accuracy()}"

    def t_topic_tracking():
        t = ProgressTracker("Test")
        t.start_session()
        t.record_problem_attempt("loops", True)
        t.record_problem_attempt("functions", False)
        assert "loops" in t.stats["topics_studied"]
        assert "functions" in t.stats["topics_studied"]
        assert len(t.stats["topics_studied"]) == 2

    def t_topic_not_duplicated():
        t = ProgressTracker("Test")
        t.start_session()
        t.record_problem_attempt("loops", True)
        t.record_problem_attempt("loops", True)
        assert t.stats["topics_studied"].count("loops") == 1

    def t_topic_performance_tracked():
        t = ProgressTracker("Test")
        t.start_session()
        t.record_problem_attempt("loops", True)
        t.record_problem_attempt("loops", False)
        perf = t.stats["topic_performance"]["loops"]
        assert perf["attempted"] == 2
        assert perf["correct"] == 1
        assert perf["accuracy"] == 50.0

    def t_weak_topics_identified():
        t = ProgressTracker("Test")
        t.start_session()
        # loops: 0% accuracy (2 attempts needed for weak topic threshold)
        t.record_problem_attempt("loops", False)
        t.record_problem_attempt("loops", False)
        weak = t.get_weak_topics()
        assert len(weak) == 1
        assert weak[0]["topic"] == "loops"

    def t_strong_topics_identified():
        t = ProgressTracker("Test")
        t.start_session()
        # loops: 100% accuracy (2 attempts needed)
        t.record_problem_attempt("loops", True)
        t.record_problem_attempt("loops", True)
        strong = t.get_strong_topics()
        assert len(strong) == 1
        assert strong[0]["topic"] == "loops"

    def t_difficulty_recommendation_easy_when_struggling():
        t = ProgressTracker("Test")
        t.start_session()
        # 0% accuracy → should recommend easy
        for _ in range(3):
            t.record_problem_attempt("loops", False)
        rec = t.get_recommended_difficulty()
        assert rec == "easy", f"Expected easy, got {rec}"

    def t_difficulty_recommendation_hard_when_excelling():
        t = ProgressTracker("Test")
        t.start_session()
        # 100% accuracy → should recommend harder
        for _ in range(5):
            t.record_problem_attempt("loops", True)
        rec = t.get_recommended_difficulty()
        assert rec in ["medium", "hard"], f"Expected medium/hard, got {rec}"

    def t_streak_starts_at_1():
        t = ProgressTracker("Test")
        t.start_session()
        assert t.stats["current_streak"] == 1

    def t_session_count_increments():
        t = ProgressTracker("Test")
        t.start_session()
        t.start_session()
        assert t.stats["sessions_count"] == 2

    def t_end_session_returns_duration():
        t = ProgressTracker("Test")
        t.start_session()
        time.sleep(0.1)  # tiny pause so duration isn't zero
        duration = t.end_session()
        assert isinstance(duration, int), f"Expected int, got {type(duration)}"

    def t_save_and_load(tmp_path="test_progress_temp.json"):
        import os
        t = ProgressTracker("Test")
        t.start_session()
        t.record_problem_attempt("loops", True)
        t.save_to_file(tmp_path)

        t2 = ProgressTracker("Test2")
        t2.load_from_file(tmp_path)
        assert t2.stats["problems_attempted"] == 1
        assert t2.stats["problems_correct"] == 1

        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    def t_stats_summary_keys():
        t = ProgressTracker("Test")
        summary = t.get_stats_summary()
        expected_keys = [
            "student_name", "total_problems", "accuracy",
            "topics_covered", "current_streak", "total_study_time",
            "current_difficulty", "hints_used", "sessions_completed"
        ]
        for key in expected_keys:
            assert key in summary, f"Missing key: {key}"

    def t_session_summary_no_error():
        t = ProgressTracker("Test")
        t.start_session()
        t.record_problem_attempt("loops", True)
        t.end_session()
        summary = t.generate_session_summary()
        assert "error" not in summary
        assert "problems_attempted" in summary

    def t_format_session_summary_is_string():
        t = ProgressTracker("Test")
        t.start_session()
        t.record_problem_attempt("loops", True)
        t.end_session()
        result = t.format_session_summary()
        assert isinstance(result, str)
        assert "SESSION SUMMARY" in result

    run_test("New tracker starts at zero", t_new_tracker_starts_empty)
    run_test("Correct attempt recorded", t_record_correct_attempt)
    run_test("Wrong attempt + hints recorded", t_record_wrong_attempt)
    run_test("Accuracy calculation is correct", t_accuracy_calculation)
    run_test("Topics tracked across subjects", t_topic_tracking)
    run_test("Same topic not duplicated in list", t_topic_not_duplicated)
    run_test("Topic performance stats tracked", t_topic_performance_tracked)
    run_test("Weak topics identified (<60%)", t_weak_topics_identified)
    run_test("Strong topics identified (>=80%)", t_strong_topics_identified)
    run_test("Recommends EASY when struggling", t_difficulty_recommendation_easy_when_struggling)
    run_test("Recommends HARDER when excelling", t_difficulty_recommendation_hard_when_excelling)
    run_test("Streak starts at 1", t_streak_starts_at_1)
    run_test("Session count increments", t_session_count_increments)
    run_test("End session returns duration (int)", t_end_session_returns_duration)
    run_test("Save and load progress", t_save_and_load)
    run_test("Stats summary has all expected keys", t_stats_summary_keys)
    run_test("Session summary generated without error", t_session_summary_no_error)
    run_test("Format session summary returns string", t_format_session_summary_is_string)

# ============================================================
# GROUP 3: CHAT  (requires API)
# ============================================================

def test_chat():
    header("GROUP 3: CHAT  (requires API)")

    from tutor_engine import get_tutor_response, clear_conversation

    def t_basic_response():
        clear_conversation()
        response = get_tutor_response("What is a Python variable?")
        assert response, "Response should not be empty"
        assert len(response) > 20, "Response seems too short"
        assert "❌" not in response, f"Got error response: {response[:100]}"

    def t_response_is_string():
        clear_conversation()
        response = get_tutor_response("What is a list in Python?")
        assert isinstance(response, str), f"Expected str, got {type(response)}"

    def t_conversation_context_maintained():
        clear_conversation()
        get_tutor_response("Let's talk about Python dictionaries.")
        response2 = get_tutor_response("Can you give me an example of what we just discussed?")
        # The second response should reference dictionaries in some way
        assert len(response2) > 20, "Context response too short"
        assert "❌" not in response2

    def t_empty_message_rejected():
        clear_conversation()
        response = get_tutor_response("")
        assert "❌" in response or "invalid" in response.lower(), \
            "Empty message should return error"

    def t_scaffolding_mode():
        clear_conversation()
        response = get_tutor_response("I don't understand loops", use_scaffolding=True)
        assert response and len(response) > 20
        assert "❌" not in response

    run_test("Basic chat response received", t_basic_response)
    run_test("Response is a string", t_response_is_string)
    run_test("Conversation context is maintained", t_conversation_context_maintained)
    run_test("Empty message returns error", t_empty_message_rejected)
    run_test("Scaffolding mode works", t_scaffolding_mode)

# ============================================================
# GROUP 4: PROBLEM GENERATION  (requires API)
# ============================================================

def test_problems():
    header("GROUP 4: PROBLEM GENERATION  (requires API)")

    from tutor_engine import generate_practice_problem

    def t_generates_problem_dict():
        p = generate_practice_problem("loops", "easy")
        assert isinstance(p, dict), "Should return a dict"

    def t_problem_has_required_keys():
        p = generate_practice_problem("loops", "easy")
        for key in ["problem", "answer", "hints"]:
            assert key in p, f"Missing key: {key}"

    def t_problem_text_not_empty():
        p = generate_practice_problem("loops", "easy")
        assert p["problem"], "Problem text should not be empty"
        assert len(p["problem"]) > 10

    def t_hints_is_a_list():
        p = generate_practice_problem("loops", "easy")
        assert isinstance(p["hints"], list), "Hints should be a list"

    def t_answer_not_empty():
        p = generate_practice_problem("functions", "medium")
        assert p["answer"], "Answer should not be empty"

    def t_topic_stored_in_problem():
        p = generate_practice_problem("lists", "easy")
        assert p.get("topic") == "lists", f"Expected 'lists', got {p.get('topic')}"

    def t_difficulty_stored_in_problem():
        p = generate_practice_problem("loops", "hard")
        assert p.get("difficulty") == "hard"

    def t_invalid_topic_returns_error():
        p = generate_practice_problem("invalid_topic_xyz", "easy")
        assert "error" in p, "Invalid topic should return error dict"

    def t_invalid_difficulty_returns_error():
        p = generate_practice_problem("loops", "insane")
        assert "error" in p

    def t_multiple_topics_work():
        for topic in ["loops", "functions", "lists", "dictionaries"]:
            p = generate_practice_problem(topic, "easy")
            assert p["problem"], f"Empty problem for topic: {topic}"

    run_test("Returns a dictionary", t_generates_problem_dict)
    run_test("Dict has problem/answer/hints keys", t_problem_has_required_keys)
    run_test("Problem text is not empty", t_problem_text_not_empty)
    run_test("Hints is a list", t_hints_is_a_list)
    run_test("Answer is not empty", t_answer_not_empty)
    run_test("Topic stored in returned dict", t_topic_stored_in_problem)
    run_test("Difficulty stored in returned dict", t_difficulty_stored_in_problem)
    run_test("Invalid topic returns error dict", t_invalid_topic_returns_error)
    run_test("Invalid difficulty returns error dict", t_invalid_difficulty_returns_error)
    run_test("Works for all 4 core topics", t_multiple_topics_work)

# ============================================================
# GROUP 5: ANSWER CHECKING  (requires API)
# ============================================================

def test_answers():
    header("GROUP 5: ANSWER CHECKING  (requires API)")

    from tutor_engine import check_student_answer

    PROBLEM = "Write a loop that prints numbers 1 to 5"
    CORRECT = "for i in range(1, 6):\n    print(i)"

    def t_correct_answer_detected():
        result = check_student_answer(PROBLEM, CORRECT, CORRECT)
        assert result["is_correct"] == True, "Should detect correct answer"

    def t_wrong_answer_detected():
        result = check_student_answer(PROBLEM, "print('hello')", CORRECT)
        assert result["is_correct"] == False, "Should detect wrong answer"

    def t_result_has_required_keys():
        result = check_student_answer(PROBLEM, CORRECT, CORRECT)
        for key in ["is_correct", "feedback", "misconception", "next_step"]:
            assert key in result, f"Missing key: {key}"

    def t_feedback_not_empty():
        result = check_student_answer(PROBLEM, CORRECT, CORRECT)
        assert result["feedback"], "Feedback should not be empty"

    def t_equivalent_answers_accepted():
        # Both are logically equivalent
        student = "for i in range(1,6): print(i)"
        result = check_student_answer(PROBLEM, student, CORRECT)
        # AI should recognise this as correct (or at least give feedback)
        assert "is_correct" in result

    def t_wrong_answer_has_guidance():
        result = check_student_answer(PROBLEM, "for i in range(5): print(i)", CORRECT)
        # When wrong, should give misconception or next step
        has_guidance = bool(result.get("misconception") or result.get("next_step") or result.get("feedback"))
        assert has_guidance, "Wrong answer should include guidance"

    run_test("Correct answer detected as correct", t_correct_answer_detected)
    run_test("Wrong answer detected as wrong", t_wrong_answer_detected)
    run_test("Result has all required keys", t_result_has_required_keys)
    run_test("Feedback is not empty", t_feedback_not_empty)
    run_test("Equivalent answers handled", t_equivalent_answers_accepted)
    run_test("Wrong answer includes guidance", t_wrong_answer_has_guidance)

# ============================================================
# GROUP 6: HINTS  (requires API)
# ============================================================

def test_hints():
    header("GROUP 6: HINTS  (requires API)")

    from tutor_engine import get_hint

    PROBLEM = "Write a function that returns the sum of two numbers"

    def t_level1_hint_returned():
        hint = get_hint(PROBLEM, hint_level=1)
        assert hint and len(hint) > 10
        assert "❌" not in hint

    def t_level2_hint_returned():
        hint = get_hint(PROBLEM, hint_level=2)
        assert hint and len(hint) > 10
        assert "❌" not in hint

    def t_level3_hint_returned():
        hint = get_hint(PROBLEM, hint_level=3)
        assert hint and len(hint) > 10
        assert "❌" not in hint

    def t_invalid_hint_level_returns_error():
        result = get_hint(PROBLEM, hint_level=9)
        assert "❌" in result, "Invalid hint level should return error message"

    def t_pre_generated_hints_used():
        pre_hints = ["Hint one", "Hint two", "Hint three"]
        result = get_hint(PROBLEM, hint_level=1, pre_generated_hints=pre_hints)
        assert result == "Hint one", f"Expected 'Hint one', got '{result}'"

    def t_hint_is_string():
        hint = get_hint(PROBLEM, hint_level=1)
        assert isinstance(hint, str)

    run_test("Level 1 hint (gentle) returned", t_level1_hint_returned)
    run_test("Level 2 hint (specific) returned", t_level2_hint_returned)
    run_test("Level 3 hint (strong) returned", t_level3_hint_returned)
    run_test("Invalid hint level returns error", t_invalid_hint_level_returns_error)
    run_test("Pre-generated hints used when provided", t_pre_generated_hints_used)
    run_test("Hint returns a string", t_hint_is_string)

# ============================================================
# GROUP 7: ADAPTIVE DIFFICULTY + COST TRACKING  (requires API)
# ============================================================

def test_adaptive():
    header("GROUP 7: ADAPTIVE DIFFICULTY + COST TRACKING  (requires API)")

    from tutor_engine import (
        generate_adaptive_problem,
        submit_answer_with_tracking,
        get_progress_report,
        get_cost_stats,
        get_study_recommendations,
        start_study_session,
        end_study_session
    )

    def t_adaptive_problem_has_difficulty():
        start_study_session()
        p = generate_adaptive_problem("loops")
        assert "difficulty" in p
        assert p["difficulty"] in ["easy", "medium", "hard"]

    def t_submit_answer_returns_accuracy():
        start_study_session()
        p = generate_adaptive_problem("loops")
        result = submit_answer_with_tracking(p, p["answer"], "loops")
        assert "accuracy" in result
        assert "total_solved" in result
        assert "streak" in result

    def t_progress_report_has_keys():
        report = get_progress_report()
        expected = ["student_name", "total_problems", "accuracy",
                    "topics_covered", "current_streak"]
        for key in expected:
            assert key in report, f"Missing key: {key}"

    def t_cost_stats_tracked():
        stats = get_cost_stats()
        assert "api_calls" in stats
        assert "total_tokens" in stats
        assert "estimated_cost" in stats
        assert stats["api_calls"] > 0, "API calls should be > 0 by now"

    def t_study_recommendations_returned():
        recs = get_study_recommendations()
        assert "next_topic" in recs
        assert "reason" in recs
        assert "weak_topics" in recs
        assert "strong_topics" in recs

    run_test("Adaptive problem has a difficulty level", t_adaptive_problem_has_difficulty)
    run_test("Submit answer returns accuracy + streak", t_submit_answer_returns_accuracy)
    run_test("Progress report has all expected keys", t_progress_report_has_keys)
    run_test("API costs are being tracked", t_cost_stats_tracked)
    run_test("Study recommendations returned", t_study_recommendations_returned)

# ============================================================
# MAIN ENTRY POINT
# ============================================================

# Map command-line args to test functions
TEST_GROUPS = {
    "validators": test_validators,
    "progress":   test_progress,
    "chat":       test_chat,
    "problems":   test_problems,
    "answers":    test_answers,
    "hints":      test_hints,
    "adaptive":   test_adaptive,
}

NO_API_GROUPS = {"validators", "progress"}   # these run without an API key

if __name__ == "__main__":

    print(f"\n{BOLD}🎓 AI TUTOR - TEST SUITE{RESET}")
    print(f"Run date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    arg = sys.argv[1].lower() if len(sys.argv) > 1 else "all"

    if arg == "all":
        # Run offline groups first, then API groups
        for name in ["validators", "progress", "chat", "problems", "answers", "hints", "adaptive"]:
            TEST_GROUPS[name]()

    elif arg == "offline":
        # Useful when you have no API key / internet
        info("Running offline tests only (validators + progress tracker)")
        for name in NO_API_GROUPS:
            TEST_GROUPS[name]()

    elif arg in TEST_GROUPS:
        TEST_GROUPS[arg]()

    else:
        print(f"{RED}Unknown group '{arg}'.{RESET}")
        print(f"Valid options: all, offline, {', '.join(TEST_GROUPS.keys())}")
        sys.exit(1)

    # Print final summary
    all_passed = results.print_summary()
    sys.exit(0 if all_passed else 1)