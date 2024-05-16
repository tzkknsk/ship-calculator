from io import BytesIO
from datetime import datetime

import pandas as pd
import streamlit as st

from utils import calculate_ship


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


st.title("SHIP Calculator App")

with st.container():

    # Upload data file for analysis
    uploaded_file = st.file_uploader(
        "Upload data file for calculation of SHIP",
        type="xlsx"
    )
    if uploaded_file is not None:

        # Load data
        df_input_matrix = pd.read_excel(uploaded_file, header=None, index_col=None)

        # Display data
        st.header("Input Data")
        st.dataframe(df_input_matrix)

        calc_bottom = st.button("Calculate SHIP")

        if calc_bottom:

            # Calculate SHIP
            matrix = df_input_matrix.to_numpy()
            ship, diff_matrix = calculate_ship(matrix)

            # Display SHIP
            df_diff_matrix = pd.DataFrame(diff_matrix)
            df_ship = pd.DataFrame({"SHIP": [ship]})

            # Display difference matrix
            st.header("Results")
            st.dataframe(df_diff_matrix)
            st.dataframe(df_ship)

            # Download results
            df_dict = {
                "Input Matrix": df_input_matrix,
                "Difference Matrix": df_diff_matrix,
                "SHIP": df_ship
            }

            output = to_excel(df_dict)
            st.download_button(
                label="Download Results",
                data=output,
                file_name=f"result_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
