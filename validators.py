# validators.py - Input validation for AlgoBuddy
"""
Validates all user inputs before they reach the AI.

This prevents:
- Empty or nonsense messages being sent to the API
- Invalid course or topic names
- Invalid difficulty levels
- Invalid hint levels
- Invalid persona names

All validators raise ValidationError with a helpful message.

NOTE: Valid courses/topics come from course_registry.py automatically.
Adding a new course there updates validation here with no extra work.
"""

from course_registry import get_all_course_ids, get_all_topic_ids_for_course
from prompts import PERSONAS

# ==============================================================================
# CUSTOM EXCEPTION
# ==============================================================================

class ValidationError(Exception):
    """Raised when user input fails validation"""
    pass

# ==============================================================================
# VALID VALUES
# ==============================================================================

VALID_DIFFICULTIES = ["easy", "medium", "hard"]
VALID_HINT_LEVELS  = [1, 2, 3]

# ==============================================================================
# VALIDATORS
# ==============================================================================

def validate_user_message(message):
    """
    Validate a student chat message.

    Returns: str — cleaned message
    Raises:  ValidationError
    """
    if not message:
        raise ValidationError("Message cannot be empty.")
    if not isinstance(message, str):
        raise ValidationError("Message must be text.")
    message = message.strip()
    if len(message) == 0:
        raise ValidationError("Message cannot be blank.")
    if len(message) > 2000:
        raise ValidationError("Message is too long (max 2000 characters).")
    return message


def validate_course(course_id):
    """
    Validate a course ID against the course registry.

    Returns: str — cleaned course ID (lowercase)
    Raises:  ValidationError
    """
    if not course_id:
        raise ValidationError("Course cannot be empty.")
    course_id = course_id.strip().lower()
    valid = get_all_course_ids()
    if course_id not in valid:
        raise ValidationError(
            f"'{course_id}' is not a valid course.\n"
            f"Available courses: {', '.join(sorted(valid))}"
        )
    return course_id


def validate_topic(topic_id, course_id=None):
    """
    Validate a topic ID.

    If course_id is provided, checks the topic belongs to that course.
    If no course_id, checks topic exists in any course.

    Returns: str — cleaned topic ID (lowercase)
    Raises:  ValidationError
    """
    if not topic_id:
        raise ValidationError("Topic cannot be empty.")
    topic_id = topic_id.strip().lower()

    if course_id:
        course_id = course_id.strip().lower()
        valid_topics = get_all_topic_ids_for_course(course_id)
        if not valid_topics:
            raise ValidationError(f"Course '{course_id}' not found.")
        if topic_id not in valid_topics:
            raise ValidationError(
                f"'{topic_id}' is not a valid topic in {course_id}.\n"
                f"Available: {', '.join(sorted(valid_topics))}"
            )
    else:
        # Check across all courses
        all_valid = []
        for cid in get_all_course_ids():
            all_valid.extend(get_all_topic_ids_for_course(cid))
        if topic_id not in all_valid:
            raise ValidationError(f"'{topic_id}' is not a recognised topic.")

    return topic_id


def validate_difficulty(difficulty):
    """
    Validate difficulty level.

    Returns: str — lowercase difficulty
    Raises:  ValidationError
    """
    if not difficulty:
        raise ValidationError("Difficulty cannot be empty.")
    difficulty = difficulty.strip().lower()
    if difficulty not in VALID_DIFFICULTIES:
        raise ValidationError(
            f"'{difficulty}' is not valid. Choose from: easy, medium, hard"
        )
    return difficulty


def validate_hint_level(hint_level):
    """
    Validate hint level (1, 2, or 3).

    Returns: int
    Raises:  ValidationError
    """
    try:
        hint_level = int(hint_level)
    except (TypeError, ValueError):
        raise ValidationError("Hint level must be a number.")
    if hint_level not in VALID_HINT_LEVELS:
        raise ValidationError(f"Hint level must be 1, 2, or 3. Got: {hint_level}")
    return hint_level


def validate_persona(persona):
    """
    Validate a persona name against the PERSONAS dict in prompts.py.

    Returns: str — persona key
    Raises:  ValidationError
    """
    if not persona:
        return "default"
    persona = persona.strip().lower()
    if persona not in PERSONAS:
        valid_list = ", ".join(sorted(PERSONAS.keys()))
        raise ValidationError(
            f"'{persona}' is not a valid persona.\n"
            f"Available: {valid_list}"
        )
    return persona


def validate_student_name(name):
    """
    Validate a student display name.

    Returns: str — cleaned name
    Raises:  ValidationError
    """
    if not name:
        raise ValidationError("Name cannot be empty.")
    name = name.strip()
    if len(name) < 2:
        raise ValidationError("Name must be at least 2 characters.")
    if len(name) > 50:
        raise ValidationError("Name must be 50 characters or fewer.")
    return name


# ==============================================================================
# TESTING
# ==============================================================================

if __name__ == "__main__":

    print("Testing validators.py\n")

    # validate_user_message
    print("✅ Message:", validate_user_message("How do loops work?"))
    try:
        validate_user_message("")
    except ValidationError as e:
        print(f"✅ Empty message caught: {e}")

    # validate_course
    print("\n✅ Course:", validate_course("python"))
    print("✅ Course:", validate_course("HCI"))  # case insensitive
    try:
        validate_course("magic_school")
    except ValidationError as e:
        print(f"✅ Invalid course caught")

    # validate_topic with course
    print("\n✅ Topic:", validate_topic("loops", "python"))
    print("✅ Topic:", validate_topic("usability", "hci"))
    try:
        validate_topic("usability", "python")  # wrong course
    except ValidationError as e:
        print(f"✅ Wrong course/topic combo caught")

    # validate_difficulty
    print("\n✅ Difficulty:", validate_difficulty("HARD"))
    try:
        validate_difficulty("extreme")
    except ValidationError as e:
        print(f"✅ Invalid difficulty caught: {e}")

    # validate_hint_level
    print("\n✅ Hint level:", validate_hint_level("2"))
    try:
        validate_hint_level(5)
    except ValidationError as e:
        print(f"✅ Invalid hint level caught: {e}")

    # validate_persona
    print("\n✅ Persona:", validate_persona("batman"))
    print("✅ Persona (empty → default):", validate_persona(""))
    try:
        validate_persona("spiderman")
    except ValidationError as e:
        print(f"✅ Invalid persona caught")

    # validate_student_name
    print("\n✅ Name:", validate_student_name("Obianuju"))
    try:
        validate_student_name("A")
    except ValidationError as e:
        print(f"✅ Short name caught: {e}")

    # Summary of what's now valid
    print(f"\n📚 Valid courses: {get_all_course_ids()}")
    print(f"🎭 Valid personas: {list(PERSONAS.keys())}")
    print(f"⚡ Valid difficulties: {VALID_DIFFICULTIES}")
    print(f"💡 Valid hint levels: {VALID_HINT_LEVELS}")
    print("\n✅ All validator tests passed!")