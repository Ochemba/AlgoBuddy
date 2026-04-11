# shared_cache.py
import streamlit as st
from course_registry import COURSES, get_all_topic_ids_for_course, get_topic, get_course
from prompts import PERSONAS

# ============================================
# CACHE THAT PERSISTS ACROSS ALL PAGES
# Using st.cache_resource - never clears automatically
# ============================================

@st.cache_resource
def get_courses():
    """Course data - loads once and persists across all pages"""
    return COURSES

@st.cache_resource
def get_personas():
    """Persona data - loads once and persists across all pages"""
    return PERSONAS

@st.cache_resource
def get_course_list():
    """List of course keys - persists across pages"""
    return list(COURSES.keys())

@st.cache_resource
def get_course_labels():
    """Course display labels - persists across pages"""
    labels = {None: "— No course —"}
    labels.update({cid: f"{c['icon']} {c['display_name']}" for cid, c in COURSES.items()})
    return labels

@st.cache_resource
def get_avatar_map():
    """Avatar mapping - never changes"""
    return {"batman": "🦇", "hermione": "🧙‍♀️", "tony_stark": "⚙️", "yoda": "🟢", "chill_senior": "😎", "default": "🤖"}

# ============================================
# DATA THAT SHOULD REFRESH OCCASIONALLY
# Using st.cache_data with TTL
# ============================================

@st.cache_data(ttl=300)  # 5 minutes
def get_topics_for_course(course_id):
    """Get topics for a course - refreshes every 5 minutes"""
    if not course_id:
        return []
    return get_all_topic_ids_for_course(course_id)

@st.cache_data(ttl=300)
def get_topic_display(course_id, topic_id):
    """Get topic display name - refreshes every 5 minutes"""
    if not course_id or not topic_id:
        return None
    t = get_topic(course_id, topic_id)
    return t["display_name"] if t else None

@st.cache_data(ttl=300)
def get_course_display(course_id):
    """Get course display name - refreshes every 5 minutes"""
    if not course_id:
        return None
    c = get_course(course_id)
    return c["display_name"] if c else None

# ============================================
# CLEAR CACHE FUNCTION
# ============================================

def clear_all_caches():
    """Clear all caches - call when user logs out"""
    get_courses.clear()
    get_personas.clear()
    get_course_list.clear()
    get_course_labels.clear()
    get_avatar_map.clear()
    get_topics_for_course.clear()
    get_topic_display.clear()
    get_course_display.clear()
    st.cache_data.clear()