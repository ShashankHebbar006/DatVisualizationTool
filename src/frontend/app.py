import os
import sys
import uuid
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
import plotly.graph_objects as go
import requests
load_dotenv()

base_path = os.path.basename(__file__)
abs_path = os.path.abspath(__file__)
dir_name = os.path.dirname(__file__)
root_dir = os.path.dirname(os.path.dirname(abs_path))

print(base_path)
print(abs_path)
print(dir_name)
print(root_dir)

uploaded_files = os.path.join(root_dir, "uploaded_files")
plots = os.path.join(root_dir, "plots")

# ----------------------------------------------
#       Remove cached files/session state
# ----------------------------------------------

if st.button("Reset"):
    st.session_state.clear()

    # Clear all uploaded files
    if os.path.exists(uploaded_files):
        for file in os.listdir(uploaded_files):
            os.remove(os.path.join(uploaded_files, file))
        os.rmdir(uploaded_files)

    # Clear all generated plots
    if os.path.exists(plots):
        for file in os.listdir(plots):
            os.remove(os.path.join(plots, file))
        os.rmdir(plots)

st.title("Data Visualization Tool")
base_url = os.getenv("BACKEND_URL")

# -------------------------------
#       File upload logic
# -------------------------------

uploaded_file = st.file_uploader(
    "Upload data",
    accept_multiple_files=True,
    type="csv"
)

if uploaded_file and "filename" not in st.session_state:
    filename = f"{uploaded_files}/{uuid.uuid4()}.csv"
    os.makedirs(uploaded_files, exist_ok=True)
    try:
        with open(filename, "wb") as f:
            f.write(uploaded_file[0].getvalue())

        st.session_state["filename"] = filename
        st.success("File uploaded successfully!")
    except Exception as e:
        st.write(f"Error uploading file: {e}")

# Stop until file uploaded
if "filename" not in st.session_state:
    st.stop()

filename = st.session_state["filename"]

# -----------------------------------
#       Generate summary logic
# -----------------------------------

if st.button("Get Summary") or "summary" in st.session_state:
    if "summary" not in st.session_state:
        resp = requests.post(f"{base_url}/get_summary", params={"filename": filename})
        st.session_state["summary"] = resp.json()

    summary = st.session_state["summary"]

    with st.expander("Summary"):
        st.json(summary)

# Stop until summary is present
if "summary" not in st.session_state:
    st.stop()

summary = st.session_state["summary"]

# -----------------------------------
#       Select plot logic
# -----------------------------------

with st.sidebar:

    # Plot selection
    selected_plot = st.selectbox(
        "Select plot type",
        ["Scatter", "Line", "Bar", "Histogram", "Heatmap"],
        placeholder="Select plot type",
        index=None
    )

    # Early stop if no plot selected yet
    if not selected_plot:
        st.stop()

    # Determine required input columns
    if selected_plot in ["Scatter", "Line"]:
        required_fields = ["x", "y"]
        headers = st.session_state['summary']['Num Cols']

    elif selected_plot == "Bar":
        required_fields = ["x"]
        headers = st.session_state['summary']['Cat Cols'] + st.session_state['summary']['Num Cols']

    elif selected_plot == "Heatmap":
        required_fields = []  # none needed
        headers = st.session_state['summary']['Num Cols']

    # Dynamic UI for required fields
    x_col = y_col = None

    if "x" in required_fields:
        x_col = st.selectbox(
            "Select X-axis",
            headers,
            placeholder="Select a column",
            index=None
        )

    if "y" in required_fields:
        y_col = st.selectbox(
            "Select Y-axis",
            headers,
            placeholder="Select a column",
            index=None
        )

    # Visualize button
    visualize = st.button("Visualize")

# -----------------------------------
#       Visualisation logic
# -----------------------------------

if selected_plot:
    st.write(f"Plotting: **{selected_plot}**")

    if visualize:

        # Validate required fields
        if "x" in required_fields and not x_col:
            st.warning("Please select X-axis")
            st.stop()

        if "y" in required_fields and not y_col:
            st.warning("Please select Y-axis")
            st.stop()

        # Build params for API
        params = {
            "filename": filename,
            "selected_plot": selected_plot
        }

        if x_col:
            params["x"] = x_col
        if y_col:
            params["y"] = y_col

        # Call backend API
        response = requests.post(f"{base_url}/visualize", params=params)

        if response.status_code == 200:
            img_path = response.json()
            st.image(img_path, use_container_width=True)
            st.success("Visualization generated successfully!")
        else:
            st.error("Backend Error: " + response.text)
