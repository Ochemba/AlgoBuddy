"""
learning_profile.py
===================
Tracks a student's learning style and adapts AlgoBuddy's behaviour.

Level 1 — Passive adaptation
    AlgoBuddy silently observes signals and adjusts automatically.

Level 2 — Active adaptation
    AlgoBuddy surfaces what it has learned about the student and
    lets them confirm, correct, or override it.

Signals tracked
---------------
- hint_rate        : fraction of problems where hints were used
- retry_rate       : fraction of problems retried after wrong answer
- avg_difficulty   : weighted average difficulty solved (easy=1, medium=2, hard=3)
- preferred_type   : most-attempted question type (MCQ / FILL_BLANK / STANDARD)
- session_length   : rolling average messages per chat session
- accuracy_trend   : last-10 accuracy minus previous-10 accuracy (positive = improving)

Derived learning style dimensions
----------------------------------
- depth_preference   : "examples" | "theory" | "balanced"
  (high hint_rate + high retry_rate → "examples";
   low hint_rate + low retry → "theory"; otherwise "balanced")

- pace_preference    : "slow" | "normal" | "fast"
  (high hint_rate → "slow"; low hint_rate + hard avg_diff → "fast")

- confidence_level   : "low" | "medium" | "high"
  (derived from accuracy_trend + avg_difficulty)

- engagement_style   : "interactive" | "passive"
  (high MCQ/fill_blank preference → "interactive")

These four dimensions feed directly into tutor_engine prompts.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Literal


# ── Types ─────────────────────────────────────────────────────────────────────
DepthPref      = Literal["examples", "theory", "balanced"]
PacePref       = Literal["slow", "normal", "fast"]
ConfidenceLevel = Literal["low", "medium", "high"]
EngagementStyle = Literal["interactive", "passive"]


@dataclass
class LearningProfile:
    # ── Raw signal counters ────────────────────────────────────────────────
    problems_with_hints: int = 0
    problems_without_hints: int = 0
    problems_retried: int = 0
    problems_not_retried: int = 0
    difficulty_scores: list = field(default_factory=list)   # 1/2/3 per attempt
    type_counts: dict = field(default_factory=lambda: {
        "MCQ": 0, "FILL_BLANK": 0, "STANDARD": 0
    })
    accuracy_history: list = field(default_factory=list)    # True/False per attempt
    session_lengths: list = field(default_factory=list)     # message count per session

    # ── Derived style (recomputed on every update) ─────────────────────────
    depth_preference: DepthPref = "balanced"
    pace_preference: PacePref = "normal"
    confidence_level: ConfidenceLevel = "medium"
    engagement_style: EngagementStyle = "interactive"

    # ── Active-adaptation state ────────────────────────────────────────────
    # Has the student confirmed/overridden the auto-detected style?
    style_confirmed: bool = False
    # Overrides set by the student (None = use auto-detected)
    depth_override: DepthPref | None = None
    pace_override: PacePref | None = None

    # ── Metadata ──────────────────────────────────────────────────────────
    total_signals: int = 0   # how many data points we have
    last_insight_shown: int = 0   # total_signals when we last showed an insight

    # ── Properties ────────────────────────────────────────────────────────
    @property
    def effective_depth(self) -> DepthPref:
        return self.depth_override or self.depth_preference

    @property
    def effective_pace(self) -> PacePref:
        return self.pace_override or self.pace_preference

    @property
    def has_enough_data(self) -> bool:
        """Need at least 5 signals before we start adapting."""
        return self.total_signals >= 5

    @property
    def should_show_insight(self) -> bool:
        """
        Surface a Level-2 insight every 10 new signals,
        but only once we have at least 10 total.
        """
        return (
            self.total_signals >= 10
            and (self.total_signals - self.last_insight_shown) >= 10
            and not self.style_confirmed
        )

    # ── Signal recording ──────────────────────────────────────────────────
    def record_problem(
        self,
        used_hints: bool,
        retried: bool,
        difficulty: str,           # "easy" | "medium" | "hard"
        question_type: str,        # "MCQ" | "FILL_BLANK" | "STANDARD"
        is_correct: bool,
    ):
        diff_score = {"easy": 1, "medium": 2, "hard": 3}.get(difficulty, 2)
        if used_hints:
            self.problems_with_hints += 1
        else:
            self.problems_without_hints += 1

        if retried:
            self.problems_retried += 1
        else:
            self.problems_not_retried += 1

        self.difficulty_scores.append(diff_score)
        if len(self.difficulty_scores) > 50:   # rolling window
            self.difficulty_scores = self.difficulty_scores[-50:]

        qt = question_type if question_type in self.type_counts else "STANDARD"
        self.type_counts[qt] += 1

        self.accuracy_history.append(is_correct)
        if len(self.accuracy_history) > 20:
            self.accuracy_history = self.accuracy_history[-20:]

        self.total_signals += 1
        self._recompute()

    def record_session(self, message_count: int):
        self.session_lengths.append(message_count)
        if len(self.session_lengths) > 20:
            self.session_lengths = self.session_lengths[-20:]
        self.total_signals += 1
        self._recompute()

    # ── Internal recompute ────────────────────────────────────────────────
    def _recompute(self):
        if not self.has_enough_data:
            return

        total_probs = self.problems_with_hints + self.problems_without_hints
        hint_rate   = self.problems_with_hints / total_probs if total_probs else 0

        total_tries = self.problems_retried + self.problems_not_retried
        retry_rate  = self.problems_retried / total_tries if total_tries else 0

        avg_diff = (
            sum(self.difficulty_scores) / len(self.difficulty_scores)
            if self.difficulty_scores else 2.0
        )

        # ── Depth preference ──────────────────────────────────────────────
        if hint_rate > 0.5 or retry_rate > 0.4:
            self.depth_preference = "examples"
        elif hint_rate < 0.2 and retry_rate < 0.15:
            self.depth_preference = "theory"
        else:
            self.depth_preference = "balanced"

        # ── Pace preference ───────────────────────────────────────────────
        if hint_rate > 0.55 or avg_diff < 1.5:
            self.pace_preference = "slow"
        elif hint_rate < 0.15 and avg_diff > 2.3:
            self.pace_preference = "fast"
        else:
            self.pace_preference = "normal"

        # ── Confidence level ──────────────────────────────────────────────
        accuracy_trend = self._accuracy_trend()
        recent_acc     = self._recent_accuracy()
        if recent_acc >= 0.75 or (accuracy_trend > 0.1 and avg_diff >= 2):
            self.confidence_level = "high"
        elif recent_acc < 0.45 or accuracy_trend < -0.1:
            self.confidence_level = "low"
        else:
            self.confidence_level = "medium"

        # ── Engagement style ──────────────────────────────────────────────
        interactive_total = self.type_counts["MCQ"] + self.type_counts["FILL_BLANK"]
        all_total         = sum(self.type_counts.values())
        if all_total and interactive_total / all_total > 0.5:
            self.engagement_style = "interactive"
        else:
            self.engagement_style = "passive"

    def _recent_accuracy(self, n: int = 10) -> float:
        recent = self.accuracy_history[-n:]
        return sum(recent) / len(recent) if recent else 0.5

    def _accuracy_trend(self) -> float:
        """Positive = improving, negative = declining."""
        h = self.accuracy_history
        if len(h) < 10:
            return 0.0
        mid  = len(h) // 2
        old  = sum(h[:mid]) / mid
        new  = sum(h[mid:]) / (len(h) - mid)
        return new - old

    # ── Serialisation ─────────────────────────────────────────────────────
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "LearningProfile":
        obj = cls()
        for k, v in d.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        return obj

    def save(self, path: str):
        try:
            with open(path, "w") as f:
                json.dump(self.to_dict(), f, indent=2)
        except Exception:
            pass

    @classmethod
    def load(cls, path: str) -> "LearningProfile":
        try:
            if os.path.exists(path):
                with open(path) as f:
                    return cls.from_dict(json.load(f))
        except Exception:
            pass
        return cls()


# ── Prompt fragment builder ───────────────────────────────────────────────────
def build_adaptation_prompt(profile: LearningProfile) -> str:
    """
    Returns a short instruction block to inject into the system prompt.
    Called by tutor_engine.py.
    """
    if not profile.has_enough_data:
        return ""

    lines = ["[LEARNING PROFILE — adapt your responses accordingly]"]

    depth = profile.effective_depth
    pace  = profile.effective_pace
    conf  = profile.confidence_level

    # Depth / explanation style
    if depth == "examples":
        lines.append(
            "• This student learns best from concrete examples and step-by-step "
            "walkthroughs. Lead with examples before theory."
        )
    elif depth == "theory":
        lines.append(
            "• This student prefers concise theoretical explanations. "
            "Skip excessive examples unless asked."
        )
    else:
        lines.append(
            "• Balance theory and examples equally for this student."
        )

    # Pace
    if pace == "slow":
        lines.append(
            "• Take it step by step. Break explanations into smaller pieces. "
            "Offer to check understanding after each concept."
        )
    elif pace == "fast":
        lines.append(
            "• This student moves quickly. Keep responses concise and advance "
            "to harder concepts when they answer correctly."
        )

    # Confidence
    if conf == "low":
        lines.append(
            "• The student's confidence is low right now. Be extra encouraging, "
            "normalise mistakes, and celebrate small wins."
        )
    elif conf == "high":
        lines.append(
            "• The student is performing confidently. Challenge them with "
            "follow-up questions and harder variants."
        )

    return "\n".join(lines)


# ── Level-2 insight message builder ──────────────────────────────────────────
def build_insight_message(profile: LearningProfile) -> str:
    """
    Returns a natural-language insight to show the student inside the chat.
    Called when profile.should_show_insight is True.
    """
    depth = profile.depth_preference
    pace  = profile.pace_preference
    conf  = profile.confidence_level

    depth_msg = {
        "examples": "you learn best when I lead with concrete examples",
        "theory":   "you prefer concise theory over lots of examples",
        "balanced": "you respond well to a mix of theory and examples",
    }[depth]

    pace_msg = {
        "slow":   "and you like to take things step by step",
        "normal": "at a steady pace",
        "fast":   "and you're comfortable moving quickly through topics",
    }[pace]

    conf_msg = {
        "low":    "I can see you're building confidence — that's completely normal at this stage.",
        "medium": "Your accuracy is solid and improving.",
        "high":   "You're performing really well — I'll start pushing you with harder challenges.",
    }[conf]

    return (
        f"📊 **AlgoBuddy has noticed** that {depth_msg}, {pace_msg}. "
        f"{conf_msg}\n\n"
        f"I'll keep adjusting how I teach you. You can also tell me directly — "
        f"for example: *\"explain with more examples\"* or *\"go faster\"*."
    )