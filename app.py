import streamlit as st
import pandas as pd
from nl_to_sql import generate_sql, fix_sql
from query_executor import execute_query
from chart_helper import suggest_chart

MAX_RETRIES = 3

st.set_page_config(page_title="NLP to SQL", page_icon="🤖", layout="wide")

# ---------------- Custom styling ----------------
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        max-width: 900px;
    }
    .app-title {
        font-size: 2.1rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .app-subtitle {
        color: #8a8a8a;
        margin-bottom: 1.5rem;
    }
    .chat-bubble-user {
        background-color: #2b6cb0;
        color: white;
        padding: 12px 16px;
        border-radius: 14px 14px 2px 14px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
    }
    .chat-bubble-assistant {
        background-color: #f0f2f6;
        color: #111;
        padding: 12px 16px;
        border-radius: 14px 14px 14px 2px;
        margin: 10px 0;
        max-width: 90%;
    }
    div[data-testid="stTextInput"] input {
        border-radius: 20px;
        padding: 10px 16px;
    }
    .stButton button {
        border-radius: 20px;
    }
    .example-btn button {
        text-align: left;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- Session state setup ----------------
if "question" not in st.session_state:
    st.session_state.question = ""
if "submit" not in st.session_state:
    st.session_state.submit = False
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {question, sql, result}


def submit_question():
    st.session_state.submit = True


def clear_question():
    st.session_state.question = ""
    st.session_state.submit = False


def use_example(example_text):
    st.session_state.question = example_text
    st.session_state.submit = True  # now auto-runs instead of just filling the box


# ---------------- Sidebar: example queries ----------------
with st.sidebar:
    st.header("💡 Try an example")
    examples = [
        "Show me all customers from Chicago",
        "What is the total sales for each category?",
        "Which region has the highest profit?",
        "Show me the top 5 products by quantity sold",
        "How many orders had late delivery in each shipping type?"
    ]
    for i, ex in enumerate(examples):
        st.button(ex, key=f"ex_{i}", on_click=use_example, args=(ex,), use_container_width=True)

    st.divider()
    if st.button("🗑️ Clear chat history", use_container_width=True):
        st.session_state.history = []

# ---------------- Main title ----------------
st.markdown('<div class="app-title">🤖 NLP to SQL</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Ask a question in plain English — get real SQL and real answers.</div>', unsafe_allow_html=True)

# ---------------- Input row: text box + clear (X) button ----------------
col1, col2 = st.columns([9, 1])
with col1:
    st.text_input(
        "Your question",
        key="question",
        on_change=submit_question,
        placeholder="e.g. Which region has the highest profit?",
        label_visibility="collapsed"
    )
with col2:
    st.button("✕", on_click=clear_question, use_container_width=True)

# ---------------- Run Query button (below the input) ----------------
st.button("▶ Run Query", on_click=submit_question, use_container_width=True)

# ---------------- Process the question ----------------
if st.session_state.submit and st.session_state.question.strip():
    question = st.session_state.question

    with st.spinner("Thinking..."):
        sql = generate_sql(question)
        result = execute_query(sql)

        attempt = 1
        while isinstance(result, str) and result.startswith("ERROR") and attempt < MAX_RETRIES:
            attempt += 1
            sql = fix_sql(question, sql, result)
            result = execute_query(sql)

    st.session_state.history.append({"question": question, "sql": sql, "result": result})
    st.session_state.submit = False  # reset so it doesn't re-run on next interaction

# ---------------- Display conversation history (newest first) ----------------
for turn in reversed(st.session_state.history):
    st.markdown(f'<div class="chat-bubble-user">{turn["question"]}</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="chat-bubble-assistant">', unsafe_allow_html=True)
        st.code(turn["sql"], language="sql")

        if isinstance(turn["result"], str):
            st.error(turn["result"])
        else:
            st.dataframe(turn["result"], use_container_width=True)

            fig = suggest_chart(turn["result"])
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)