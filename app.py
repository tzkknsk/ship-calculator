from io import BytesIO
from datetime import datetime

import pandas as pd
import streamlit as st

from utils import calculate_ship

# Set page config
st.set_page_config(layout="wide")


def to_excel(
        df_dict: dict[str, pd.DataFrame]
) -> BytesIO:

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        for sheet_name, df in df_dict.items():

            df.to_excel(
                writer,
                sheet_name=sheet_name,
                index=False,
                header=True if sheet_name == "SHIP" else False
            )

    output.seek(0)
    return output


# Session State
save_state_variables = [
    "uploaded_file",
    "df_input_matrix",
    "matrix",
    "ship",
    "calc_bottom",
    "diff_matrix",
    "df_diff_matrix",
    "df_ship",
]
for var in save_state_variables:
    if var not in st.session_state:
        st.session_state[var] = None

ss = st.session_state

st.title("SHIP Calculator App")

tab1, tab2 = st.tabs(["Upload data", "Download sample file to upload"])

with tab1:
    # Upload data file for analysis
    ss.uploaded_file = st.file_uploader(
        "Upload data file for calculation of SHIP",
        type="xlsx"
    )

with tab2:
    sample = pd.read_excel(
        "data/sample_input.xlsx",
        header=None,
        index_col=None
    )
    st.download_button(
        label="Download Sample File",
        data=to_excel({"sample input": sample}),
        file_name="sample_input.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


if ss.uploaded_file is not None:

    # Load data
    ss.df_input_matrix = pd.read_excel(
        ss.uploaded_file,
        header=None,
        index_col=None
    )

    # Display data
    st.header("Input Data")
    st.dataframe(ss.df_input_matrix)

    ss.calc_bottom = st.button("Calculate SHIP")

    if ss.calc_bottom:

        # Calculate SHIP
        ss.matrix = ss.df_input_matrix.to_numpy()
        ss.ship, ss.diff_matrix = calculate_ship(ss.matrix)

        # Display SHIP
        ss.df_diff_matrix = pd.DataFrame(ss.diff_matrix)
        ss.df_ship = pd.DataFrame({"SHIP": [ss.ship]})

        # Display difference matrix
        st.header("Results")
        st.dataframe(ss.df_diff_matrix)
        st.dataframe(ss.df_ship)

        # Download results
        df_dict = {
            "Input Matrix": ss.df_input_matrix,
            "Difference Matrix": ss.df_diff_matrix,
            "SHIP": ss.df_ship
        }

        output = to_excel(df_dict)
        st.download_button(
            label="Download Results",
            data=output,
            file_name=f"calculated_SHIP_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
