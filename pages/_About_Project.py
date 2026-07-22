import streamlit as st

st.set_page_config(page_title="About Project", page_icon="📘", layout="wide")

st.title("📘 About StreamSphere Analytics Dashboard")

st.markdown("""
## 📌 Project Overview

**StreamSphere Analytics Dashboard** is an interactive analytics platform developed using **Python, PostgreSQL, Streamlit, Pandas, and Plotly**.

The dashboard helps analyze video performance, user engagement, geographical distribution, and content trends through interactive visualizations and KPI cards.
""")

st.divider()

st.subheader("🛠️ Technology Stack")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
- 🐍 Python
- 🗄️ PostgreSQL
- 📊 Streamlit
""")

with col2:
    st.markdown("""
- 📈 Plotly
- 🐼 Pandas
- 🔍 SQL
""")

st.divider()

st.subheader("✨ Key Features")

st.markdown("""
- 📊 Interactive Dashboard
- 🎥 Video Performance Analytics
- 👥 User Analytics
- 🌍 Geography Analytics
- 📅 Time-Based Analytics
- 🔎 Interactive Filters
- 📈 KPI Cards
- 📥 CSV Export
""")

st.divider()

st.subheader("🗂️ Database Tables")

st.markdown("""
- **users**
- **videos**
- **watch_history**
""")

st.divider()

st.subheader("🎯 Project Objective")

st.info("""
The objective of this project is to provide meaningful insights into video content performance and user engagement using an interactive analytics dashboard powered by SQL and Python.
""")

st.divider()

st.success("🚀 Developed by Yuktha K | Product Analytics Platform")