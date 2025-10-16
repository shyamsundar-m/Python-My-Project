import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Page config
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Ecomm_Sales.csv")
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")
region = st.sidebar.multiselect("Select Region", options=df["Region"].unique(), default=df["Region"].unique())
category = st.sidebar.multiselect("Select Category", options=df["Category"].unique(), default=df["Category"].unique())

filtered_df = df[(df["Region"].isin(region)) & (df["Category"].isin(category))]

# Title
st.title("Sales Dashboard")

# KPIs
total_sales = filtered_df["Sales"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Orders", total_orders)
col3.metric("Unique Customers", total_customers)

st.markdown("---")

# Sales by Category
st.subheader("Sales by Category")
fig1 = px.bar(filtered_df.groupby("Category")["Sales"].sum().reset_index(), x="Category", y="Sales", color="Category")
st.plotly_chart(fig1, use_container_width=True)

# Sales by Region
st.subheader("Sales by Region")
fig2 = px.pie(filtered_df, names="Region", values="Sales", title="Sales Distribution by Region")
st.plotly_chart(fig2, use_container_width=True)

# Correlation Heatmap
st.subheader("Correlation Heatmap")
numeric_df = filtered_df.select_dtypes(include=np.number)
fig4, ax = plt.subplots()
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig4)