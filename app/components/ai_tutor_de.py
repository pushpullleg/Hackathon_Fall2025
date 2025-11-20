"""
AI Tutor for Data Engineer Roadmap
----------------------------------

Provides a tutor page with:
- Greeting for Mukesh
- One-time 5-question assessment (roadmap-based MCQs)
- Level detection (4 levels)
- Topic recommendations
- Event logging for learning analytics
- Lightweight chat with an LLM focused on the Data Engineer roadmap
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any

import streamlit as st
from dotenv import load_dotenv

try:
    from openai import OpenAI
except Exception:  # pragma: no cover - OpenAI may not be installed in all envs
    OpenAI = None  # type: ignore

load_dotenv()

DEFAULT_CHAT_MODEL = "gpt-4o-mini"
RESPONSES_ONLY_PREFIXES = ("gpt-4.1", "o1", "o3")
PRACTICE_KEYWORDS = (
    "practice",
    "practiced",
    "practicing",
    "learn",
    "learned",
    "learning",
    "review",
    "reviewed",
    "studied",
    "study",
    "retain",
    "retention",
    "recap",
)
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


# ---------- Paths & persistence ----------

def _get_data_dir() -> str:
    """Return the directory where tutor analytics data is stored."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def _get_events_path() -> str:
    return os.path.join(_get_data_dir(), "tutor_events.json")


def _load_events() -> List[Dict[str, Any]]:
    """Load all tutor events from JSON; return empty list if none."""
    path = _get_events_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_events(events: List[Dict[str, Any]]) -> None:
    """Persist all tutor events to JSON."""
    path = _get_events_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)


def _log_event(event_type: str, user_id: str, payload: Dict[str, Any]) -> None:
    """Append a single analytics event."""
    events = _load_events()
    events.append(
        {
            "type": event_type,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data": payload,
        }
    )
    _save_events(events)


def _build_recent_practice_digest(
    messages: List[Dict[str, Any]], max_entries: int = 3
) -> str:
    """
    Build a short recap of recent practice-focused chat snippets.
    """
    if not messages:
        return (
            "I didn't spot specific practice highlights yet. Ask for a quick drill "
            "or share what you just practiced, then try again."
        )

    highlights: List[str] = []
    for message in reversed(messages):
        content = str(message.get("content", "")).strip()
        if not content:
            continue

        sentences = SENTENCE_SPLIT_RE.split(content)
        for sentence in sentences:
            cleaned = sentence.strip()
            if not cleaned:
                continue

            normalized = cleaned.lower()
            if any(keyword in normalized for keyword in PRACTICE_KEYWORDS):
                speaker = "You" if message.get("role") == "user" else "Tutor"
                highlights.append(f"- {speaker}: {cleaned}")
                if len(highlights) >= max_entries:
                    break
        if len(highlights) >= max_entries:
            break

    if highlights:
        return (
            "Here’s a quick retention recap based on your recent chat:\n"
            + "\n".join(highlights)
        )
    return (
        "I didn't spot specific practice highlights yet. Ask for a quick drill "
        "or share what you just practiced, then try again."
    )


# ---------- LLM helpers ----------

def _should_use_responses_api(model_name: str) -> bool:
    """Return True if the selected model only supports the Responses API."""
    if not model_name:
        return False
    normalized = model_name.lower()
    return any(normalized.startswith(prefix) for prefix in RESPONSES_ONLY_PREFIXES)


