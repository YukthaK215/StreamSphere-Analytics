import streamlit as st
import pandas as pd
from db_connection import get_connection

st.set_page_config(
    page_title="User Analytics",
    page_icon="👥",
    layout="wide"
)

conn = get_connection()

# ---------------- SQL QUERIES ---------------- #

users_query = """
SELECT COUNT(*) AS total_users
FROM users;
"""

active_users_query = """
SELECT
    u.name,
    COUNT(w.watch_id) AS videos_watched
FROM users u
JOIN watch_history w
ON u.user_id = w.user_id
GROUP BY u.name
ORDER BY videos_watched DESC
LIMIT 5;
"""

# ---------------- DATA ---------------- #

users_df = pd.read_sql(users_query, conn)
active_users_df = pd.read_sql(active_users_query, conn)

# ---------------- TITLE ---------------- #

st.title("👥 User Analytics")

st.markdown("""
Analyze user activity and engagement.
""")

st.divider()

# ---------------- KPI ---------------- #

st.metric("👥 Total Users", int(users_df.iloc[0]["total_users"]))

st.divider()

# ---------------- TOP USERS ---------------- #

st.subheader("🏆 Top 5 Most Active Users")

st.dataframe(active_users_df)

st.bar_chart(
    active_users_df.set_index("name"),
    use_container_width=True
)

st.divider()

# ---------------- INSIGHTS ---------------- #

st.subheader("📌 Key Insights")

st.success(f"🏆 Most Active User: {active_users_df.iloc[0]['name']}")

st.info(f"👥 Total Registered Users: {users_df.iloc[0]['total_users']}")

st.warning("📈 User activity is measured based on videos watched.")

conn.close()