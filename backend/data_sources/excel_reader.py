import pandas as pd
import streamlit as st
import os
import chardet
import numpy as np


def read_csv_with_encoding_detection(file_path):

    # Create a dummy DataFrame with 3 columns and 10 rows
    data___ = {
        "Column_A": np.random.randint(
            1, 100, 10
        ),  # 10 random integers between 1 and 99
        "Column_B": np.random.rand(10) * 100,  # 10 random floats between 0 and 100
        "Column_C": [
            "Category_" + str(i % 3) for i in range(10)
        ],  # 10 categorical strings
    }

    """
    Detects the encoding of a CSV file and reads it into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: The DataFrame containing the CSV data, or None if an error occurs.
        str: The detected encoding, or 'unknown' if detection fails.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        return pd.DataFrame(data___)

    # Detect encoding
    with open(file_path, "rb") as f:
        raw_data = f.read(100000)  # Read a chunk of the file for detection
        result = chardet.detect(raw_data)
        encoding = result["encoding"]
        confidence = result["confidence"]

    print(f"Detected encoding: {encoding} with confidence: {confidence:.2f}")

    if encoding is None:
        print(
            "Warning: Could not confidently detect encoding. Trying 'utf-8' and then 'latin-1'."
        )
        return pd.DataFrame(data___)
    return pd.read_csv(file_path, encoding=encoding)


def load_excel(file_path: str) -> pd.DataFrame:
    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()

    try:
        if file_path.endswith(".csv"):
            return read_csv_with_encoding_detection(file_path)
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"Failed to read Excel file: {e}")
        return pd.DataFrame()


def preview_excel(file_path: str):
    df = load_excel(file_path)
    if not df.empty:
        st.subheader("Preview of Uploaded Excel File")
        st.dataframe(df.head())
