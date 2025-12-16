import streamlit as st
import os
import zipfile
import shutil
import main
import uuid


# def submit_task_ui():
#     st.title("📤 Submit Task")

#     prefix = st.session_state.task_form_uuid
#     disabled = st.session_state.task_submitted

#     q_dirs = [d for d in os.listdir("QuestionBank") if os.path.isdir(os.path.join("QuestionBank", d))]
#     if not q_dirs:
#         st.warning("No questions available. Please create a question first.")
#         return

#     selected_q = st.selectbox(
#         "Select Question",
#         q_dirs,
#         key=f"selq_{prefix}",
#         disabled=disabled,
#         width=300,
#     )

#     question_file = os.path.join("QuestionBank", selected_q, "question.txt")
#     answer_file = os.path.join("QuestionBank", selected_q, "answer_scheme.v")
#     modules_file = os.path.join("QuestionBank", selected_q, "modules.csv")

#     col1, col2 = st.columns(2)
#     files_exist = True

#     with col1:
#         if os.path.exists(question_file):
#             with open(question_file, "r") as f:
#                 st.text_area(
#                     "Question Text Preview",
#                     f.read(),
#                     height=300,
#                     disabled=True,
#                     key=f"qprev_{prefix}_{selected_q}",
#                 )
#         else:
#             st.warning("No question.txt found!")
#             files_exist = False

#     with col2:
#         if os.path.exists(answer_file):
#             with open(answer_file, "r") as f:
#                 st.text_area(
#                     "Answer Scheme Preview",
#                     f.read(),
#                     height=300,
#                     disabled=True,
#                     key=f"aprev_{prefix}_{selected_q}",
#                 )
#         else:
#             st.warning("No answer_scheme.v found!")
#             files_exist = False

#     if os.path.exists(modules_file):
#         with open(modules_file, "r") as f:
#             st.text_area(
#                 "Modules CSV Preview",
#                 f.read(),
#                 height=250,
#                 disabled=True,
#                 key=f"mprev_{prefix}_{selected_q}",
#             )
#     else:
#         st.warning("No modules.csv found!")
#         files_exist = False

#     task_name = st.text_input(
#         "Task Name",
#         key=f"taskname_{prefix}",
#         disabled=disabled,
#         width=300,
#     )
#     uploaded_zip = st.file_uploader(
#         "Upload ZIP File",
#         type=["zip"],
#         key=f"zip_{prefix}",
#         disabled=disabled,
#         width=400,
#     )

#     status_placeholder = st.empty()

#     if not st.session_state.task_submitted:
#         submit_clicked = st.button("📥 Submit Task")
#         if submit_clicked:
#             if not files_exist:
#                 st.error("Cannot submit: One or more required files are missing!\nPlease create new question.")
#             elif not task_name or not uploaded_zip:
#                 st.error("Please provide a task name and upload a ZIP file.")
#             else:
#                 st.session_state.task_submitted = True
#                 st.session_state.task_processed = False
#                 st.rerun()
#     else:
#         st.info("Task submitted. Processing...")

#     if st.session_state.task_submitted and not st.session_state.task_processed and uploaded_zip is not None:
#         st.session_state.task_processed = True

#         status_placeholder.info("Task received. Processing... Please wait.")

#         os.makedirs("SolutionBank", exist_ok=True)
#         os.makedirs("trash", exist_ok=True)

#         task_path = os.path.join("trash", f"{task_name}.zip")
#         with open(task_path, "wb") as f:
#             f.write(uploaded_zip.getbuffer())

#         extract_dir = os.path.join("trash", f"{task_name}_extracted")
#         os.makedirs(extract_dir, exist_ok=True)
#         with zipfile.ZipFile(task_path, "r") as zip_ref:
#             zip_ref.extractall(extract_dir)

#         def get_deepest_folder_with_files(path):
#             deepest_folder = path
#             max_depth = -1
#             for root, dirs, files in os.walk(path):
#                 if files:
#                     depth = root.count(os.sep)
#                     if depth > max_depth:
#                         max_depth = depth
#                         deepest_folder = root
#             return deepest_folder

