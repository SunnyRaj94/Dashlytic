import streamlit as st
import os

import plotly.express as px
from backend.utils.session_manager import logout_user
from backend.data_sources.excel_reader import load_excel


def show_dashboard():
    st.title(f"Welcome, {st.session_state['username']}!")
    st.write("Upload an Excel file to view and analyze your data.")

    username = st.session_state["username"]
    user_dir = os.path.join("data", username)
    os.makedirs(user_dir, exist_ok=True)

    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls", "csv"])

    if uploaded_file:
        file_path = os.path.join(user_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File saved to {file_path}")

    uploaded_files = os.listdir(user_dir)
    if uploaded_files:
        selected_file = st.selectbox("Select a file to explore", uploaded_files)
        if selected_file:
            file_path = os.path.join(user_dir, selected_file)
            df = load_excel(file_path)

            if not df.empty:
                st.subheader("Data Preview")
                st.dataframe(df)

                numeric_cols = df.select_dtypes(include="number").columns.tolist()
                non_numeric_cols = df.select_dtypes(exclude="number").columns.tolist()

                if numeric_cols and non_numeric_cols:
                    st.subheader("Data Visualization")
                    x_axis = st.selectbox("Select X-axis", options=non_numeric_cols)
                    y_axis = st.selectbox("Select Y-axis", options=numeric_cols)
                    chart_type = st.radio("Chart Type", ["Bar", "Line"])

                    if x_axis and y_axis:
                        if chart_type == "Bar":
                            fig = px.bar(
                                df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}"
                            )
                        else:
                            fig = px.line(
                                df, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}"
                            )
                        st.plotly_chart(fig, use_container_width=True)

                st.subheader("Data Filters")
                for col in non_numeric_cols:
                    unique_vals = df[col].dropna().unique()
                    selected_vals = st.multiselect(
                        f"Filter by {col}", options=unique_vals, default=unique_vals
                    )
                    df = df[df[col].isin(selected_vals)]

                st.subheader("Filtered Data")
                st.dataframe(df)

    if st.button("Logout"):
        logout_user()
        st.rerun()
