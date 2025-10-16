import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from CSV
@st.cache_data
def load_data():
    file_path = r'O:\Project_2\netflix title.csv'
    df = pd.read_csv(file_path)
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    return df

df = load_data()

#App Layout
st.title("🎬 Netflix Content Explorer")
st.markdown("Analyze trends in titles, ratings, durations, and genres using interactive filters.")


#Sidebar filter
type_filter = st.sidebar.selectbox("Select Type", options=['All'] + sorted(df['type'].dropna().unique().tolist()))
country_filter = st.sidebar.multiselect("Select Country", options=sorted(df['country'].dropna().unique().tolist()))
year_range = st.sidebar.slider("Release Year Range", int(df['release_year'].min()), int(df['release_year'].max()), (2010, 2020))

filtered_df = df.copy()
if type_filter != 'All':
    filtered_df = filtered_df[filtered_df['type'] == type_filter]
if country_filter:
    filtered_df = filtered_df[filtered_df['country'].isin(country_filter)]
filtered_df = filtered_df[(filtered_df['release_year'] >= year_range[0]) & (filtered_df['release_year'] <= year_range[1])]

#Data preview
st.subheader("Filtered Titles")
st.dataframe(filtered_df[['title', 'type', 'country', 'release_year', 'rating', 'duration']].head(10))

#Content Type Distribution
st.subheader("Content Type Distribution")
type_counts = filtered_df['type'].value_counts()
fig1, ax1 = plt.subplots()
sns.barplot(x=type_counts.index, y=type_counts.values, ax=ax1)
ax1.set_ylabel("Count")
st.pyplot(fig1)

#Release Year Trend
st.subheader("Titles Released Over Time")
year_counts = filtered_df['release_year'].value_counts().sort_index()
fig2, ax2 = plt.subplots()
sns.lineplot(x=year_counts.index, y=year_counts.values, marker='o', ax=ax2)
ax2.set_xlabel("Year")
ax2.set_ylabel("Number of Titles")
st.pyplot(fig2)

#Rating Distribution
st.subheader("Rating Distribution")
fig3, ax3 = plt.subplots()
sns.countplot(data=filtered_df, y='rating', order=filtered_df['rating'].value_counts().index, ax=ax3)
st.pyplot(fig3)

