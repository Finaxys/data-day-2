import streamlit as st
import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np


price_history_df = pd.read_csv('../cache/SILVER_PRICE_ANA.csv')
company_names = list(set(price_history_df['NAME'].values))
company_names.append('')


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


#get graph based on ISIN code
st.title('Price evolution based on code ISIN')

col_isin1, col_isin2 = st.columns(2)
with col_isin1:

    isin=st.text_input('ISIN code')

with col_isin2:
    time_val = st.radio(
    "Change timestamps values",
    ('10', '20', '30'),horizontal=True, key='10')

if isin !='':
    if isin in price_history_df['OBNAME'].values:

        xpoints, ypoints, df = get_x_y_isin(isin, time_val)
        st.line_chart(df)
        
        with col_isin1:
            st.write('Max Price', round(max(ypoints), 2))
            st.write('Min Price', round(min(ypoints), 2))
            
    else : 
        st.warning('ISIN code not found !')



#get graph based on entity name
st.title('Price evolution based on Entity Name')

col_ent1, col_ent2 = st.columns(2)
with col_ent1:
    entity = st.selectbox('Choose entity name', sorted(company_names), key = 2)

with col_ent2:
    time_val = st.radio(
    "Change timestamps values",
    ('10', '20', '30'), horizontal=True, key='20') 


if entity !='':
    xpoints, ypoints, df = get_x_y_entity(entity, time_val) 
    #plot(xpoints, ypoints)
    
    st.line_chart(df)
    with col_ent1:
        st.write('Max Price', round(max(ypoints), 2))
        st.write('Min Price', round(min(ypoints), 2))
