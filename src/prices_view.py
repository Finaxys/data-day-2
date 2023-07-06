from snowflake.snowpark import Session
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd


def create_snowpark_session():
    session = Session.builder.configs(st.secrets["snowpark"]).create()
    return session


session = create_snowpark_session()
silver_price = session.sql("SELECT * FROM SILVER_PRICE_ANALYTICS WHERE NAME = 'AXA'").to_pandas()

final_df = silver_price.filter(['TIMESTAMP', 'PRICE'])

final_df['TIMESTAMP'] = pd.to_datetime(final_df['TIMESTAMP'] / 1000, unit='ms').astype('datetime64[ms]')

final_df = final_df.groupby('TIMESTAMP', as_index=False, sort=False)['PRICE'].mean()

final_df = final_df.sort_values('TIMESTAMP')
final_df = final_df.set_index('TIMESTAMP')
final_df = final_df.resample('ms').ffill()
final_df = final_df.resample('30T').mean()

final_df = final_df.between_time('07:00:00', '15:00:00')

final_df = final_df.reset_index()
final_df['TIMESTAMP'] = final_df['TIMESTAMP'].astype(str)
final_df = final_df.set_index('TIMESTAMP')

plt.plot(final_df)
plt.title('Price evolution')
plt.xlabel('TIMESTAMP')
plt.ylabel('PRICE')
st.pyplot(plt)