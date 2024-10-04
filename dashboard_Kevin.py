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

datemin = df1['dteday'].min()
datemax = df1['dteday'].max()
with st.sidebar:
    st.header('Kevin\'s dashboard')
    st.image('IMG_5170.JPG')

    date_1, date_n = st.date_input(
        label = 'Date range:',
        min_value = datemin,
        max_value = datemax,
        value = [datemin,datemax]
    )

    hour = st.selectbox(label = 'Select Hour', options=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23))

main_df1 = df1[(df1['dteday'] >= str(date_1))&(df1['dteday'] <= str(date_n))]

daily_main_df1 = main_df1.resample(rule='D', on='dteday').agg({
    "cnt" : "sum"
})
daily_main_df1 = daily_main_df1.reset_index()
daily_main_df1.rename(columns={
    'cnt' : 'count'
}, inplace=True)

st.subheader('Ranged-Daily Bike Sharing')

column1, column2 = st.columns(2)
with column1:
    Count = daily_main_df1['count'].sum()
    st.metric('Order Count:', value=Count)
    
#
fig,ax = plt.subplots(figsize=(24,12))
ax.plot(
    daily_main_df1['dteday'],
    daily_main_df1['count'],
    marker = 'o',
    linewidth = 2,
    color = "#90CAF9"
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
ax.set_title("Casual Weather", loc="center", 25)
ax.set_ylabel("count mean", size=20)
ax.set_xlabel("hour", size=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)
