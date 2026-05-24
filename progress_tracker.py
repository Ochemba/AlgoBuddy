# progress_tracker.py — AlgoBuddy Progress Tracking with Supabase
"""
Tracks student progress: XP, streaks, accuracy, badges.
"""

from supabase_client import retry_on_error
from supabase_client import supabase
from datetime import date, datetime, timedelta
from typing import Optional

# Levels configuration
LEVELS = [
    {"name": "Beginner", "min_xp": 0, "icon": "🌱", "max_xp": 99},
    {"name": "Explorer", "min_xp": 100, "icon": "🔍", "max_xp": 249},
    {"name": "Apprentice", "min_xp": 250, "icon": "📘", "max_xp": 299},
    {"name": "Journeyman", "min_xp": 300, "icon": "⚙️", "max_xp": 599},
    {"name": "Developer", "min_xp": 600, "icon": "💻", "max_xp": 849},
    {"name": "Coder", "min_xp": 850, "icon": "⚙️", "max_xp": 1299},
    {"name": "Debugger", "min_xp": 1300, "icon": "🐛", "max_xp": 1849},
    {"name": "Architect", "min_xp": 1850, "icon": "🏗️", "max_xp": 2499},
    {"name": "Engineer", "min_xp": 2500, "icon": "🔧", "max_xp": 3299},
    {"name": "Senior Dev", "min_xp": 3300, "icon": "🚀", "max_xp": 4299},
    {"name": "AlgoMaster", "min_xp": 4300, "icon": "🏆", "max_xp": 999999},
]

# Badges configuration
BADGES = [
    # Practice badges
    {
        "id": "first_attempt",
        "name": "First Step",
        "icon": "👣",
        "desc": "Attempt your first practice problem",
        "requirement": "problems_attempted >= 1",
    },
    {
        "id": "ten_problems",
        "name": "Getting Warm",
        "icon": "🔥",
        "desc": "Attempt 10 practice problems",
        "requirement": "problems_attempted >= 10",
    },
    {
        "id": "fifty_problems",
        "name": "Grinder",
        "icon": "💪",
        "desc": "Attempt 50 practice problems",
        "requirement": "problems_attempted >= 50",
    },
    {
        "id": "hundred_problems",
        "name": "Century",
        "icon": "💯",
        "desc": "Attempt 100 practice problems",
        "requirement": "problems_attempted >= 100",
    },
    # Accuracy badges
    {
        "id": "accuracy_70",
        "name": "Sharp Mind",
        "icon": "🎯",
        "desc": "Reach 70% overall accuracy",
        "requirement": "accuracy >= 70",
    },
    {
        "id": "accuracy_90",
        "name": "Precision",
        "icon": "🏹",
        "desc": "Reach 90% overall accuracy",
        "requirement": "accuracy >= 90",
    },
    # Hint-free badges
    {
        "id": "hint_free_5",
        "name": "Independent",
        "icon": "🧠",
        "desc": "Solve 5 problems without hints",
        "requirement": "hint_free_solves >= 5",
    },
    {
        "id": "hint_free_20",
        "name": "No Crutches",
        "icon": "🦾",
        "desc": "Solve 20 problems without hints",
        "requirement": "hint_free_solves >= 20",
    },
    # Time badges
    {
        "id": "night_owl", 
        "name": "Night Owl", 
        "icon": "🦉", 
        "desc": "Study after midnight (12 AM - 5 AM)", 
        "requirement": "night_study_sessions >= 3"
    },
    {
        "id": "streak_7",
        "name": "Week Warrior",
        "icon": "🗓️",
        "desc": "Study 7 days in a row",
        "requirement": "current_streak >= 7",
    },
    {
        "id": "early_bird",
        "name": "Early Bird",
        "icon": "🌅",
        "desc": "Study early in the morning (5 AM - 8 AM)",
        "requirement": "morning_study_sessions >= 3"
    },
    # Streak badges
    {
        "id": "streak_3",
        "name": "On a Roll",
        "icon": "📅",
        "desc": "Study 3 days in a row",
        "requirement": "current_streak >= 3",
    },
    
    {
        "id": "streak_30",
        "name": "Unstoppable",
        "icon": "⚡",
        "desc": "Study 30 days in a row",
        "requirement": "current_streak >= 30",
    },
    # Flashcard badges
   
    {
        "id": "chat_sess",
        "name": "Yapper",
        "icon": "🗣️",
        "desc": "Complete 12 chat sessions",
        "requirement": "chat_sessions >= 12"
    },
    {
        "id": "flashcard_100",
        "name": "Deck Master",
        "icon": "🎴",
        "desc": "Review 100 flashcards",
        "requirement": "flashcards_reviewed >= 100",
    },
    # Topic breadth badges
    {
        "id": "topics_3",
        "name": "Curious",
        "icon": "🔭",
        "desc": "Study 3 different topics",
        "requirement": "topics_studied_count >= 3",
    },
    {
        "id": "topics_10",
        "name": "Well-Rounded",
        "icon": "🌐",
        "desc": "Study 10 different topics",
        "requirement": "topics_studied_count >= 10",
    },
    # Chat / engagement badges
    {
        "id": "chat_sessions_5",
        "name": "Chatty",
        "icon": "💬",
        "desc": "Complete 5 chat sessions",
        "requirement": "chat_sessions >= 5",
    },
    {
        "id": "notes_upload",
        "name": "Note Taker",
        "icon": "📎",
        "desc": "Upload your own notes",
        "requirement": "notes_uploaded >= 1",
    },
    # XP milestone badges
    {
        "id": "xp_500",
        "name": "Levelling Up",
        "icon": "⭐",
        "desc": "Earn 500 XP",
        "requirement": "xp >= 500",
    },
    {
        "id": "flashcard_10",
        "name": "Card Shark",
        "icon": "🃏",
        "desc": "Review 10 flashcards",
        "requirement": "flashcards_reviewed >= 10",
    },
    {
        "id": "xp_2000",
        "name": "XP Machine",
        "icon": "🌟",
        "desc": "Earn 2000 XP",
        "requirement": "xp >= 2000",
    },
    # Completionist badge — earns automatically when all others are done
    {
        "id": "badge_collector",
        "name": "Badge Collector",
        "icon": "🎖️",
        "desc": "Earn every Tier 1 badge",
        "requirement": "all_tier1_badges_earned >= 1",
    },
]

