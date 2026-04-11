# course_registry.py - Master Course Registry
"""
The single source of truth for ALL courses in the AI Tutor.

Every other file (validators, prompts, Streamlit UI) imports from here.

TO ADD A NEW COURSE IN FUTURE:
  1. Create courses/yourcourse.py  (copy any existing one as template)
  2. Import it below and add to COURSES dict
  3. That's it — the rest of the app updates automatically

COURSE TYPES:
  "programming"  → code-focused problems and explanations
  "theory"       → discussion, definitions, exam-style questions
  "mixed"        → combination of both
"""

# Import all course definitions
from courses.python    import COURSE as PYTHON
from courses.java      import COURSE as JAVA
from courses.Csharp    import COURSE as CSHARP
from courses.Dsa       import COURSE as DSA
from courses.Hci       import COURSE as HCI
from courses.Databases import COURSE as DATABASES
from courses.data_engineering import COURSE as DATA_ENGINEERING
from courses.data_science import COURSE as DATA_SCIENCE
from courses.machine_learning import COURSE as MACHINE_LEARNING
from courses.web_dev import COURSE as WEB_DEV

# Master registry — add new courses here
COURSES = {
    "python":    PYTHON,
    "java":      JAVA,
    "csharp":    CSHARP,
    "dsa":       DSA,
    "hci":       HCI,
    "databases": DATABASES,
    "data_engineering": DATA_ENGINEERING,
    "data_science": DATA_SCIENCE,
    "machine_learning": MACHINE_LEARNING,
    "web_dev": WEB_DEV

}

# ==============================================================================
# HELPER FUNCTIONS  (used by validators, prompts, and the UI)
# ==============================================================================

def get_all_course_ids():
    """Return list of all valid course IDs"""
    return list(COURSES.keys())


def get_course(course_id):
    """
    Get full course definition

    Returns:
        dict: Course info, or None if not found
    """
    return COURSES.get(course_id.lower())


def get_course_display_name(course_id):
    """Get the human-readable course name"""
    course = get_course(course_id)
    return course["display_name"] if course else course_id


def get_all_topics_for_course(course_id):
    """Return dict of all topics in a course"""
    course = get_course(course_id)
    return course["topics"] if course else {}


def get_all_topic_ids_for_course(course_id):
    """Return list of topic ID strings for a course"""
    return list(get_all_topics_for_course(course_id).keys())


def get_topic(course_id, topic_id):
    """Get a specific topic from a specific course"""
    topics = get_all_topics_for_course(course_id)
    return topics.get(topic_id)


def get_topic_prompt_context(course_id, topic_id):
    """
    Build a rich context string for the AI problem-generation prompt.
    Gives the AI specific guidance on what to test.

    Returns:
        str: Context block to inject into prompts
    """
    course = get_course(course_id)
    topic  = get_topic(course_id, topic_id)

    if not course or not topic:
        return f"Course: {course_id}, Topic: {topic_id}"

    concepts_str = ", ".join(topic["key_concepts"][:6])

    return f"""Course: {course['display_name']}
Topic: {topic['display_name']}
Description: {topic['description']}
Key concepts to test: {concepts_str}
Teaching note: {topic['teaching_notes']}
Course type: {course['type']} ({"write code solutions" if course['type'] == 'programming' else "mix of theory explanations and practical exercises" if course['type'] == 'mixed' else "theory explanations and exam-style questions"})"""


def get_recommended_next_topics(course_id, topics_studied):
    """
    Given topics a student has studied in a course,
    return what they're now ready to study next.

    Args:
        course_id (str): The course
        topics_studied (list): Topic IDs already covered

    Returns:
        list of dicts: [{topic_id, display_name, tier}, ...]
    """
    all_topics = get_all_topics_for_course(course_id)
    studied_set = set(topics_studied)
    recommendations = []

    for topic_id, info in all_topics.items():
        if topic_id in studied_set:
            continue
        prereqs = set(info.get("prerequisites", []))
        if prereqs.issubset(studied_set):
            recommendations.append({
                "topic_id": topic_id,
                "display_name": info["display_name"],
                "tier": info["tier"]
            })

    recommendations.sort(key=lambda x: x["tier"])
    return recommendations


def get_course_type(course_id):
    """Return 'programming', 'theory', or 'mixed'"""
    course = get_course(course_id)
    return course["type"] if course else "mixed"


def print_course_map():
    """Print a visual overview of all courses and their topics"""
    print("\n" + "="*65)
    print("  🎓 AI TUTOR — COURSE & TOPIC MAP")
    print("="*65)

    for course_id, course in COURSES.items():
        print(f"\n{course['icon']}  {course['display_name']}  [{course_id}]  ({course['type']})")
        print(f"   {course['description']}")

        # Group topics by tier
        by_tier = {}
        for tid, tinfo in course["topics"].items():
            tier = tinfo["tier"]
            by_tier.setdefault(tier, []).append((tid, tinfo))

        tier_labels = {1: "Beginner", 2: "Intermediate", 3: "Advanced", 4: "Expert"}
        for tier in sorted(by_tier.keys()):
            print(f"\n   Tier {tier} — {tier_labels.get(tier, '')}:")
            for tid, tinfo in by_tier[tier]:
                prereqs = tinfo.get("prerequisites", [])
                prereq_str = f"  ← needs: {', '.join(prereqs)}" if prereqs else ""
                print(f"     • {tinfo['display_name']:<40} [{tid}]{prereq_str}")

    total_topics = sum(len(c["topics"]) for c in COURSES.values())
    print(f"\n{'='*65}")
    print(f"  {len(COURSES)} courses  |  {total_topics} topics total")
    print("="*65 + "\n")


# ==============================================================================
# TESTING
# ==============================================================================

if __name__ == "__main__":

    print_course_map()

    print("--- Testing helpers ---\n")

    # All course IDs
    print(f"✅ Course IDs: {get_all_course_ids()}\n")

    # Topics in a course
    topics = get_all_topic_ids_for_course("hci")
    print(f"✅ HCI topics ({len(topics)}): {topics}\n")

    # Recommendations
    studied = ["java_basics", "java_data_types", "java_conditionals"]
    recs = get_recommended_next_topics("java", studied)
    print(f"✅ Java recommendations after studying basics:")
    for r in recs:
        print(f"   → {r['display_name']} (Tier {r['tier']})")

    # Prompt context
    print(f"\n✅ Prompt context for DSA → sorting:")
    print(get_topic_prompt_context("dsa", "sorting"))

    print("\n✅ All registry tests passed!")