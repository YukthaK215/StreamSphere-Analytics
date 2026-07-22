import streamlit as st
import pandas as pd
import plotly.express as px
from db_connection import get_connection

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="StreamSphere Analytics",
    page_icon="📊",
    layout="wide"
)

conn = get_connection()

# ---------------- SQL QUERIES ---------------- #

query = """
SELECT
    v.title,
    v.category,
    COUNT(*) AS total_views
FROM watch_history w
JOIN videos v
ON w.video_id = v.video_id
GROUP BY v.title, v.category
ORDER BY total_views DESC;
"""

df = pd.read_sql(query, conn)

country_query = """
SELECT
    u.country,
    v.title,
    v.category,
    COUNT(*) AS total_views
FROM watch_history w
JOIN users u
ON w.user_id = u.user_id
JOIN videos v
ON w.video_id = v.video_id
GROUP BY u.country, v.title, v.category;
"""

country_df = pd.read_sql(country_query, conn)



# ---------------- CATEGORY DATA ---------------- #

category_query = """
SELECT
    category,
    COUNT(*) AS total_videos
FROM videos
GROUP BY category;
"""

category_filter_query = """
SELECT DISTINCT category
FROM videos
ORDER BY category;
"""
country_filter_query = """
SELECT DISTINCT country
FROM users
ORDER BY country;
"""



category_df = pd.read_sql(category_query, conn)
category_filter_df = pd.read_sql(category_filter_query, conn)

# ---------------- SIDEBAR FILTERS ---------------- #

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("📊 StreamSphere")

st.sidebar.caption("Product Analytics Dashboard")

st.sidebar.markdown("---")

st.sidebar.subheader("🎯 Dashboard Filters")

country_filter_df = pd.read_sql(country_filter_query, conn)

country_options = ["All"] + country_filter_df["country"].tolist()

selected_country = st.sidebar.selectbox(
    "🌍 Select Country",
    country_options
)



# ---------------- SIDEBAR FILTERS ---------------- #

categories = ["All"] + sorted(df["title"].unique().tolist())

selected_video = st.sidebar.selectbox(
    "🎥 Select Video",
    categories
)

category_options = ["All"] + category_filter_df["category"].tolist()

selected_category = st.sidebar.selectbox(
    "📂 Select Category",
    category_options
)

# Apply country filter
if selected_country != "All":
    df = country_df[country_df["country"] == selected_country]
else:
    df = df

# Apply video filter
if selected_video != "All":
    df = df[df["title"] == selected_video]

# Apply category filter
if selected_category != "All":
    df = df[df["category"] == selected_category]

if df.empty:
    st.warning("⚠️ No data found for the selected filters.")
    st.stop()

category_df = (
    df.groupby("category")
      .size()
      .reset_index(name="total_videos")
)



# ---------------- COUNTRY DATA ---------------- #

if selected_country == "All":

    country_query = """
    SELECT
        country,
        COUNT(*) AS total_users
    FROM users
    GROUP BY country;
    """

else:

    country_query = f"""
    SELECT
        country,
        COUNT(*) AS total_users
    FROM users
    WHERE country = '{selected_country}'
    GROUP BY country;
    """

country_df = pd.read_sql(country_query, conn)
# Apply category filter
if selected_category != "All":
    category_df = category_df[
        category_df["category"] == selected_category
    ]

views_query = """
SELECT
    u.country,
    COUNT(*) AS total_views
FROM watch_history w
JOIN users u
ON w.user_id = u.user_id
GROUP BY u.country;
"""

average_views_query = """
SELECT
    ROUND(COUNT(*)::numeric / COUNT(DISTINCT video_id), 2) AS avg_views
FROM watch_history;
"""

users_query = """
SELECT
    country,
    COUNT(*) AS total_users
FROM users
GROUP BY country;
"""

countries_query = """
SELECT COUNT(DISTINCT country) AS total_countries
FROM users;
"""

categories_query = """
SELECT COUNT(DISTINCT category) AS total_categories
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

views_df = pd.read_sql(views_query, conn)
if selected_country != "All":
    views_df = views_df[
        views_df["country"] == selected_country
    ]
average_views_df = pd.read_sql(average_views_query, conn)
users_df = pd.read_sql(users_query, conn)
if selected_country != "All":
    users_df = users_df[
        users_df["country"] == selected_country
    ]
countries_df = pd.read_sql(countries_query, conn)
categories_count_df = pd.read_sql(categories_query, conn)
date_df = pd.read_sql(date_query, conn)
active_users_df = pd.read_sql(active_users_query, conn)
category_views_df = pd.read_sql(category_views_query, conn)

# ---------------- TITLE ---------------- #
st.image(
    "https://img.icons8.com/color/96/combo-chart--v1.png",
    width=70
)
st.title("📊 StreamSphere Analytics Dashboard")

st.markdown("""
### Real-time insights into video performance, user engagement, and content trends.

