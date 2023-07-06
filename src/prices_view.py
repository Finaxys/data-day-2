from snowflake.snowpark import Session
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd


def create_snowpark_session():
    session = Session.builder.configs(st.secrets["snowpark"]).create()
    return session


session = create_snowpark_session()
silver_price = session.table("SILVER_PRICE_ANALYTICS").to_pandas()


def get_x_y_entity(val, time_val):
    final_df = silver_price[silver_price['NAME'] == val].filter(['TIMESTAMP', 'PRICE'])

    final_df['TIMESTAMP'] = pd.to_datetime(final_df['TIMESTAMP'] / 1000, unit='ms').astype('datetime64[ms]')

    final_df = final_df.groupby('TIMESTAMP', as_index=False, sort=False)['PRICE'].mean()

    final_df = final_df.sort_values('TIMESTAMP')

    final_df.TIMESTAMP = final_df.TIMESTAMP.dt.floor('30T').ffill()
    final_df = final_df.groupby('TIMESTAMP')['PRICE'].mean()

    final_df = final_df.between_time('07:00:00', '15:00:00')

    final_df = final_df.reset_index()
    final_df['TIMESTAMP'] = final_df['TIMESTAMP'].astype(str)
    final_df = final_df.set_index('TIMESTAMP')

    return final_df


entity = 'AXA'
time_val ='30'
final_df = get_x_y_entity(entity, time_val)
plt.plot(final_df)
plt.title('Price evolution')
plt.xlabel('TIMESTAMP')
plt.ylabel('PRICE')
st.pyplot(plt)