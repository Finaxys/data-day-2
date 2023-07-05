from snowflake.snowpark import Session
from snowflake.snowpark.functions import avg, sum, col, cast
from snowflake.snowpark.types import IntegerType
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



#create snowpark session
def create_snowpark_session():
    
    session = Session.builder.configs(st.secrets["snowpark"]).create()
    return session

# get all agent names in list
session = create_snowpark_session()
silver_esg = session.table("SILVER_ESG_ANALYTICS")
agent_names = silver_esg.select("AGENTNAME").distinct().sort('AGENTNAME').collect()

# Side bar for agent names
agent = st.sidebar.selectbox(
    "Select agent name",
    (agent_names)
)

st.header('ESG PORTFOLIO ANALYSIS')

# get ESG, E, S, G and holding avg
silver_esg = silver_esg.filter(col('AGENTNAME') == agent)
esg_avg = silver_esg.select(avg('ESG').alias("ESG"), avg('E').alias("E"), avg('S').alias("S"), avg('G').alias("G"), avg('HOLDING').alias("HOLDING"))
esg_avg = esg_avg.to_pandas()
esg_avg.columns = ['ESG Score', 'Environment Score', 'Social Score', 'Governance Score', 'HOLDING']
st.markdown(esg_avg.style.hide(axis="index").to_html(), unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader('TOP 3 ESG')
    bottom_3 = silver_esg.sort(col("ESG").desc()).limit(3).select('INSTRUMENT_NAME', 'ESG').to_pandas()
    bottom_3.columns = ['INSTRUMENT', 'ESG SCORE']
    st.markdown(bottom_3.style.hide(axis="index").to_html(), unsafe_allow_html=True)


with col2:
    st.subheader('BOTTOM 3 ESG')
    top_3 = silver_esg.sort(col("ESG").asc()).limit(3).select('INSTRUMENT_NAME', 'ESG').to_pandas()
    top_3.columns = ['INSTRUMENT', 'ESG SCORE']
    st.markdown(top_3.style.hide(axis="index").to_html(), unsafe_allow_html=True)


ratio_sector = silver_esg.group_by("SECTOR_LONGNAME").agg(cast(sum('HOLDING_RATIO')*100, IntegerType()))
#get sector names with no ratio and replace None valeus with 0
ratio_sector_all = session.table("SILVER_ESG_ANALYTICS").select("SECTOR_LONGNAME").distinct().join(ratio_sector, "SECTOR_LONGNAME", "leftouter").replace(to_replace=None, value=0)

ratio_sector_all = ratio_sector_all.to_pandas()
ratio_sector_all.columns = ['SECTOR_LONGNAME', 'RATIO']


st.subheader('Sector Allocation')

st.data_editor(
    ratio_sector_all,
    column_config={
        "SECTOR_LONGNAME": st.column_config.TextColumn(
            "SECTORS"
        ),
        "RATIO": st.column_config.ProgressColumn(
            "RATIO (PERCENTAGE)",
            format='%f%%',
            min_value=-100,
            
            max_value=100,
        ),
    },
    hide_index=True,
)

df = pd.DataFrame(data=ratio_sector_all)
df = df.set_index("SECTOR_LONGNAME")

st.bar_chart(df, use_container_width=True)


x = ratio_sector_all['SECTOR_LONGNAME']
y = ratio_sector_all['RATIO']

fig, ax = plt.subplots()
bars = ax.barh(x, y)

ax.bar_label(bars)   
width = 0.75 # the width of the bars 
ind = np.arange(len(y))  # the x locations for the groups
ax.barh(ind, y, width, color="dodgerblue")
ax.set_yticklabels(x, minor=False)
ax.set_xlim([-100, 100])

plt.title('SECTOR ALLOCATION')
plt.xlabel('RATIO (percent)')
plt.ylabel('SECTOR NAME')      
st.pyplot(plt)