import streamlit as st
import pandas as pd
import plotly.express as px
from db_connection import get_connection

st.set_page_config(
    page_title="Geography Analytics",
    page_icon="🌍",
    layout="wide"
)

conn = get_connection()

# ---------------- SQL QUERIES ---------------- #

country_query = """
SELECT
    country,
    COUNT(*) AS total_users
FROM users
GROUP BY country
ORDER BY total_users DESC;
"""

users_query = """
SELECT COUNT(*) AS total_users
FROM users;
"""

countries_query = """
SELECT COUNT(DISTINCT country) AS total_countries
FROM users;
"""

# ---------------- DATA ---------------- #

country_df = pd.read_sql(country_query, conn)
users_df = pd.read_sql(users_query, conn)
countries_df = pd.read_sql(countries_query, conn)

# ---------------- TITLE ---------------- #

st.title("🌍 Geography Analytics")

st.markdown("""
Analyze user distribution across different countries.
""")

st.divider()

# ---------------- KPI CARDS ---------------- #

col1, col2 = st.columns(2)

with col1:
    st.metric("🌍 Total Countries", int(countries_df.iloc[0]["total_countries"]))

with col2:
    st.metric("👥 Total Users", int(users_df.iloc[0]["total_users"]))

st.divider()

# ---------------- USERS BY COUNTRY ---------------- #

st.subheader("👥 Users by Country")

st.dataframe(country_df)

st.bar_chart(
    country_df.set_index("country"),
    use_container_width=True
)

fig = px.pie(
    country_df,
    names="country",
    values="total_users",
    title="User Distribution by Country"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------- INSIGHTS ---------------- #

st.subheader("📌 Key Insights")

top_country = country_df.iloc[0]["country"]

st.success(f"🌟 Country with Highest Users: {top_country}")

st.info(f"🌍 Total Countries: {countries_df.iloc[0]['total_countries']}")

st.warning(f"👥 Total Registered Users: {users_df.iloc[0]['total_users']}")

conn.close()