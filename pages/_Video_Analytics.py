import streamlit as st
import pandas as pd
import plotly.express as px
from db_connection import get_connection

st.set_page_config(
    page_title="Video Analytics",
    page_icon="🎥",
    layout="wide"
)

conn = get_connection()

# ---------------- SQL QUERIES ---------------- #

videos_query = """
SELECT COUNT(*) AS total_videos
FROM videos;
"""

category_query = """
SELECT
    category,
    COUNT(*) AS total_videos
FROM videos
GROUP BY category
ORDER BY total_videos DESC;
"""

top_videos_query = """
SELECT
    title,
    category
FROM videos;
"""

# ---------------- DATA ---------------- #

videos_df = pd.read_sql(videos_query, conn)
category_df = pd.read_sql(category_query, conn)
top_videos_df = pd.read_sql(top_videos_query, conn)

# ---------------- TITLE ---------------- #

st.title("🎥 Video Analytics")

st.markdown("""
Analyze video library, categories, and content distribution.
""")

st.divider()

# ---------------- KPI ---------------- #

st.metric("🎥 Total Videos", int(videos_df.iloc[0]["total_videos"]))

st.divider()

# ---------------- CATEGORY DISTRIBUTION ---------------- #

st.subheader("📂 Videos by Category")

st.dataframe(category_df)

st.bar_chart(
    category_df.set_index("category"),
    use_container_width=True
)

fig = px.pie(
    category_df,
    names="category",
    values="total_videos",
    title="Video Category Distribution"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------- VIDEO LIST ---------------- #

st.subheader("🎬 Video Library")

st.dataframe(top_videos_df)

st.divider()

# ---------------- INSIGHTS ---------------- #

st.subheader("📌 Key Insights")

st.success(f"🎥 Total Videos: {videos_df.iloc[0]['total_videos']}")

st.info(f"📂 Total Categories: {len(category_df)}")

st.warning("📊 Education currently contains the highest number of videos.")

conn.close()