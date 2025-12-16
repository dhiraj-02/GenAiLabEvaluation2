import streamlit as st
import os
import uuid
import main  

def create_question_ui():
    st.title("📝 Create Question")

    prefix = st.session_state.form_id
    disabled = st.session_state.question_submitted or st.session_state.question_created

    # --- Inputs ---
    question_name = st.text_input(
        "Question Name",
        key=f"{prefix}_question_name",
        disabled=disabled,
        width=300,
    )

    col1, col2 = st.columns(2)
    with col1:
        question_txt = st.text_area(
            "Question Text",
            height=300,
            key=f"{prefix}_question_txt",
            disabled=disabled,
        )
    with col2:
        answer_scheme = st.text_area(
            "Answer Scheme",
            height=300,
            key=f"{prefix}_answer_scheme",
            disabled=disabled,
        )

    num_modules = st.number_input(
        "Number of Modules",
        min_value=0,
        step=1,
        key=f"{prefix}_num_modules",
        disabled=disabled,
        width=200,
    )

    modules = []
    if num_modules > 0:
        st.subheader("Modules")
        for i in range(int(num_modules)):
            c1, c2 = st.columns([2, 1])
            with c1:
                modname = st.text_input(
                    f"Module Name {i+1}",
                    key=f"{prefix}_mod_{i}",
                    disabled=disabled,
                    width=300,
                )
            with c2:
                marks = st.number_input(
                    f"Max Marks {i+1}",
                    min_value=0.0,
                    step=0.5,
                    key=f"{prefix}_marks_{i}",
                    disabled=disabled,
                    width=200,
                )
            modules.append((modname, marks))

    status_placeholder = st.empty()

    # --- Create Question button & "creating" state ---
    if not st.session_state.question_created:
        if not st.session_state.question_submitted:
            if st.button("✅ Create Question", disabled=False):
                if not question_name or not question_txt or not answer_scheme or not modules:
                    st.error("Please fill all the required fields!")
                elif any(not mod or marks <= 0 for mod, marks in modules):
                    st.error("Each module must have a name and marks greater than 0!")
                else:
                    st.session_state.question_submitted = True
                    st.session_state.question_processed = False
                    st.rerun()
        else:
            st.info("Question submitted. Creating question...")

    # --- Processing block ---
    if (
        not st.session_state.question_created
        and st.session_state.question_submitted
        and not st.session_state.question_processed
    ):
        st.session_state.question_processed = True

        status_placeholder.info("Creating question files...")

        try:
            with st.spinner("Creating question... Please wait."):
                main.create_question_with_separate_modulefiles(answer_scheme, modules, question_name, question_txt)

            st.session_state.question_created = True
            st.success(f"Files for question '{question_name}' created successfully!")
        except Exception as e:
            st.session_state.question_submitted = False
            st.session_state.question_processed = False
            st.error(f"Error while creating question: {e}")

    # --- Clear / New Question ---
    if st.session_state.question_created:
        if st.button("🔄 Clear / New Question"):
            st.session_state.form_id = str(uuid.uuid4())
            st.session_state.question_created = False
            st.session_state.question_submitted = False
            st.session_state.question_processed = False
            st.rerun()
