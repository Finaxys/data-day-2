import streamlit as st
import pandas as pd

st.set_page_config(page_title='Portfolio Performance',
                   page_icon=':bar_chart:',
                   layout='wide')

st.title('Portfolio Performance')

# Read datas from Excel file
datas = pd.read_csv('SILVER_HOLDING_RATIO.csv')

# Display RAW Data
st.subheader('Raw data')
st.write(datas)

# Split the screen in 3 columns
left_column, center_column, right_column = st.columns(3)

# Data used to display orderbook sorted by holding score
data_ob = datas.filter(['ORDERBOOK', 'OB_HOLDING']).groupby('OB_HOLDING').sum().sort_values('OB_HOLDING', ascending=False)

with left_column:
    st.subheader('Instruments Allocation')
    # getting max share for nice progress bar display
    max_share = datas['OB_HOLDING'].max()
    st.dataframe(data_ob,
                 column_config={
                     "ORDERBOOK": "Instrument",
                     "OB_HOLDING": st.column_config.ProgressColumn(
                         "Shares", max_value=max_share, format='%d'
                     )})

# Data is used to display top and bottom agent sorted by holding score
data_holding = datas.filter(['AGENTNAME', 'HOLDING']).groupby('AGENTNAME').mean().sort_values('HOLDING', ascending=False)

with center_column:
    st.subheader('Top 3 Performer')
    # Display top 3 ESG instruments sorted by ESG score
    st.write(data_holding.head(3))

with right_column:
    st.subheader('Bottom 3 Performer')
    st.write(data_holding.tail(3))