#         deepest = get_deepest_folder_with_files(extract_dir)

#         dest_folder = f"SolutionBank/{task_name}"
#         os.makedirs(dest_folder, exist_ok=True)

#         for f_name in os.listdir(deepest):
#             src_file = os.path.join(deepest, f_name)
#             if os.path.isfile(src_file):
#                 shutil.copy(src_file, dest_folder)

#         def progress_callback(current, total):
#             status_placeholder.info(f"Processing file {current}/{total}")

#         try:
#             with st.spinner("Processing task... Please wait."):
#                 main.main(selected_q, task_name, progress_callback=progress_callback)
#             st.success(f"Evaluation complete. Results saved to Results/{selected_q}-{task_name}.xlsx")
#         except Exception as e:
#             st.error(f"Error during evaluation: {e}")

#     if st.session_state.task_processed and st.button("🔄 Clear / New Task"):
#         st.session_state.task_form_uuid = str(uuid.uuid4())
#         st.session_state.task_submitted = False
#         st.session_state.task_processed = False
#         st.rerun()

def submit_task_ui():
    st.title("📤 Submit Task")

    prefix = st.session_state.task_form_uuid
    disabled = st.session_state.task_submitted

    # --- Directories ---
    q_dirs = [d for d in os.listdir("QuestionBank") if os.path.isdir(os.path.join("QuestionBank", d))]
    if not q_dirs:
        st.warning("No questions available. Please create a question first.")
        return

    # --- Dropdown ---
    selected_q = st.selectbox(
        "Select Question",
        q_dirs,
        key=f"selq_{prefix}",
        disabled=disabled,
        width=300,
    )

    # --- Paths ---
    question_file = os.path.join("QuestionBank", selected_q, "question.txt")
    answer_file = os.path.join("QuestionBank", selected_q, "answer_scheme.v")
    modules_file = os.path.join("QuestionBank", selected_q, "modules.csv")
    module_codes_folder = os.path.join("QuestionBank", selected_q, "module_codes")

    # --- Preview / Warnings ---
    col1, col2 = st.columns(2)
    files_exist = True

    with col1:
        if os.path.exists(question_file):
            with open(question_file, "r") as f:
                st.text_area(
                    "Question Text Preview",
                    f.read(),
                    height=300,
                    disabled=True,
                    key=f"qprev_{prefix}_{selected_q}",
                )
        else:
            st.warning("No question.txt found!")
            files_exist = False

    with col2:
        if os.path.exists(answer_file):
            with open(answer_file, "r") as f:
                st.text_area(
                    "Answer Scheme Preview",
                    f.read(),
                    height=300,
                    disabled=True,
                    key=f"aprev_{prefix}_{selected_q}",
                )
        else:
            st.warning("No answer_scheme.v found!")
            files_exist = False

    if os.path.exists(modules_file):
        with open(modules_file, "r") as f:
            st.text_area(
                "Modules CSV Preview",
                f.read(),
                height=250,
                disabled=True,
                key=f"mprev_{prefix}_{selected_q}",
            )
    else:
        st.warning("No modules.csv found!")
        files_exist = False

    # --- Module codes (.v per module) preview + selection ---
    module_files = []
    if os.path.isdir(module_codes_folder):
        module_files = sorted(
            f for f in os.listdir(module_codes_folder) if f.endswith(".v")
        )
        if module_files:
            st.subheader("Module Codes (please select the modules to be evaluated)")
            for idx, fname in enumerate(module_files):
                # 2 per row
                if idx % 2 == 0:
                    cols = st.columns(2)
                col = cols[idx % 2]

                file_path = os.path.join(module_codes_folder, fname)
                try:
                    with open(file_path, "r") as f:
                        code_content = f.read()
                except Exception as e:
                    code_content = f"Error reading file: {e}"

                with col:
                    chk_key = f"modchk_{prefix}_{selected_q}_{fname}"
                    # checkbox with filename as label
                    st.checkbox(
                        fname,
                        key=chk_key,
                        disabled=disabled,
                    )
                    st.text_area(
                        "Preview",
                        code_content,
                        height=250,
                        disabled=True,
                        key=f"modcode_{prefix}_{selected_q}_{fname}",
                    )
        else:
            st.info("No .v module files found in module_codes folder.")
    else:
        st.info("No module_codes folder found for this question.")

    # Collect selected modules (strip .v)
    selected_modules = []
    for fname in module_files:
        chk_key = f"modchk_{prefix}_{selected_q}_{fname}"
        if st.session_state.get(chk_key, False):
            mod_name = os.path.splitext(fname)[0]
            selected_modules.append(mod_name)

    # --- Inputs ---
    task_name = st.text_input(
        "Task Name",
        key=f"taskname_{prefix}",
        disabled=disabled,
        width=300,
    )
    uploaded_zip = st.file_uploader(
        "Upload ZIP File",
        type=["zip"],
        key=f"zip_{prefix}",
        disabled=disabled,
        width=400,
    )

    # --- Placeholder for status ---
    status_placeholder = st.empty()

    # --- Submit button ---
    if not st.session_state.task_submitted:
        submit_clicked = st.button("📥 Submit Task")
        if submit_clicked:
            if not files_exist:
                st.error("Cannot submit: One or more required files are missing!\nPlease create new question.")
            elif not task_name or not uploaded_zip:
                st.error("Please provide a task name and upload a ZIP file.")
            elif module_files and not selected_modules:
                # Only enforce selection if module files actually exist
                st.error("Please select at least one module to evaluate.")
            else:
                st.session_state.task_submitted = True
                st.session_state.task_processed = False
                st.rerun()
    else:
        st.info("Task submitted. Processing...")

    # --- Processing block (runs only once per submission) ---
    if st.session_state.task_submitted and not st.session_state.task_processed and uploaded_zip is not None:
        st.session_state.task_processed = True  # mark as processed immediately

        status_placeholder.info("Task received. Processing... Please wait.")

        # Ensure directories
        os.makedirs("SolutionBank", exist_ok=True)
        os.makedirs("trash", exist_ok=True)

        # Save ZIP
        task_path = os.path.join("trash", f"{task_name}.zip")
        with open(task_path, "wb") as f:
            f.write(uploaded_zip.getbuffer())

        # Extract ZIP
        extract_dir = os.path.join("trash", f"{task_name}_extracted")
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(task_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # Copy files from deepest folder
        def get_deepest_folder_with_files(path):
            deepest_folder = path
            max_depth = -1
            for root, dirs, files in os.walk(path):
                if files:
                    depth = root.count(os.sep)
                    if depth > max_depth:
                        max_depth = depth
                        deepest_folder = root
            return deepest_folder

        deepest = get_deepest_folder_with_files(extract_dir)

        # Ensure SolutionBank folder for this task exists
        dest_folder = f"SolutionBank/{task_name}"
        os.makedirs(dest_folder, exist_ok=True)

        # Copy files
        for f_name in os.listdir(deepest):
            src_file = os.path.join(deepest, f_name)
            if os.path.isfile(src_file):
                shutil.copy(src_file, dest_folder)

        # Progress callback
        def progress_callback(current, total):
            status_placeholder.info(f"Processing file {current}/{total}")

        try:
            with st.spinner("Processing task... Please wait."):
                # You will need to update main.main signature for this:
                # def main(question_name, task_name, selected_modules, progress_callback=None)
                main.main(selected_q, task_name, selected_modules, progress_callback=progress_callback)
            st.success(f"Evaluation complete. Results saved to Results/{selected_q}-{task_name}.xlsx")
        except Exception as e:
            st.error(f"Error during evaluation: {e}")

    # --- Clear / New Task button ---
    if st.session_state.task_processed and st.button("🔄 Clear / New Task"):
        st.session_state.task_form_uuid = str(uuid.uuid4())  # new keys for widgets
        st.session_state.task_submitted = False
        st.session_state.task_processed = False
        st.rerun()