# Badges Tier 2
BADGES_TIER2 = [
    {
        "id": "t2_legend",
        "name": "Legend",
        "icon": "🦁",
        "desc": "Reach Grandmaster level (1500 XP)",
        "requirement": "xp >= 1500",
    },
    {
        "id": "t2_500_problems",
        "name": "Problem Slayer",
        "icon": "⚔️",
        "desc": "Attempt 500 practice problems",
        "requirement": "problems_attempted >= 500",
    },
    {
        "id": "t2_perfectionist",
        "name": "Perfectionist",
        "icon": "💎",
        "desc": "Reach 95% overall accuracy",
        "requirement": "accuracy >= 95",
    },
    {
        "id": "t2_streak_100",
        "name": "Century Streak",
        "icon": "🔱",
        "desc": "Study 100 days in a row",
        "requirement": "current_streak >= 100",
    },
    {
        "id": "t2_independent", 
        "name": "Independent Thinker", 
        "icon": "🧠", 
        "desc": "Solve 50 problems without hints",
        "requirement": "hint_free_solves >= 50"
    },
    
    {
        "id": "t2_night_owl_pro", 
        "name": "No Sleep!", 
        "icon": "🦉", 
        "desc": "Study after midnight 30 times",
        "requirement": "night_study_sessions >= 30"
    },
    {
        "id": "t2_early_bird_pro", 
        "name": "First-dibs", 
        "icon": "🌅", 
        "desc": "Study before 8 AM 30 times",
        "requirement": "morning_study_sessions >= 30"
    },
    {
        "id": "t2_self_reliant", 
        "name": "Hot Headed", 
        "icon": "🧨", 
        "desc": "Solve 100 problems without hints",
        "requirement": "hint_free_solves >= 100"
    },
    {
        "id": "t2_social", 
        "name": "Social Butterfly", 
        "icon": "🦋", 
        "desc": "Have 50 chat sessions",
        "requirement": "chat_sessions >= 50"
    },
    {
        "id": "t2_note_keeper", 
        "name": "Note Keeper", 
        "icon": "📚", 
        "desc": "Upload 50 notes",
        "requirement": "notes_uploaded >= 50"
    },
    {
        "id": "t2_topic_explorer", 
        "name": "Topic Explorer", 
        "icon": "🗺️", 
        "desc": "Study 30 different topics",
        "requirement": "topics_studied_count >= 30"
    },
    {
        "id": "t2_flashcard_500",
        "name": "Flash Master",
        "icon": "🌊",
        "desc": "Review 500 flashcards",
        "requirement": "flashcards_reviewed >= 500",
    },
    {
        "id": "t2_hint_free_100",
        "name": "Pure Genius",
        "icon": "🧬",
        "desc": "Solve 100 problems without hints",
        "requirement": "hint_free_solves >= 100",
    },
    {
        "id": "t2_topics_all",
        "name": "Omniscient",
        "icon": "🌍",
        "desc": "Study 25 different topics",
        "requirement": "topics_studied_count >= 25",
    },
    {
        "id": "t2_chat_50",
        "name": "Deep Thinker",
        "icon": "🔮",
        "desc": "Complete 50 chat sessions",
        "requirement": "chat_sessions >= 50",
    },
    {
        "id": "t2_xp_10000",
        "name": "XP God",
        "icon": "👑",
        "desc": "Earn 10,000 XP",
        "requirement": "xp >= 10000",
    },
    {
        "id": "t2_all_tier2",
        "name": "The AlgoBuddy",
        "icon": "🤖",
        "desc": "Earn every Tier 2 badge — you are AlgoBuddy",
        "requirement": "all_tier2_badges_earned >= 1",
    },
]

