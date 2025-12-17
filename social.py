import streamlit as st
import pandas as pd

# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(
    page_title="Social Media Engagement Dashboard",
    layout="wide"
)

# ----------------------------
# Load dataset
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("social_media_3platforms_3years.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["engagement"] = df["likes"] + df["comments"] + df["shares"]
    return df

df = load_data()

# ----------------------------
# Dashboard title
# ----------------------------
st.title("📊 Social Media Engagement Analytics Dashboard")
st.write("Select *Year* and *Month* to analyze platform and content performance.")

# ----------------------------
# User input controls
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    selected_year = st.selectbox(
        "Select Year",
        sorted(df["year"].unique())
    )

with col2:
    selected_month = st.selectbox(
        "Select Month",
        sorted(df["month"].unique())
    )

# ----------------------------
# Filter data
# ----------------------------
filtered_df = df[
    (df["year"] == selected_year) &
    (df["month"] == selected_month)
]

if filtered_df.empty:
    st.warning("No data available for the selected year and month.")
    st.stop()

# ----------------------------
# Calculations
# ----------------------------
top_platform_views = (
    filtered_df.groupby("platform")["views"]
    .sum()
    .idxmax()
)

top_platform_engagement = (
    filtered_df.groupby("platform")["engagement"]
    .sum()
    .idxmax()
)

top_content_views = (
    filtered_df.groupby("content_type")["views"]
    .sum()
    .idxmax()
)

top_content_engagement = (
    filtered_df.groupby("content_type")["engagement"]
    .sum()
    .idxmax()
)

# ----------------------------
# KPI display
# ----------------------------
st.subheader("🔍 Key Insights")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("📈 Most Viewed Platform", top_platform_views)
kpi2.metric("🔥 Most Engaged Platform", top_platform_engagement)
kpi3.metric("🎥 Most Viewed Content", top_content_views)
kpi4.metric("💬 Most Engaged Content", top_content_engagement)

# ----------------------------
# Charts
# ----------------------------
st.subheader("📊 Visual Analysis")

col3, col4 = st.columns(2)

with col3:
    st.write("Views by Platform")
    st.bar_chart(
        filtered_df.groupby("platform")["views"].sum()
    )

with col4:
    st.write("Engagement by Content Type")
    st.bar_chart(
        filtered_df.groupby("content_type")["engagement"].sum()
    )

# ----------------------------
# Data table
# ----------------------------
with st.expander("📄 View Filtered Data"):
    st.dataframe(filtered_df)
