import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import io


sns.set(style='dark')


df1 = pd.read_csv("result_all.csv")


def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='date').agg({
        'count': 'sum',
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()
    return daily_rent_df

def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0).reset_index()
    return monthly_rent_df

def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather').agg({
        'count': 'sum'
    }).reset_index()
    return weather_rent_df


def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season').agg({
        'count': 'sum'
    }).reset_index()
    return season_rent_df


min_date = pd.to_datetime(df1['date']).dt.date.min()
max_date = pd.to_datetime(df1['date']).dt.date.max()
 
with st.sidebar:
    image_url = "https://images.unsplash.com/photo-1602148740250-0a4750e232e9?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"  # Ganti dengan URL gambar yang diinginkan
    st.image(image_url, use_column_width=True)
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = df1[(df1['date'] >= str(start_date)) & 
                (df1['date'] <= str(end_date))]


daily_rent_df = create_daily_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
merged_df = pd.merge(monthly_rent_df, season_rent_df, left_on='month', right_on='season', how='outer')


st.header('Bike Rental Dashboard :sparkles:')

st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_rent_df['casual'].sum()
    st.metric('Casual User', value=daily_rent_casual)

with col2:
    daily_rent_registered = daily_rent_df['registered'].sum()
    st.metric('Registered User', value=daily_rent_registered)
 
with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    st.metric('Total User', value=daily_rent_total)

st.subheader('Monthly Rentals')
fig, ax = plt.subplots(figsize=(24, 8))
ax.bar(
    monthly_rent_df['month'],  # Updated here
    monthly_rent_df['count'],
    color='tab:blue'
)

for index, row in enumerate(monthly_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)

st.pyplot(fig)


st.subheader('Season Rentals')

fig, ax = plt.subplots(figsize=(16, 8), frameon=True, dpi=100)


sns.barplot(
    x="season",
    y="count",
    data=season_rent_df,
    palette = 'husl',
    ax=ax
)

for index, row in enumerate(season_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x')
ax.tick_params(axis='y')

st.pyplot(fig)


st.subheader('Weatherly Rentals')

fig, ax = plt.subplots(figsize=(16, 8))


sns.barplot(
    x=weather_rent_df.index,
    y=weather_rent_df["count"],
    palette = 'husl',
    ax=ax
)

for index, row in enumerate(weather_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)



st.caption('Copyright (c) Dhimas Dwi Nugroho 2023')
