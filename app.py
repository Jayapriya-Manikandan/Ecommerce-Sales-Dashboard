import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page title
st.title("🛒 Ecommerce Sales Dashboard")

# Load dataset
df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin1")

# Sidebar Filters
st.sidebar.header("Filters")

selected_category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

# Apply Filters
df = df[
    (df["Category"].isin(selected_category)) &
    (df["Region"].isin(selected_region))
]


# Dataset Preview
st.subheader("Dataset Preview")
st.dataframe(df.head())


# KPI Metrics
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_quantity = df["Quantity"].sum()
total_orders = df["Order ID"].nunique()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Sales ($)", f"${total_sales:,.2f}")

with col2:
    st.metric("Total Profit ($)", f"${total_profit:,.2f}")

with col3:
    st.metric("Total Quantity", total_quantity)

with col4:
    st.metric("Total Orders", total_orders)


# Sales by Category
st.subheader("Sales by Category")

category_sales = df.groupby("Category")["Sales"].sum()

fig, ax = plt.subplots()
category_sales.plot(kind="bar", ax=ax)
ax.set_xlabel("Category")
ax.set_ylabel("Sales ($)")
ax.set_title("Category-wise Sales")

st.pyplot(fig)


# Profit by Category
st.subheader("Profit by Category")

category_profit = df.groupby("Category")["Profit"].sum()

st.bar_chart(category_profit)


# Monthly Sales Trend
st.subheader("Monthly Sales Trend")

df["Order Date"] = pd.to_datetime(df["Order Date"])

monthly_sales = df.groupby(
    df["Order Date"].dt.to_period("M")
)["Sales"].sum()

monthly_sales.index = monthly_sales.index.astype(str)

st.line_chart(monthly_sales)


# Sales by Region
st.subheader("Sales by Region")

region_sales = df.groupby("Region")["Sales"].sum()

st.bar_chart(region_sales)