def _messages_to_responses_input(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert Chat Completions style messages to Responses API input format.
    """
    formatted = []
    for message in messages:
        role = message.get("role", "user")
        content = message.get("content", "")

        content_blocks: List[Dict[str, Any]] = []
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict):
                    block_text = block.get("text") or block.get("content") or ""
                else:
                    block_text = str(block)
                content_type = "input_text" if role != "assistant" else "output_text"
                content_blocks.append({"type": content_type, "text": str(block_text)})
        else:
            content_type = "input_text" if role != "assistant" else "output_text"
            content_blocks = [{"type": content_type, "text": str(content)}]

        formatted.append({"role": role, "content": content_blocks})
    return formatted


def _extract_text_from_responses(response: Any) -> str:
    """
    Safely pull assistant text from a Responses API result.
    """
    chunks: List[str] = []

    output = getattr(response, "output", None) or []
    for item in output:
        content_list = getattr(item, "content", None) or []
        for block in content_list:
            text_value = getattr(block, "text", None) or getattr(block, "value", None)
            if text_value:
                chunks.append(text_value)
    if chunks:
        return "\n".join(chunks).strip()

    if hasattr(response, "output_text"):
        output_text = getattr(response, "output_text")
        if isinstance(output_text, list):
            return "\n".join(output_text).strip()
        if isinstance(output_text, str):
            return output_text.strip()

    if hasattr(response, "model_dump"):
        data = response.model_dump()
        for item in data.get("output", []):
            for block in item.get("content", []):
                text_value = block.get("text") or block.get("value")
                if text_value:
                    chunks.append(text_value)
        if chunks:
            return "\n".join(chunks).strip()

    return ""


def _generate_llm_reply(client: Any, messages: List[Dict[str, Any]], temperature: float = 0.2) -> str:
    """
    Call OpenAI using either Chat Completions or Responses depending on model support.
    """
    model_name = os.getenv("OPENAI_CHAT_MODEL", DEFAULT_CHAT_MODEL)

    if _should_use_responses_api(model_name):
        response = client.responses.create(
            model=model_name,
            input=_messages_to_responses_input(messages),
            temperature=temperature,
        )
        text = _extract_text_from_responses(response)
        if text:
            return text
        # Fallback to ensure we always return something if parsing fails
        return "I generated a response but could not parse the text output."

    completion = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
    )
    return completion.choices[0].message.content


# ---------- Assessment definition ----------

def _get_questions() -> List[Dict[str, Any]]:
    """
    Return the fixed set of 5 roadmap-based MCQs.

    Each question maps to a pillar/topic from the Data Engineer roadmap.
    """
    return [
        {
            "id": "q1_python_basics",
            "pillar": "Foundations",
            "topic": "Core Skills - Python",
            "text": "In Python, what is the best way to iterate over a list of items with their index?",
            "options": [
                "Use a classic for-loop with range(len(items))",
                "Use enumerate(items) inside the for-loop",
                "Manually increment a counter variable inside the loop",
                "You cannot access index during iteration",
            ],
            "correct_index": 1,
            "difficulty": 1,
        },
        {
            "id": "q2_sql_joins",
            "pillar": "Storage & Databases",
            "topic": "Relational Databases - SQL",
            "text": "Which SQL JOIN returns all rows from the left table and matching rows from the right table?",
            "options": [
                "INNER JOIN",
                "LEFT JOIN (LEFT OUTER JOIN)",
                "RIGHT JOIN (RIGHT OUTER JOIN)",
                "FULL OUTER JOIN",
            ],
            "correct_index": 1,
            "difficulty": 1,
        },
        {
            "id": "q3_etl_elt",
            "pillar": "Data Ingestion & Pipelines",
            "topic": "Pipeline Fundamentals - ETL vs ELT",
            "text": "What is the main difference between ETL and ELT?",
            "options": [
                "ETL transforms data after loading it into the warehouse; ELT transforms before loading",
                "ETL transforms data before loading into the warehouse; ELT transforms after loading",
                "They are exactly the same",
                "ETL is only for batch, ELT only for streaming",
            ],
            "correct_index": 1,
            "difficulty": 2,
        },
        {
            "id": "q4_batch_streaming",
            "pillar": "Data Ingestion & Pipelines",
            "topic": "Ingestion Types - Batch vs Streaming",
            "text": "Which statement best describes streaming ingestion?",
            "options": [
                "Data is loaded once per day as a single bulk file",
                "Data is ingested as continuous events with low latency",
                "Data is copied manually by engineers",
                "Streaming ingestion does not support real-time analytics",
            ],
            "correct_index": 1,
            "difficulty": 2,
        },
        {
            "id": "q5_cloud_services",
            "pillar": "Big Data & Infrastructure",
            "topic": "Cloud Platforms - AWS / Azure / GCP",
            "text": "In a typical cloud architecture, which service is most appropriate for object storage?",
            "options": [
                "Amazon S3 or Azure Blob Storage",
                "Managed relational database (e.g., Amazon RDS)",
                "Virtual machines (EC2, VM, Compute Engine)",
                "Serverless compute (AWS Lambda, Azure Functions)",
            ],
            "correct_index": 0,
            "difficulty": 2,
        },
    ]


# ---------- Utility: compute level & summary ----------

def _compute_level_and_summary(answers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Given a list of answer dicts with 'correct' flags, compute:
    - score
    - level (1-4)
    - per-pillar accuracy
    - recommended topics
    """
    if not answers:
        return {
            "score": 0,
            "level": 1,
            "pillar_stats": {},
            "primary_recommendation": None,
            "secondary_recommendations": [],
        }

    total = len(answers)
    correct = sum(1 for a in answers if a.get("correct"))
    score = correct / total

    # Simple mapping: 0–0.25 -> 1, 0.25–0.5 -> 2, 0.5–0.75 -> 3, >0.75 -> 4
    if score <= 0.25:
        level = 1
    elif score <= 0.5:
        level = 2
    elif score <= 0.75:
        level = 3
    else:
        level = 4

    # Per-pillar stats
    pillar_stats: Dict[str, Dict[str, int]] = {}
    for a in answers:
        pillar = a.get("pillar", "Unknown")
        if pillar not in pillar_stats:
            pillar_stats[pillar] = {"total": 0, "correct": 0}
        pillar_stats[pillar]["total"] += 1
        if a.get("correct"):
            pillar_stats[pillar]["correct"] += 1

    # Compute weakest pillar(s) as recommendations
    weakest_pillar = None
    weakest_accuracy = 1.1
    for pillar, stats in pillar_stats.items():
        acc = stats["correct"] / stats["total"]
        if acc < weakest_accuracy:
            weakest_accuracy = acc
            weakest_pillar = pillar

    primary = None
    secondary: List[str] = []
    if weakest_pillar:
        primary = weakest_pillar
        # Recommend all pillars sorted by increasing accuracy
        sorted_pillars = sorted(
            pillar_stats.items(),
            key=lambda kv: kv[1]["correct"] / kv[1]["total"],
        )
        for pillar, _ in sorted_pillars:
            if pillar != weakest_pillar:
                secondary.append(pillar)

    return {
        "score": score,
        "level": level,
        "pillar_stats": pillar_stats,
        "primary_recommendation": primary,
        "secondary_recommendations": secondary,
    }


def get_latest_summary(user_id: str) -> Dict[str, Any]:
    """
    Public helper used by the main Streamlit app to show tutor insights.

    Returns a dict with 'level', 'last_assessed_at', 'primary_recommendation',
    'secondary_recommendations' if available.
    """
    events = _load_events()
    latest: Dict[str, Any] = {}
    for ev in events:
        if ev.get("user_id") != user_id:
            continue
        if ev.get("type") == "tutor_assessment_completed":
            latest = ev

    if not latest:
        return {}

    data = latest.get("data", {})
    return {
        "level": data.get("level"),
        "last_assessed_at": latest.get("timestamp"),
        "primary_recommendation": data.get("primary_recommendation"),
        "secondary_recommendations": data.get("secondary_recommendations", []),
    }


# ---------- Streamlit tutor panel ----------

def _init_tutor_state():
    """Initialize tutor-related session state variables."""
    if "tutor_stage" not in st.session_state:
        st.session_state.tutor_stage = "intro"  # intro, question, summary
    if "tutor_question_index" not in st.session_state:
        st.session_state.tutor_question_index = 0
    if "tutor_answers" not in st.session_state:
        st.session_state.tutor_answers = []
    if "tutor_current_choice" not in st.session_state:
        st.session_state.tutor_current_choice = None
    if "tutor_chat_messages" not in st.session_state:
        st.session_state.tutor_chat_messages = []
    if "tutor_show_practice_summary" not in st.session_state:
        st.session_state.tutor_show_practice_summary = False
    if "tutor_last_digest_signature" not in st.session_state:
        st.session_state.tutor_last_digest_signature = None
    if "tutor_llm_client" not in st.session_state:
        # Lazily create an OpenAI client if available
        if OpenAI is not None:
            try:
                st.session_state.tutor_llm_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            except Exception:
                st.session_state.tutor_llm_client = None
        else:
            st.session_state.tutor_llm_client = None


def render_ai_tutor_panel(user_name: str = "Mukesh", user_id: str = "Mukesh"):
    """
    Render the AI Tutor panel content.

    This should be called inside a right-side column on the roadmap page.
    """
    _init_tutor_state()
    questions = _get_questions()

    st.markdown(
        """
        <div style="background-color: #050505; border-radius: 12px; padding: 1rem 1.25rem; border: 1px solid #222;">
            <h3 style="color: #FFFFFF; margin: 0 0 0.5rem 0;">🤖 Adaptive AI Tutor</h3>
            <p style="color: #CCCCCC; margin: 0 0 1rem 0; font-size: 0.9rem;">
                Hi {name}, I'm your tutor for the <span style="color: #CF3A4E;">Data Engineer Roadmap</span>.
                I'll ask a few quick questions to estimate your level and then suggest what to learn next.
            </p>
        </div>
        """.format(
            name=user_name
        ),
        unsafe_allow_html=True,
    )

    # Check if user already has a completed assessment
    summary = get_latest_summary(user_id)
    has_profile = bool(summary)

    if st.session_state.tutor_stage == "intro":
        _render_intro_stage(has_profile, summary)
    elif st.session_state.tutor_stage == "question":
        _render_question_stage(user_id, questions)
    elif st.session_state.tutor_stage == "summary":
        _render_summary_stage(user_id, summary_override=None)

    # Chat section is always available under the assessment / summary
    _render_chat_section(user_id, user_name=user_name)


def _render_intro_stage(has_profile: bool, summary: Dict[str, Any]):
    """Render first-time vs returning-user intro."""
    st.markdown("---")
    LEVEL_LABELS = {
        1: "Beginner",
        2: "Emerging",
        3: "Proficient",
        4: "Advanced",
    }

    if not has_profile:
        st.markdown(
            """
            <p style="color: #FFFFFF; font-weight: 600; margin-bottom: 0.5rem;">
                First time here? Let's run a quick 5-question check-up.
            </p>
            <p style="color: #AAAAAA; font-size: 0.9rem; margin-bottom: 0.75rem;">
                It will help me understand your current skills and customize your roadmap.
            </p>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Start Assessment", key="tutor_start_assessment", use_container_width=True):
            st.session_state.tutor_stage = "question"
            st.session_state.tutor_question_index = 0
            st.session_state.tutor_answers = []
            st.session_state.tutor_current_choice = None
    else:
        level = summary.get("level")
        level_label = LEVEL_LABELS.get(level, "")
        primary = summary.get("primary_recommendation")
        secondary = summary.get("secondary_recommendations", [])
        st.markdown(
            f"""
            <p style="color: #FFFFFF; font-weight: 600; margin-bottom: 0.5rem;">
                Welcome back! Your current Data Engineer level is
                <span style="color:#CF3A4E;">L{level} – {level_label}</span>.
            </p>
            """,
            unsafe_allow_html=True,
        )
        if primary:
            sec_text = ", ".join(secondary) if secondary else "None yet"
            st.markdown(
                f"""
                <div style="background-color:#111; border-radius:8px; padding:0.75rem; border:1px solid #222; margin-bottom:0.75rem;">
                    <p style="color:#CCCCCC; font-size:0.85rem; margin:0;">
                        <strong>Focus next:</strong> {primary}<br>
                        <strong>Also explore:</strong> {sec_text}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Update my level", key="tutor_retake", use_container_width=True):
                st.session_state.tutor_stage = "question"
                st.session_state.tutor_question_index = 0
                st.session_state.tutor_answers = []
                st.session_state.tutor_current_choice = None
        with col2:
            if st.button(
                "Practice & retention",
                key="tutor_practice_retention",
                use_container_width=True,
            ):
                st.session_state.tutor_show_practice_summary = True


def _render_question_stage(user_id: str, questions: List[Dict[str, Any]]):
    """Render the current question and handle navigation."""
    idx = st.session_state.tutor_question_index
    question = questions[idx]

    st.markdown("---")
    st.markdown(
        f"""
        <p style="color:#AAAAAA; font-size:0.85rem; margin-bottom:0.25rem;">
            Question {idx + 1} of {len(questions)}
        </p>
        <p style="color:#FFFFFF; font-weight:600; margin-bottom:0.5rem;">
            {question['text']}
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Options as radio buttons
    choice = st.radio(
        "Select the best answer:",
        options=list(range(len(question["options"]))),
        format_func=lambda i: question["options"][i],
        index=st.session_state.tutor_current_choice
        if st.session_state.tutor_current_choice is not None
        else 0,
        key=f"tutor_q_{idx}",
    )
    st.session_state.tutor_current_choice = choice

    col_back, col_spacer, col_next = st.columns([1, 4, 1])
    with col_back:
        if st.button("← Back", key=f"tutor_back_{idx}", use_container_width=True) and idx > 0:
            # Go back to previous question
            st.session_state.tutor_question_index -= 1
            # Remove last answer
            if st.session_state.tutor_answers:
                st.session_state.tutor_answers.pop()
            st.session_state.tutor_current_choice = None

    with col_next:
        label = "Next →" if idx < len(questions) - 1 else "Finish ✓"
        if st.button(label, key=f"tutor_next_{idx}", use_container_width=True):
            # Save answer
            correct_index = question["correct_index"]
            is_correct = choice == correct_index
            answer_record = {
                "question_id": question["id"],
                "pillar": question["pillar"],
                "topic": question["topic"],
                "selected_index": int(choice),
                "correct_index": correct_index,
                "correct": bool(is_correct),
            }
            st.session_state.tutor_answers.append(answer_record)

            _log_event(
                "tutor_question_answered",
                user_id,
                {
                    **answer_record,
                    "difficulty": question["difficulty"],
                },
            )

            if idx < len(questions) - 1:
                st.session_state.tutor_question_index += 1
                st.session_state.tutor_current_choice = None
            else:
                # Completed all questions -> compute summary
                summary = _compute_level_and_summary(st.session_state.tutor_answers)
                _log_event(
                    "tutor_assessment_completed",
                    user_id,
                    {
                        "level": summary["level"],
                        "score": summary["score"],
                        "pillar_stats": summary["pillar_stats"],
                        "primary_recommendation": summary["primary_recommendation"],
                        "secondary_recommendations": summary["secondary_recommendations"],
                    },
                )
                st.session_state.tutor_stage = "summary"


def _render_summary_stage(user_id: str, summary_override: Dict[str, Any] = None):
    """Render summary based on latest assessment."""
    st.markdown("---")
    LEVEL_LABELS = {
        1: "Beginner",
        2: "Emerging",
        3: "Proficient",
        4: "Advanced",
    }

    summary = summary_override or get_latest_summary(user_id)
    if not summary:
        st.write("No summary available yet.")
        return

    level = summary.get("level", 1)
    level_label = LEVEL_LABELS.get(level, "")
    primary = summary.get("primary_recommendation")
    secondary = summary.get("secondary_recommendations", [])

    st.markdown(
        f"""
        <p style="color:#FFFFFF; font-weight:600; margin-bottom:0.5rem;">
            Great job! Your current Data Engineer level is
            <span style="color:#CF3A4E;">L{level} – {level_label}</span>.
        </p>
        """,
        unsafe_allow_html=True,
    )

    if primary:
        sec_text = ", ".join(secondary) if secondary else "None yet"
        st.markdown(
            f"""
            <div style="background-color:#111; border-radius:8px; padding:0.75rem; border:1px solid #222; margin-bottom:0.75rem;">
                <p style="color:#CCCCCC; font-size:0.85rem; margin:0;">
                    <strong>Focus next:</strong> {primary}<br>
                    <strong>Also explore:</strong> {sec_text}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button("Close tutor", key="tutor_close", use_container_width=True):
        # Reset stage so next open shows summary quickly
        st.session_state.tutor_stage = "intro"
        st.session_state.show_ai_tutor = False


def _render_chat_section(user_id: str, user_name: str = "Student") -> None:
    """Render a simple chat interface with the AI tutor."""
    st.markdown("---")
    st.markdown(
        """
        <p style="color:#FFFFFF; font-weight:600; margin-bottom:0.5rem;">
            Chat with your tutor
        </p>
        <p style="color:#AAAAAA; font-size:0.85rem; margin-bottom:0.5rem;">
            Ask questions about the roadmap, topics, or your next steps.
        </p>
        """,
        unsafe_allow_html=True,
    )

    user_input = st.chat_input("Type your question for the tutor...")

    if st.session_state.get("tutor_show_practice_summary"):
        existing_messages = list(st.session_state.tutor_chat_messages)
        digest = _build_recent_practice_digest(existing_messages)
        current_signature = (digest, len(existing_messages))
        last_signature = st.session_state.get("tutor_last_digest_signature")
        if current_signature != last_signature:
            summary_msg = {"role": "assistant", "content": digest}
            st.session_state.tutor_chat_messages.append(summary_msg)
            _log_event("tutor_chat_message", user_id, summary_msg)
            st.session_state.tutor_last_digest_signature = current_signature
        st.session_state.tutor_show_practice_summary = False

    # Show chat history (existing messages)
    for msg in st.session_state.tutor_chat_messages:
        role = msg.get("role", "assistant")
        with st.chat_message(role):
            st.markdown(msg.get("content", ""))
    if user_input:
        # Log user message
        st.session_state.tutor_chat_messages.append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user"):
            st.markdown(user_input)
        _log_event(
            "tutor_chat_message",
            user_id,
            {"role": "user", "content": user_input},
        )

        # Generate tutor response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                client = st.session_state.tutor_llm_client
                if client is not None:
                    try:
                        # Lightweight LLM call focused on DE roadmap topics
                        system_prompt = (
                            "You are an Adaptive AI Tutor for Data Engineers. "
                            "Focus ONLY on data engineering topics such as Python, SQL, "
                            "data storage, data pipelines, batch vs streaming, cloud "
                            "services, governance and testing. "
                            "Explain concepts clearly and concisely using step-by-step "
                            "reasoning when helpful. Do NOT ask quiz questions unless "
                            "the user explicitly requests practice questions."
                        )
                        chat_history = [
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.tutor_chat_messages[-6:]
                        ]
                        messages = [{"role": "system", "content": system_prompt}] + chat_history
                        response = _generate_llm_reply(client, messages)
                    except Exception as exc:
                        st.warning(f"LLM call failed: {exc}")
                        response = (
                            "I'm having trouble contacting the full AI service right now, "
                            "but conceptually: I am your Data Engineer tutor. Ask me about "
                            "storage, pipelines, SQL, or cloud and I'll guide you based on "
                            "the roadmap."
                        )
                else:
                    response = (
                        "I don't have direct access to the LLM in this environment, but "
                        "I'm your Data Engineer tutor. Use the roadmap and assessment "
                        "above as your guide, and we can still talk through concepts."
                    )
                response = response.strip()
                if user_name and user_name.lower() not in response.lower():
                    response = f"{user_name}, {response}"
                st.markdown(response)
            st.session_state.tutor_chat_messages.append(
                {"role": "assistant", "content": response}
            )
            _log_event(
                "tutor_chat_message",
                user_id,
                {"role": "assistant", "content": response},
            )


