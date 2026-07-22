import streamlit as st
import pandas as pd
from db_connection import get_connection

st.set_page_config(
    page_title="Time Analytics",
    page_icon="📅",
    layout="wide"
)

conn = get_connection()

# ---------------- SQL QUERIES ---------------- #

videos_query = """
SELECT COUNT(*) AS total_videos
FROM videos;
"""

date_query = """
SELECT
    upload_date,
    COUNT(*) AS total_uploads
FROM videos
GROUP BY upload_date
ORDER BY upload_date;
"""

# ---------------- DATA ---------------- #

videos_df = pd.read_sql(videos_query, conn)
date_df = pd.read_sql(date_query, conn)

# ---------------- TITLE ---------------- #

st.title("📅 Time Analytics")

st.markdown("""
Analyze video upload trends and activity over time.
""")

st.divider()

# ---------------- KPI CARDS ---------------- #

col1, col2 = st.columns(2)

with col1:
    st.metric("🎥 Total Videos", int(videos_df.iloc[0]["total_videos"]))

with col2:
    st.metric("📅 Upload Days", len(date_df))

st.divider()

# ---------------- UPLOAD TREND ---------------- #

st.subheader("📈 Video Upload Trend")

st.dataframe(date_df)

st.line_chart(
    date_df.set_index("upload_date"),
    use_container_width=True
)

st.divider()

# ---------------- KEY INSIGHTS ---------------- #

st.subheader("📌 Key Insights")

st.success(f"🎥 Total Videos Uploaded: {videos_df.iloc[0]['total_videos']}")

st.info(f"📅 Videos were uploaded across {len(date_df)} different days.")

st.warning("📈 Upload trend helps identify content publishing patterns.")

conn.close()