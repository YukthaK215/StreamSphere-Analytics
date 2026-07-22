import streamlit as st
import pandas as pd
import plotly.express as px
from db_connection import get_connection

st.set_page_config(
    page_title="Engagement Analytics",
    page_icon="📈",
    layout="wide"
)

conn = get_connection()

# ---------------- SQL QUERIES ---------------- #

query = """
SELECT
    v.title,
    COUNT(*) AS total_views
FROM watch_history w
JOIN videos v
ON w.video_id = v.video_id
GROUP BY v.title
ORDER BY total_views DESC;
"""

views_query = """
SELECT COUNT(*) AS total_views
FROM watch_history;
"""

average_views_query = """
SELECT
ROUND(COUNT(*)::numeric / COUNT(DISTINCT video_id),2) AS avg_views
FROM watch_history;
"""

category_views_query = """
SELECT
v.category,
COUNT(w.watch_id) AS total_views
FROM videos v
JOIN watch_history w
ON v.video_id = w.video_id
GROUP BY v.category
ORDER BY total_views DESC;
"""

# ---------------- DATA ---------------- #

df = pd.read_sql(query, conn)
views_df = pd.read_sql(views_query, conn)
average_views_df = pd.read_sql(average_views_query, conn)
category_views_df = pd.read_sql(category_views_query, conn)

# ---------------- TITLE ---------------- #

st.title("📈 Engagement Analytics")

st.markdown("""
Analyze user engagement through video views, popularity, and content performance.
""")

st.divider()

# ---------------- KPI CARDS ---------------- #

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👀 Total Views", int(views_df.iloc[0]["total_views"]))

with col2:
    st.metric("⭐ Most Viewed Video", df.iloc[0]["title"])

with col3:
    st.metric("📈 Avg Views / Video", average_views_df.iloc[0]["avg_views"])

st.divider()

# ---------------- TOP VIEWED VIDEOS ---------------- #

st.subheader("🎥 Top Viewed Videos")

st.dataframe(df)

st.bar_chart(df.set_index("title"))

# ---------------- CATEGORY ENGAGEMENT ---------------- #

st.subheader("📊 Most Popular Video Categories")

st.dataframe(category_views_df)

fig = px.pie(
    category_views_df,
    names="category",
    values="total_views",
    title="Category-wise Engagement"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- INSIGHTS ---------------- #

st.subheader("📌 Key Insights")

st.success(f"🔥 Most Viewed Video: {df.iloc[0]['title']}")

st.info(f"📈 Average Views per Video: {average_views_df.iloc[0]['avg_views']}")

st.warning("📂 Education is currently the most popular category.")

conn.close()