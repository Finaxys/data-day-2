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
    final_df = final_df.set_index('TIMESTAMP')
    final_df = final_df.resample('ms').bfill()
    # values = final_df.resample(time_val+'T').aggregate()
    final_df = final_df.resample(time_val + 'T').mean()

    final_df = final_df.between_time('07:00:00', '15:00:00')

    final_df = final_df.reset_index()
    final_df['TIMESTAMP'] = final_df['TIMESTAMP'].astype(str)
    final_df = final_df.set_index('TIMESTAMP')

    xpoints = list(final_df.index)

    ypoints = list(final_df['PRICE'].values)

    return xpoints, ypoints


entity = 'AXA'
time_val = '30'
xpoints, ypoints = get_x_y_entity(entity, time_val)

plt.plot(xpoints, ypoints)
plt.title('Price evolution')
plt.xlabel('TIMESTAMP')
plt.ylabel('PRICE')
st.pyplot(plt)