Analyze user behavior, monitor content performance, and explore key business metrics through interactive dashboards powered by **Python, PostgreSQL, Streamlit, and Plotly**.
""")

st.divider()

# ---------------- KPI CARDS ---------------- #

col1, col2, col3, col4 = st.columns(4)
col5, col6, col7 = st.columns(3)

with col1:
    st.metric("🎥 Total Videos", len(df))

with col2:
    st.metric("⭐ Most Viewed Video", df.iloc[0]["title"])

with col3:
    total_views = int(views_df["total_views"].sum())
    st.metric("👀 Total Views", total_views)

with col4:
    total_users = int(users_df["total_users"].sum())
    st.metric("👥 Total Users", total_users)

with col5:
    if selected_country == "All":
        countries = int(countries_df.iloc[0]["total_countries"])
    else:
        countries = 1

    st.metric(
        "🌍 Countries",
        countries
    )

with col6:
    st.metric("📂 Categories", int(categories_count_df.iloc[0]["total_categories"]))


with col7:
    st.metric(
        "📈 Avg Views / Video",
        average_views_df.iloc[0]["avg_views"]
    )

st.divider()
st.divider()

# ---------------- DASHBOARD INSIGHTS ---------------- #

# ---------------- DASHBOARD SUMMARY ---------------- #

st.subheader("📌 Dashboard Summary")

col1, col2 = st.columns(2)

with col1:
    st.success(f"🎥 Most Viewed Video: **{df.iloc[0]['title']}**")

    st.info(f"📈 Average Views per Video: **{average_views_df.iloc[0]['avg_views']}**")

with col2:
    st.warning(f"📂 Selected Category: **{selected_category}**")

    st.info(f"🌍 Selected Country: **{selected_country}**")

# ---------------- ROW 1 ---------------- #

left, right = st.columns(2)

# ---------------- ROW 1 ---------------- #

left, right = st.columns(2)

with left:

    st.subheader("🎥 Top Viewed Videos")

    st.dataframe(df)

    st.download_button(
        label="📥 Download CSV",
        data=df.to_csv(index=False),
        file_name="top_viewed_videos.csv",
        mime="text/csv"
    )

    st.bar_chart(
        df.set_index("title"),
        use_container_width=True
    )

with right:

    st.subheader("📂 Videos by Category")

    st.dataframe(category_df)

    fig = px.pie(
    category_df,
    names="category",
    values="total_videos",
    title="Video Distribution by Category",
    hole=0.4
)

    st.plotly_chart(fig, use_container_width=True)

    st.bar_chart(
        category_df.set_index("category"),
        use_container_width=True
    )

# ---------------- ROW 2 ---------------- #

left, right = st.columns(2)

with left:

    st.subheader("👥 Users by Country")

    st.dataframe(country_df)

    st.bar_chart(
        country_df.set_index("country"),
        use_container_width=True
    )

with right:

    st.subheader("📅 Video Upload Trend")

    st.dataframe(date_df)

    st.line_chart(
        date_df.set_index("upload_date"),
        use_container_width=True
    )

# ---------------- ROW 3 ---------------- #

left, right = st.columns(2)

with left:

    st.subheader("👤 Top 5 Most Active Users")

    st.dataframe(active_users_df)

    st.bar_chart(
        active_users_df.set_index("name"),
        use_container_width=True
    )

with right:

    st.subheader("📊 Most Popular Video Categories")

    st.dataframe(category_views_df)

    st.bar_chart(
        category_views_df.set_index("category"),
        use_container_width=True
    )

# ---------------- FOOTER ---------------- #

st.markdown("---")

st.divider()

st.markdown(
    """
    <div style='text-align:center; color:gray;'>
        🚀 <b>StreamSphere Analytics Dashboard</b><br>
        Developed by <b>Yuktha K</b><br>
        Python • PostgreSQL • Streamlit • Plotly
    </div>
    """,
    unsafe_allow_html=True
)