import streamlit as st


def display_data(df):
    st.data_editor(
        df,
        column_config={
            "SECTOR_LONGNAME": st.column_config.TextColumn(
                "SECTORS"
            ),
            "HOLDING_RATIO": st.column_config.ProgressColumn(
                "RATIO (PERCENTAGE)",
                format='%f%%',
                min_value=-100,

                max_value=100,
            ),
        },
        hide_index=True,
    )
