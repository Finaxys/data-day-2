import streamlit as st
import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np


esg_history_df = pd.read_excel(
    io=r'../ESG REPORT v1.0.xlsx',
    engine='openpyxl',
    sheet_name='RAW'
)

esg_history_df_gold = pd.read_csv('../cache/SILVER_ESG_ANA.csv', index_col=False)
#esg_history_df = pd.read_csv('../cache/SILVER_ESG.csv', index_col=False)
agents_names = list(set(esg_history_df['AGENTNAME'].values))
agents_names.insert(0, '')



price_history_df = pd.read_csv('../cache/SILVER_PRICE_ANA.csv')
company_names = list(set(price_history_df['NAME'].values))
company_names.append('')


def plot(xpoints, ypoints):
    fig = plt.figure(figsize = (15, 7))
    
    plt.plot(xpoints, ypoints)
    plt.xlabel("Timelapse during the day")
    plt.ylabel("Price")
    plt.title("Price evolution")
    st.pyplot(fig)



def get_x_y_isin(val, time_vale):

    final_df = price_history_df[price_history_df['OBNAME'] == val].filter(['TIMESTAMP', 'PRICE'])

    final_df['TIMESTAMP'] = pd.to_datetime(final_df['TIMESTAMP']/1000, unit='ms').astype('datetime64[ms]')

    final_df =final_df.groupby('TIMESTAMP', as_index=False, sort=False)['PRICE'].mean()


    final_df = final_df.sort_values('TIMESTAMP')
    final_df = final_df.set_index('TIMESTAMP')
    final_df = final_df.resample('ms').bfill()
    final_df = final_df.resample( time_vale+'T').mean()


    final_df = final_df.between_time('07:00:00', '15:00:00')
    
    final_df = final_df.reset_index()
    final_df['TIMESTAMP']=final_df['TIMESTAMP'].astype(str)
    final_df = final_df.set_index('TIMESTAMP')
                          

    xpoints = list(final_df.index)
    
    ypoints = list(final_df['PRICE'].values)

    return xpoints, ypoints, final_df


def get_x_y_entity(val, time_val):
    final_df = price_history_df[price_history_df['NAME'] == val].filter(['TIMESTAMP', 'PRICE'])

    final_df['TIMESTAMP'] = pd.to_datetime(final_df['TIMESTAMP']/1000, unit='ms').astype('datetime64[ms]')

    final_df =final_df.groupby('TIMESTAMP', as_index=False, sort=False)['PRICE'].mean()


    final_df = final_df.sort_values('TIMESTAMP')
    final_df = final_df.set_index('TIMESTAMP')
    final_df = final_df.resample('ms').bfill()
    #values = final_df.resample(time_val+'T').aggregate()
    final_df = final_df.resample(time_val+'T').mean()
    

    final_df = final_df.between_time('07:00:00', '15:00:00')
    
    final_df = final_df.reset_index()
    final_df['TIMESTAMP']=final_df['TIMESTAMP'].astype(str)
    final_df = final_df.set_index('TIMESTAMP')
                          

    xpoints = list(final_df.index)
    
    ypoints = list(final_df['PRICE'].values)

    return xpoints, ypoints, final_df

def return_top_3_esg(agent_name):
    
    data_agent = esg_history_df.loc[esg_history_df['AGENTNAME'] == agent_name]
    data_instrument = data_agent.filter(['INSTRUMENT_NAME', 'ESG']).groupby('INSTRUMENT_NAME').mean().sort_values('ESG', ascending=False)
    data_instrument['ESG'] = data_instrument['ESG'].astype(str).str.replace('.0', '', regex=False)
    data_instrument = data_instrument.reset_index()

    return data_instrument.tail(3)


def return_bottom_3_esg(agent_name):
    data_agent = esg_history_df.loc[esg_history_df['AGENTNAME'] == agent_name]
    data_instrument = data_agent.filter(['INSTRUMENT_NAME', 'ESG']).groupby('INSTRUMENT_NAME').mean().sort_values('ESG', ascending=False)
    data_instrument['ESG'] = data_instrument['ESG'].astype(str).str.replace('.0', '', regex=False)
    data_instrument = data_instrument.reset_index()

    return data_instrument.head(3)




st.title('ESG PORTFOLIO ANALYSIS')
# Side bar for agent names

agent = st.sidebar.selectbox(
    "Select agent name",
    (agents_names)
)

if agent!='':
    data_agent = esg_history_df.loc[esg_history_df['AGENTNAME'] == agent]
    agents_info = data_agent.filter(['AGENTNAME', 'ESG', 'E', 'S', 'G', 'HOLDING']).groupby('AGENTNAME').mean()
    agents_info = agents_info.reset_index()
    agents_info = agents_info.drop(columns = ['AGENTNAME'])
    agents_info = agents_info[['ESG', 'E', 'S', 'G', 'HOLDING']]
    agents_info.columns = ['ESG Score', 'Environment Score', 'Social Score', 'Governance Score', 'HOLDING']
    
    #convert into string to delete 0s 
    agents_info= agents_info.round(2)
    for col in agents_info.columns:
        agents_info[col] = agents_info[col].astype(str).str.replace('.0', '', regex=False)


    st.markdown(agents_info.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('TOP 3 ESG')
        
        st.markdown(return_top_3_esg(agent).style.hide(axis="index").to_html(), unsafe_allow_html=True)
        #compute the holding ratio per each sector using groupby function
        st.subheader('Sector Allocation')

        data_sector = data_agent.filter(['SECTOR_LONGNAME', 'HOLDING_RATIO']).groupby('SECTOR_LONGNAME').sum()
        data_sector['HOLDING_RATIO'] = data_sector['HOLDING_RATIO'].round(2)*100
        
        ratio_sector = data_sector.reset_index()
        
        
        ratio_sector['HOLDING_RATIO'] = ratio_sector['HOLDING_RATIO'].astype('int')

        #print the progress bar with holding ratio
        st.data_editor(
        ratio_sector[['SECTOR_LONGNAME','HOLDING_RATIO']],
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
        #get total ratio
        st.write('TOTAL : ', ratio_sector['HOLDING_RATIO'].sum(), '%')

    with col2:
        st.subheader('BOTTOM 3 ESG')
        st.markdown(return_bottom_3_esg(agent).style.hide(axis="index").to_html(), unsafe_allow_html=True)

