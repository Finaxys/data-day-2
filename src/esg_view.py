import streamlit as st
import pandas as pd
from Display import display_data

st.set_page_config(page_title='ESG Portfolio',
                   page_icon=':bar_chart:',
                   layout='wide')

st.title('ESG Portfolio Analysis')

# datas = pd.read_csv(r'ESG REPORT.csv', delimiter=';', decimal=',')

datas = pd.read_excel(
    io=r'../ESG REPORT v1.0.xlsx',
    engine='openpyxl',
    sheet_name='RAW'
)

agents = datas['AGENTNAME'].unique()
sectors = datas['SECTOR_LONGNAME'].unique()

option = st.sidebar.selectbox('Select agent : ', agents)

data_agent = datas.loc[datas['AGENTNAME'] == option]

data_esg = data_agent.filter(['AGENTNAME', 'ESG', 'E', 'S', 'G']).groupby('AGENTNAME').mean()
st.subheader('ESG Scoring')
st.write(data_esg)

left_column, center_column, right_column = st.columns(3)

with left_column:
    data_sector = data_agent.filter(['SECTOR_LONGNAME', 'HOLDING_RATIO']).groupby('SECTOR_LONGNAME').sum()
    data_sector['HOLDING_RATIO'] = data_sector['HOLDING_RATIO'].round(1)*100
    st.subheader('Sector Allocation')
    data_sector = data_sector.reset_index()
    #st.write(data_sector)
    display_data(data_sector[['SECTOR_LONGNAME','HOLDING_RATIO']])
    

data_instrument = data_agent.filter(['INSTRUMENT_NAME', 'ESG']).groupby('INSTRUMENT_NAME').mean().sort_values('ESG', ascending=False)

with center_column:
    st.subheader('Top 3 ESG')
    st.write(data_instrument.head(3))

with right_column:
    st.subheader('Bottom 3 ESG')
    st.write(data_instrument.tail(3))

st.subheader('Raw data')
st.write(datas)
