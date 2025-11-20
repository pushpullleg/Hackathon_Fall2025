"""
Data Engineer Analytics Panel
-----------------------------

Uses stored tutor interaction events to surface mastery, progress,
time-on-task, streaks, personalization, and a Skill-O-Meter gauge.
"""

from __future__ import annotations

import json
import os
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple

import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------


def _get_events_path() -> str:
    """Return absolute path to the tutor events log."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "data", "tutor_events.json")


def _load_events() -> List[Dict[str, Any]]:
    """Load all stored tutor events."""
    path = _get_events_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _parse_timestamp(ts: str) -> datetime | None:
    """Parse ISO timestamps that may end with Z."""
    if not ts:
        return None
    try:
        ts_clean = ts.replace("Z", "+00:00")
        return datetime.fromisoformat(ts_clean)
    except Exception:
        return None


def _chunk_sessions(events: List[Dict[str, Any]]) -> List[Tuple[datetime, datetime]]:
    """
    Group events into contiguous sessions (30 minute idle timeout).

    Returns list of (start, end) tuples.
    """
    sessions: List[Tuple[datetime, datetime]] = []
    sorted_events = sorted(
        (e for e in events if e.get("timestamp")),
        key=lambda e: e["timestamp"],
    )

    current_start: datetime | None = None
    last_time: datetime | None = None
    idle_limit = timedelta(minutes=30)

    for event in sorted_events:
        ts = _parse_timestamp(event["timestamp"])
        if not ts:
            continue
        if current_start is None:
            current_start = ts
            last_time = ts
            continue
        if ts - (last_time or ts) <= idle_limit:
            last_time = ts
            continue
        sessions.append((current_start, last_time or current_start))
        current_start = ts
        last_time = ts

    if current_start:
        sessions.append((current_start, last_time or current_start))

    return sessions


def _calculate_streak(dates: List[datetime]) -> int:
    """Calculate consecutive-day streak based on event dates."""
    if not dates:
        return 0
    unique_dates = {dt.date() for dt in dates}
    today = datetime.utcnow().date()
    streak = 0
    cursor = today

    while cursor in unique_dates:
        streak += 1
        cursor -= timedelta(days=1)

    if streak == 0:
        # No activity today, start from last active day
        cursor = max(unique_dates)
        while cursor in unique_dates:
            streak += 1
            cursor -= timedelta(days=1)

    return streak


def _summarize_user_metrics(user_id: str) -> Dict[str, Any]:
    """Aggregate tutor analytics for a single user."""
    events = [e for e in _load_events() if e.get("user_id") == user_id]
    question_events = [e for e in events if e.get("type") == "tutor_question_answered"]
    assessment_events = [
        e for e in events if e.get("type") == "tutor_assessment_completed"
    ]

    sessions = _chunk_sessions(events)
    total_minutes = 0
    for start, end in sessions:
        duration = max(1, int((end - start).total_seconds() / 60))
        total_minutes += duration

    question_count = len(question_events)
    correct_count = sum(1 for e in question_events if e["data"].get("correct"))
    accuracy = correct_count / question_count if question_count else 0

    level_entry = assessment_events[-1] if assessment_events else None
    level_data = level_entry.get("data", {}) if level_entry else {}
    level_score = level_data.get("score", accuracy)
    level_value = level_data.get("level", 1)
    pillar_stats = level_data.get("pillar_stats", {})

    if not pillar_stats and question_events:
        pillar_tracker: Dict[str, Dict[str, int]] = defaultdict(
            lambda: {"total": 0, "correct": 0}
        )
        for event in question_events:
            pillar = event["data"].get("pillar", "General")
            pillar_tracker[pillar]["total"] += 1
            if event["data"].get("correct"):
                pillar_tracker[pillar]["correct"] += 1
        pillar_stats = pillar_tracker

    day_timestamps = [
        _parse_timestamp(e["timestamp"]) for e in events if e.get("timestamp")
    ]
    streak_days = _calculate_streak([dt for dt in day_timestamps if dt])

    primary_focus = level_data.get("primary_recommendation")
    secondary_focus = level_data.get("secondary_recommendations", [])
    recent_topics = [
        event["data"].get("topic")
        for event in reversed(question_events[-6:])
        if event["data"].get("topic")
    ]

    return {
        "level": level_value,
        "score_pct": level_score * 100,
        "question_count": question_count,
        "correct_count": correct_count,
        "accuracy_pct": accuracy * 100,
        "pillar_stats": pillar_stats,
        "sessions": len(sessions),
        "active_minutes": total_minutes,
        "streak_days": streak_days,
        "primary_focus": primary_focus,
        "secondary_focus": secondary_focus,
        "recent_topics": recent_topics,
        "last_assessed": _parse_timestamp(level_entry["timestamp"]) if level_entry else None,
    }


# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------

LEVEL_LABELS = {
    1: "Beginner",
    2: "Emerging",
    3: "Proficient",
    4: "Advanced",
}


def _render_skill_gauge(level: int, score_pct: float) -> None:
    """Render Skill-O-Meter gauge."""
    thresholds = [
        {"range": [0, 25], "color": "#CF3A4E"},
        {"range": [25, 50], "color": "#F08A24"},
        {"range": [50, 75], "color": "#4A90E2"},
        {"range": [75, 100], "color": "#3CB371"},
    ]
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score_pct,
            number={"suffix": "%"},
            title={"text": f"Skill-O-Meter • L{level} {LEVEL_LABELS.get(level, '')}"},
            gauge={
                "axis": {"range": [0, 100], "tickvals": [0, 25, 50, 75, 100]},
                "bar": {"color": "#FFD700"},
                "steps": thresholds,
                "threshold": {
                    "line": {"color": "#FFFFFF", "width": 4},
                    "thickness": 0.75,
                    "value": score_pct,
                },
            },
        )
    )
    fig.update_layout(height=280, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)


def _render_pillar_progress(pillar_stats: Dict[str, Dict[str, int]]) -> None:
    """Render mastery progress bars per pillar."""
    if not pillar_stats:
        st.info("Answer a few tutor questions to unlock mastery insights.")
        return

    for pillar, stats in pillar_stats.items():
        total = stats.get("total", 1)
        correct = stats.get("correct", 0)
        pct = int((correct / total) * 100) if total else 0
        bar_color = "#3CB371" if pct >= 75 else "#F08A24" if pct >= 40 else "#CF3A4E"
        st.markdown(
            f"""
            <div style="margin-bottom: 0.4rem;">
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#FFFFFF; font-weight:600;">{pillar}</span>
                    <span style="color:#FFFFFF;">{pct}%</span>
                </div>
                <div style="background:#1A1A1A; border-radius:999px; height:8px;">
                    <div style="width:{pct}%; height:8px; border-radius:999px; background:{bar_color};"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_stat_card(label: str, value: str, sub: str = "") -> None:
    st.markdown(
        f"""
        <div style="background: #050505; border: 1px solid #222; border-radius: 12px;
                    padding: 1rem; height: 120px;">
            <p style="margin:0; color:#A0AEC0; font-size:0.85rem;">{label}</p>
            <p style="margin:0.2rem 0 0 0; color:#FFFFFF; font-size:1.6rem; font-weight:700;">
                {value}
            </p>
            <p style="margin:0.1rem 0 0 0; color:#718096; font-size:0.85rem;">{sub}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_de_analytics_panel(user_id: str = "demo-mukesh", user_name: str = "Mukesh") -> None:
    """Render the Data Engineer analytics experience."""
    st.markdown(
        """
        <div style="background: #050505; border: 1px solid #222; border-radius: 16px;
                    padding: 1.2rem 1.5rem; margin-bottom: 1rem;">
            <p style="color:#CF3A4E; font-weight:600; margin:0;">Data Engineer Learning Pulse</p>
            <h3 style="color:#FFFFFF; margin:0.2rem 0 0 0;">📊 Analytics Command Center</h3>
            <p style="color:#94A3B8; margin:0.4rem 0 0 0;">
                Built from your AI Tutor sessions, tailored to <strong>{name}</strong>.
                Track mastery, time-on-task, streaks, and personalized focus areas.
            </p>
        </div>
        """.format(
            name=user_name
        ),
        unsafe_allow_html=True,
    )

    summary = _summarize_user_metrics(user_id)
    level = summary["level"]
    score_pct = summary["score_pct"]

    cols = st.columns([1.2, 1])
    with cols[0]:
        _render_skill_gauge(level, score_pct)
    with cols[1]:
        c1, c2 = st.columns(2)
        with c1:
            minutes = summary["active_minutes"]
            hours = minutes / 60
            time_label = f"{hours:.1f} hrs" if minutes >= 60 else f"{minutes} min"
            _render_stat_card("Time Spent", time_label, "Across tutor sessions")
        with c2:
            _render_stat_card(
                "Questions Answered",
                str(summary["question_count"]),
                f"{summary['accuracy_pct']:.0f}% accuracy",
            )
        c3, c4 = st.columns(2)
        with c3:
            _render_stat_card(
                "Sessions",
                str(summary["sessions"]),
                "Last 30 days" if summary["sessions"] else "No sessions yet",
            )
        with c4:
            streak = summary["streak_days"]
            streak_text = "🔥 streak alive" if streak else "Start your streak"
            _render_stat_card("Streak", f"{streak} days", streak_text)

    st.markdown("---")
    st.markdown("#### 🧠 Mastery by Pillar")
    _render_pillar_progress(summary["pillar_stats"])

    st.markdown("---")
    st.markdown("#### 📋 Recommendations")
    focus_cols = st.columns(3)
    with focus_cols[0]:
        primary = summary["primary_focus"] or "Keep exploring fundamentals"
        st.markdown(
            f"""
            <div style="background:#0B0B0B; border:1px solid #CF3A4E; border-radius:12px; padding:1rem;">
                <p style="margin:0; color:#CF3A4E; font-weight:600;">Focus Next</p>
                <p style="margin:0.4rem 0 0 0; color:#FFFFFF;">{primary}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with focus_cols[1]:
        secondary = summary["secondary_focus"][:2]
        secondary_text = ", ".join(secondary) if secondary else "Tutor will add more soon."
        st.markdown(
            f"""
            <div style="background:#0B0B0B; border:1px solid #4A90E2; border-radius:12px; padding:1rem;">
                <p style="margin:0; color:#4A90E2; font-weight:600;">Also Explore</p>
                <p style="margin:0.4rem 0 0 0; color:#FFFFFF;">{secondary_text}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with focus_cols[2]:
        recent = summary["recent_topics"] or ["Take the quick assessment"]
        rec_html = "<br>".join(f"• {topic}" for topic in recent)
        st.markdown(
            f"""
            <div style="background:#0B0B0B; border:1px solid #FFD700; border-radius:12px; padding:1rem;">
                <p style="margin:0; color:#FFD700; font-weight:600;">Recent Topics</p>
                <p style="margin:0.4rem 0 0 0; color:#FFFFFF; font-size:0.9rem;">{rec_html}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("#### 🛡️ Keep the streak going")
    st.write(
        "Complete a quick 5-question assessment or chat with the tutor to "
        "earn more XP and unlock the next badge."
    )
    if st.button("⬅️ Back to roadmap", key="analytics_close_btn", use_container_width=True):
        st.session_state.show_analytics = False


