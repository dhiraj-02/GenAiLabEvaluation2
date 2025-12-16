import streamlit as st
import uuid

from ui.create_question import create_question_ui
from ui.submit_task import submit_task_ui
from ui.view_results import view_results  

st.set_page_config(page_title="GenAI Lab Evaluation", layout="wide")

# --- Initialize session state ---
if "task_submitted" not in st.session_state:
    st.session_state.task_submitted = False
if "task_processed" not in st.session_state:
    st.session_state.task_processed = False
if "task_form_uuid" not in st.session_state:
    st.session_state.task_form_uuid = str(uuid.uuid4())
if "form_id" not in st.session_state:
    st.session_state.form_id = str(uuid.uuid4())
if "question_created" not in st.session_state:
    st.session_state.question_created = False
if "question_submitted" not in st.session_state:
    st.session_state.question_submitted = False
if "question_processed" not in st.session_state:
    st.session_state.question_processed = False
if "menu" not in st.session_state:
    st.session_state.menu = "📤 Submit Task"  # default

# --- Sidebar navigation ---
st.sidebar.markdown("## Navigation")

menu = st.sidebar.radio(
    "Go to:",
    ["📤 Submit Task", "➕ Create Question", "🔍 View Results"],
    index=0,
    key="sidebar_menu",
    disabled=st.session_state.task_submitted and not st.session_state.task_processed,
)

st.session_state.menu = menu

# --- Routing ---
if menu == "➕ Create Question":
    create_question_ui()
elif menu == "📤 Submit Task":
    submit_task_ui()
# elif menu == "🔍 View Results":
#     view_results()
