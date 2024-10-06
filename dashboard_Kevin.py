import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

st.header('Bike Sharing Dashboard :bike:')

df1 = pd.read_csv('day.csv')
df1['dteday'] = pd.to_datetime(df1['dteday'])
df2 = pd.read_csv('hour.csv')
df2['dteday'] = pd.to_datetime(df2['dteday'])

with st.sidebar:
    st.header('Kevin\'s dashboard')
    st.image('IMG_5170.JPG')

    hour = st.selectbox(label = 'Select Hour', options=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23))


mdf1 = df1.resample(rule='M', on='dteday').agg({
    "cnt": "sum"
})

mdf1.index = mdf1.index.strftime('%Y-%m')
mdf1 = mdf1.reset_index()
mdf1.rename(columns={
    "dteday": "month",
    "cnt": "cnt_monthly"
}, inplace=True)

st.subheader('Monthly Bike Sharing')
    
#
fig,ax = plt.subplots(figsize=(24,12))
ax.plot(
    mdf1['month'],
    mdf1['cnt_monthly'],
    marker = 'o',
    linewidth = 2,
    color = "red"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

#
wdf1 = df1.groupby(by=["weathersit"]).agg({
    "casual": "sum",
    "registered": "sum",
    "cnt": "sum"
})

wdf1 = wdf1.reset_index()
wdf1.rename(columns={
    "casual": "casual_w",
    "registered": "registered_w",
    "cnt": "cnt_w"
}, inplace=True)

wdf1["weather"] = wdf1["weathersit"].apply(lambda x: "clear" if x == 1 else "mist" if x == 2 else "light snow" if x == 3 else "heavy rain")

st.subheader('The Effect of Weather on The Number of Bicycle Sharing')

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(12,6))

sns.barplot(data=wdf1, x="weather", y="casual_w", ax=ax[0])
ax[0].set_title("Casual User in Each Weather", loc="center")
ax[0].set_ylabel('Count')
ax[0].set_xlabel(None)
ax[0].tick_params(axis='x', labelsize=11)
sns.barplot(data=wdf1, x="weather", y="registered_w", color='red', ax=ax[1])
ax[1].set_title("Reg. User in Each Weather", loc="center")
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].tick_params(axis='x', labelsize=11)
sns.barplot(data=wdf1, x="weather", y="cnt_w", color='green',ax=ax[2])
ax[2].set_title("Total User in Each Weather", loc="center")
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].tick_params(axis='x', labelsize=11)
st.pyplot(fig)

st.subheader('Hourly Average of Bike Sharing')

hdf2 = df2.groupby(by=["hr"]).agg({
    "cnt": "mean"
})
column3, column4 = st.columns(2)
with column3:
    Count = hdf2['cnt'][hour]
    st.metric('Average total user in hour that you choose:', value=Count)

fig,ax = plt.subplots(nrows=1, ncols=1,figsize=(24,20))
sns.barplot(data=hdf2, x="hr", y="cnt")
ax.set_title("Casual Weather", loc="center", size=25)
ax.set_ylabel("count mean", size=20)
ax.set_xlabel("hour", size=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)
