import streamlit as st
import os
import pandas as pd

def view_results():
    st.title("🔍 View Results")
    RESULTS_DIR = "Results"

    if not os.path.exists(RESULTS_DIR):
        st.warning(f"Directory '{RESULTS_DIR}' does not exist.")
        return

    files = [f for f in os.listdir(RESULTS_DIR) if f.endswith(".xlsx")]
    if not files:
        st.info("No Excel files found in the results directory.")
        return

    selected_file = st.selectbox("Select a results file:", files)

    if selected_file:
        file_path = os.path.join(RESULTS_DIR, selected_file)
        try:
            df = pd.read_excel(file_path)
            st.write(f"Showing contents of **{selected_file}**")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Failed to read file: {e}")
