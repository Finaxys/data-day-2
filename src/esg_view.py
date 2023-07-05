import streamlit as st
import pandas as pd
from Display import display_data

st.set_page_config(page_title='ESG Portfolio',
                   page_icon=':bar_chart:',
                   layout='wide')

st.title('ESG Portfolio Analysis')

# Read datas from Excel file
datas = pd.read_excel(
    io=r'ESG REPORT v1.0.xlsx',
    engine='openpyxl',
    sheet_name='RAW'
)

# List of uniques agent names
agents = datas['AGENTNAME'].unique()

option = st.sidebar.selectbox('Select agent : ', agents)

# Retrieved the data based on the agent name selected
# TODO : Use the selected agent name to filter data
data_agent = datas.loc[datas['AGENTNAME'] == option]

# Grouping by agent name, only display some columns and processing their mean value
data_esg = data_agent.filter(['AGENTNAME', 'ESG', 'E', 'S', 'G']).groupby('AGENTNAME').mean()

# TODO : Write data_esg dataframe with streamlit with a title named 'ESG Scoring'
st.subheader('ESG Scoring')
st.write(data_esg)

# Split the screen in 3 columns
left_column, center_column, right_column = st.columns(3)

with left_column:
    # Display all sectors and the portfolio holding ratio for each sector
    data_sector = data_agent.filter(['SECTOR_LONGNAME', 'HOLDING_RATIO']).groupby('SECTOR_LONGNAME').sum()
    data_sector['HOLDING_RATIO'] = data_sector['HOLDING_RATIO'].round(1)*100
    data_sector = data_sector.reset_index()

    st.subheader('Sector Allocation')
    # Display data with a custom display (detailed available in a separate file)
    display_data(data_sector[['SECTOR_LONGNAME','HOLDING_RATIO']])
    
# Data used to display top and bottom ESG instruments sorted by ESG score
data_instrument = data_agent.filter(['INSTRUMENT_NAME', 'ESG']).groupby('INSTRUMENT_NAME').mean().sort_values('ESG', ascending=False)

with center_column:
    st.subheader('Top 3 ESG')
    # Display top 3 ESG instruments sorted by ESG score
    st.write(data_instrument.head(3))

with right_column:
    st.subheader('Bottom 3 ESG')
    # TODO : Based on the Top 3 ESG, display bottom 3 ESG instruments sorted by ESG score
    st.write(data_instrument.tail(3))

st.subheader('Raw data')
st.write(datas)