# XP awards
XP_AWARDS = {
    "problem_correct": 4,
    "hint_free_correct": 5,
    "flashcard_review": 2,
    "chat_session": 10,
    "notes_upload": 5,
    "streak_bonus": 7,
}


class ProgressTracker:
    """Tracks student progress with Supabase persistence."""

    def __init__(self, student_name: str, user_id: str = None):
        self.student_name = student_name
        self._user_id = user_id
        self._stats_cache = None
        self._topics_studied = set()

    def _get_user_id(self) -> str:
        """Get current user ID from session or cache."""
        if self._user_id:
            return self._user_id
        
        try:
            import streamlit as st
            return st.session_state.get("user_id")
        except Exception:
            return None

    @retry_on_error(max_retries=3, delay=1.0)
    def _get_progress(self) -> dict:
        """Get or create progress record for current user."""
        user_id = self._get_user_id()
        if not user_id:
            return {}

        try:
            result = supabase().table("user_progress").select("*").eq("user_id", user_id).execute()
            if result.data:
                self._stats_cache = result.data[0]
                # Ensure time-based fields exist
                if "study_sessions_by_hour" not in self._stats_cache:
                    self._stats_cache["study_sessions_by_hour"] = {}
                if "night_study_sessions" not in self._stats_cache:
                    self._stats_cache["night_study_sessions"] = 0
                if "morning_study_sessions" not in self._stats_cache:
                    self._stats_cache["morning_study_sessions"] = 0
                return self._stats_cache
            else:
                insert = supabase().table("user_progress").insert({
                    "user_id": user_id,
                    "study_sessions_by_hour": {},
                    "night_study_sessions": 0,
                    "morning_study_sessions": 0
                }).execute()
                if insert.data:
                    self._stats_cache = insert.data[0]
                    return self._stats_cache
        except Exception as e:
            print(f"Error getting progress: {e}")
        return {}

    @retry_on_error(max_retries=3, delay=1.0)
    def _update_progress(self, updates: dict) -> bool:
        """Update progress record."""
        user_id = self._get_user_id()
        if not user_id:
            return False

        try:
            result = supabase().table("user_progress").update(updates).eq("user_id", user_id).execute()
            if result.data:
                self._stats_cache = result.data[0]
                return True
        except Exception as e:
            print(f"Error updating progress: {e}")
        return False

    def _add_xp(self, amount: int, reason: str) -> None:
        """Add XP and record in history."""
        user_id = self._get_user_id()
        if not user_id:
            return

        try:
            progress = self._get_progress()
            current_xp = progress.get("xp", 0)
            new_xp = current_xp + amount

            self._update_progress({"xp": new_xp})

            supabase().table("xp_history").insert({
                "user_id": user_id,
                "amount": amount,
                "reason": reason
            }).execute()

        except Exception as e:
            print(f"Error adding XP: {e}")

    def record_study_session(self):
        """Record when a user studies (for time-based badges)"""
        from datetime import datetime
        current_hour = datetime.now().hour
        
        # Get current progress
        progress = self._get_progress()
        
        # Initialize study_sessions_by_hour if it doesn't exist
        if "study_sessions_by_hour" not in progress:
            study_sessions = {}
        else:
            study_sessions = progress.get("study_sessions_by_hour", {})
        
        # Track sessions by hour
        hour_str = str(current_hour)
        study_sessions[hour_str] = study_sessions.get(hour_str, 0) + 1
        
        # Get current counts
        night_count = progress.get("night_study_sessions", 0)
        morning_count = progress.get("morning_study_sessions", 0)
        
        # Night Owl: 12 AM - 5 AM (hours 0-4)
        if 0 <= current_hour <= 4:
            night_count += 1
        
        # Early Bird: 5 AM - 8 AM (hours 5-7)
        elif 5 <= current_hour <= 7:
            morning_count += 1
        
        # Update all at once
        self._update_progress({
            "study_sessions_by_hour": study_sessions,
            "night_study_sessions": night_count,
            "morning_study_sessions": morning_count
        })

    def _check_and_award_badges(self) -> list:
        """Check and award any new badges."""
        user_id = self._get_user_id()
        if not user_id:
            return []

        progress = self._get_progress()
        earned = set(progress.get("earned_badges", []))
        new_badges = []

        # Calculate context for badge conditions
        ctx = {
            "problems_attempted": progress.get("problems_attempted", 0),
            "accuracy": self.get_accuracy(),
            "hint_free_solves": progress.get("hint_free_solves", 0),
            "current_streak": progress.get("current_streak", 0),
            "flashcards_reviewed": progress.get("flashcards_reviewed", 0),
            "topics_studied_count": len(self._topics_studied),
            "chat_sessions": progress.get("chat_sessions", 0),
            "notes_uploaded": progress.get("notes_uploaded", 0),
            "night_study_sessions": progress.get("night_study_sessions", 0),
            "morning_study_sessions": progress.get("morning_study_sessions", 0),
            "xp": progress.get("xp", 0),
            "all_tier1_badges_earned": 0,
            "all_tier2_badges_earned": 0,
        }

        # Tier 1 badges (excluding badge_collector)
        tier1_ids = [b["id"] for b in BADGES if b["id"] != "badge_collector"]
        for badge in BADGES:
            if badge["id"] == "badge_collector":
                continue
            if badge["id"] not in earned:
                try:
                    if eval(badge["requirement"], {"__builtins__": {}}, ctx):
                        earned.add(badge["id"])
                        new_badges.append(badge["id"])
                except Exception:
                    pass

        # Check if all Tier 1 badges are earned
        all_t1_done = all(bid in earned for bid in tier1_ids)
        ctx["all_tier1_badges_earned"] = 1 if all_t1_done else 0
        if all_t1_done and "badge_collector" not in earned:
            earned.add("badge_collector")
            new_badges.append("badge_collector")

        # Tier 2 badges (only if badge_collector is earned)
        if "badge_collector" in earned:
            tier2_ids = [b["id"] for b in BADGES_TIER2 if b["id"] != "t2_all_tier2"]
            for badge in BADGES_TIER2:
                if badge["id"] == "t2_all_tier2":
                    continue
                if badge["id"] not in earned:
                    try:
                        if eval(badge["requirement"], {"__builtins__": {}}, ctx):
                            earned.add(badge["id"])
                            new_badges.append(badge["id"])
                    except Exception:
                        pass

            # Check if all Tier 2 badges are earned
            all_t2_done = all(bid in earned for bid in tier2_ids)
            ctx["all_tier2_badges_earned"] = 1 if all_t2_done else 0
            if all_t2_done and "t2_all_tier2" not in earned:
                earned.add("t2_all_tier2")
                new_badges.append("t2_all_tier2")

        if new_badges:
            self._update_progress({"earned_badges": list(earned)})

        return new_badges

    def _update_streak(self) -> None:
        """Update streak based on last active date."""
        progress = self._get_progress()
        if not progress:
            return

        last_active = progress.get("last_active_date")
        today = date.today().isoformat()

        if last_active == today:
            return

        current_streak = progress.get("current_streak", 0)
        longest_streak = progress.get("longest_streak", 0)

        if last_active == (date.today() - timedelta(days=1)).isoformat():
            current_streak += 1
            if current_streak > longest_streak:
                longest_streak = current_streak
            # Award streak bonus for milestones
            if current_streak in [3, 7, 14, 30, 100]:
                self._add_xp(XP_AWARDS["streak_bonus"], f"{current_streak}-day streak bonus")
        else:
            current_streak = 1

        updates = {
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "last_active_date": today
        }
        self._update_progress(updates)

    def get_stats_summary(self) -> dict:
        """Get a summary of all stats."""
        progress = self._get_progress()
        if not progress:
            return {"xp": 0, "level": LEVELS[0], "level_progress": {"pct": 0, "needed": 100}, "earned_badges": []}

        xp = progress.get("xp", 0)

        # Find current level by finding the highest level where xp >= min_xp
        current_level = LEVELS[0]
        for level in LEVELS:
            if xp >= level["min_xp"]:
                current_level = level
            else:
                break

        # Find next level (the one after current)
        level_index = -1
        for i, lvl in enumerate(LEVELS):
            if lvl["name"] == current_level["name"]:
                level_index = i
                break
        
        next_level = LEVELS[level_index + 1] if level_index + 1 < len(LEVELS) else current_level
        
        xp_in_level = xp - current_level["min_xp"]
        xp_needed = next_level["min_xp"] - current_level["min_xp"]
        pct = (xp_in_level / xp_needed * 100) if xp_needed > 0 else 100

        # Ensure badges are checked
        self._check_and_award_badges()
        progress = self._get_progress()

        return {
            "xp": xp,
            "level": current_level,
            "level_progress": {
                "pct": min(100, pct),
                "needed": max(0, next_level["min_xp"] - xp)
            },
            "earned_badges": progress.get("earned_badges", [])
        }

    def get_accuracy(self) -> float:
        """Calculate overall accuracy."""
        progress = self._get_progress()
        attempted = progress.get("problems_attempted", 0)
        correct = progress.get("problems_correct", 0)

        if attempted == 0:
            return 0.0
        return (correct / attempted) * 100

    def get_topic_performance(self) -> dict:
        """Get performance by topic."""
        user_id = self._get_user_id()
        if not user_id:
            return {}

        try:
            result = supabase().table("topic_performance").select("*").eq("user_id", user_id).execute()
            performance = {}
            for row in result.data:
                attempts = row.get("attempts", 0)
                correct = row.get("correct", 0)
                accuracy = (correct / attempts * 100) if attempts > 0 else 0
                performance[row["topic_id"]] = {
                    "attempts": attempts,
                    "correct": correct,
                    "accuracy": accuracy
                }
                if attempts > 0:
                    self._topics_studied.add(row["topic_id"])
            return performance
        except Exception:
            return {}

    @retry_on_error(max_retries=3, delay=1.0)
    def record_problem_attempt(self, topic: str, is_correct: bool, hints_used: int = 0, difficulty: str = "medium", problem_type: str = "standard") -> None:
        """Record a problem attempt."""
        user_id = self._get_user_id()
        if not user_id:
            return

        # Track topics studied
        self._topics_studied.add(topic)

        # Update streak
        self._update_streak()

        progress = self._get_progress()
        attempted = progress.get("problems_attempted", 0) + 1
        correct = progress.get("problems_correct", 0) + (1 if is_correct else 0)

        updates = {
            "problems_attempted": attempted,
            "problems_correct": correct
        }

        if is_correct and hints_used == 0:
            updates["hint_free_solves"] = progress.get("hint_free_solves", 0) + 1
            self._add_xp(XP_AWARDS["hint_free_correct"], f"Hint-free solve on {topic}")

        if is_correct:
            self._add_xp(XP_AWARDS["problem_correct"], f"Correct answer on {topic}")

        self._update_progress(updates)

        # Update topic performance
        try:
            existing = supabase().table("topic_performance").select("*").eq("user_id", user_id).eq("topic_id", topic).execute()
            if existing.data:
                record = existing.data[0]
                supabase().table("topic_performance").update({
                    "attempts": record["attempts"] + 1,
                    "correct": record["correct"] + (1 if is_correct else 0),
                    "hints_used": record["hints_used"] + hints_used,
                    "last_practiced": datetime.now().isoformat()
                }).eq("id", record["id"]).execute()
            else:
                supabase().table("topic_performance").insert({
                    "user_id": user_id,
                    "topic_id": topic,
                    "attempts": 1,
                    "correct": 1 if is_correct else 0,
                    "hints_used": hints_used,
                    "last_practiced": datetime.now().isoformat()
                }).execute()
        except Exception as e:
            print(f"Error updating topic performance: {e}")

        # Record practice attempt
        try:
            supabase().table("practice_attempts").insert({
                "user_id": user_id,
                "topic_id": topic,
                "difficulty": difficulty,
                "problem_type": problem_type,
                "is_correct": is_correct,
                "hints_used": hints_used
            }).execute()
        except Exception:
            pass

        # Check badges
        self._check_and_award_badges()

    @retry_on_error(max_retries=3, delay=1.0)
    def record_flashcard_review(self, count: int) -> None:
        """Record flashcard reviews."""
        user_id = self._get_user_id()
        if not user_id:
            return

        progress = self._get_progress()
        reviewed = progress.get("flashcards_reviewed", 0) + count
        self._update_progress({"flashcards_reviewed": reviewed})

        xp_gained = count * XP_AWARDS["flashcard_review"]
        self._add_xp(xp_gained, f"Reviewed {count} flashcard(s)")

        self._check_and_award_badges()

    def record_chat_session(self) -> None:
        """Record a chat session."""
        user_id = self._get_user_id()
        if not user_id:
            return

        progress = self._get_progress()
        sessions = progress.get("chat_sessions", 0) + 1
        self._update_progress({"chat_sessions": sessions})

        self._add_xp(XP_AWARDS["chat_session"], "Completed a chat session")
        self._check_and_award_badges()

    def record_notes_upload(self) -> None:
        """Record notes upload."""
        user_id = self._get_user_id()
        if not user_id:
            return

        progress = self._get_progress()
        notes = progress.get("notes_uploaded", 0) + 1
        self._update_progress({"notes_uploaded": notes})

        self._add_xp(XP_AWARDS["notes_upload"], "Uploaded notes")
        self._check_and_award_badges()

    def get_weak_topics(self, limit: int = 3) -> list:
        """Get topics with lowest accuracy."""
        perf = self.get_topic_performance()
        topics = []
        for topic, data in perf.items():
            if data["attempts"] >= 3:
                topics.append({
                    "topic": topic,
                    "accuracy": data["accuracy"]
                })
        topics.sort(key=lambda x: x["accuracy"])
        return topics[:limit]

    def get_strong_topics(self, limit: int = 3) -> list:
        """Get topics with highest accuracy."""
        perf = self.get_topic_performance()
        topics = []
        for topic, data in perf.items():
            if data["attempts"] >= 3:
                topics.append({
                    "topic": topic,
                    "accuracy": data["accuracy"]
                })
        topics.sort(key=lambda x: -x["accuracy"])
        return topics[:limit]

    @property
    def stats(self) -> dict:
        """Return stats dict for backward compatibility."""
        progress = self._get_progress()
        return {
            "xp": progress.get("xp", 0),
            "current_streak": progress.get("current_streak", 0),
            "longest_streak": progress.get("longest_streak", 0),
            "problems_attempted": progress.get("problems_attempted", 0),
            "problems_correct": progress.get("problems_correct", 0),
            "hint_free_solves": progress.get("hint_free_solves", 0),
            "flashcards_reviewed": progress.get("flashcards_reviewed", 0),
            "chat_sessions": progress.get("chat_sessions", 0),
            "notes_uploaded": progress.get("notes_uploaded", 0),
            "earned_badges": progress.get("earned_badges", []),
            "topic_performance": self.get_topic_performance(),
            "xp_history": [],
            "study_sessions_by_hour": progress.get("study_sessions_by_hour", {}),
            "night_study_sessions": progress.get("night_study_sessions", 0),
            "morning_study_sessions": progress.get("morning_study_sessions", 0),
        }

    def load_from_file(self, filename: str) -> None:
        """Legacy method - no-op for Supabase."""
        pass

    def save_to_file(self, filename: str) -> None:
        """Legacy method - no-op for Supabase."""
        pass