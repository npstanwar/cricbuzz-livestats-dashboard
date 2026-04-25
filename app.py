import streamlit as st

# Page Configuration
st.set_page_config(page_title="Cricbuzz LiveStats", page_icon="🏏", layout="wide")

# Custom Sidebar CSS
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E7EB !important;
    }

    [data-testid="stSidebarNav"] span {
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
        font-size: 15px;
        color: #4B5563;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Header
with st.sidebar:
    st.markdown("<h1 style='color: #111827; font-size: 32px; font-weight: 800; margin-bottom: 20px;'>🏏 Cricbuzz</h1>", unsafe_allow_html=True)

# Main Dashboard
st.title("🏏 Cricbuzz LiveStats Dashboard")
st.markdown("### Welcome to the ultimate cricket analytics platform.")
st.markdown("---")

tab_home, tab_insights = st.tabs(["🏠 Project Overview", "💼 Business Insights & Value"])

with tab_home:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### 📌 Project Overview
        *Cricbuzz LiveStats* is a comprehensive, user-friendly cricket analytics dashboard. It integrates real-time API data with robust historical SQL databases to provide unparalleled insights into the game of cricket.
        
        #### 🛠️ Tools & Technologies Used
        * **Frontend:** Streamlit (Python)
        * **Data Manipulation:** Pandas
        * **Database:** SQLite3
        * **Live Data:** Cricbuzz RapidAPI
        * **Visualizations:** Streamlit Native Charts & UI-Avatars
        """)

    with col2:
        st.markdown("""
        #### 🧭 Navigation Guide
        👈 **Use the sidebar to explore the modules:**
        
        1. **Live Matches:** Real-time scorecards and venue details fetched straight from the API.
        2. **Top Stats:** ICC Rankings and player spotlights visualized cleanly.
        3. **SQL Analytics:** 25+ advanced SQL queries demonstrating complex data extraction.
        4. **CRUD Operations:** An interactive playground to Create, Read, Update, and Delete database records.
        """)

    st.markdown("---")
    st.markdown("""
        #### 📂 Project Folder Structure
        ```text
        CRICBUZZ
        │
        ├── app.py                      # Home Page & Entry Point
        ├── cricket.db                  # SQLite Local Database
        ├── requirements.txt            # Python Dependencies
        │
        ├── pages/                      # Dashboard Modules
        │   ├── 1_Live_Matches.py       
        │   ├── 2_Top_Stats.py          
        │   ├── 3_SQL_Analytics.py      
        │   └── 4_CRUD_Operations.py    
        │
        └── utils/                      # Helper Scripts
            ├── db_connection.py        
            └── generate_mock_data.py
        ```
        """)

with tab_insights:
    st.markdown("""
    ### 💼 Driving Business Strategy with Data
    This dashboard is engineered to generate actionable intelligence across five distinct industries.

    #### 📺 1. Sports Media & Broadcasting
    * **Pre-Match Narratives:** Utilizes historical head-to-head analytics (Q22) to provide commentators with instant rivalry statistics.
    * **Live Context:** Real-time API integration provides live scorecards, while SQL queries (Q24) highlight historical batting partnership success for live broadcasts.

    #### 🎮 2. Fantasy Cricket Platforms
    * **Momentum Tracking:** Employs advanced SQL Window Functions (Q23) to calculate rolling averages (last 5 vs. 10 innings), categorizing players into "Form Buckets" to help users draft the "hot hand."
    * **Venue Targeting:** Analyzes bowler economy rates at specific stadiums (Q14) to optimize fantasy captaincy picks based on match locations.

    #### 📈 3. Cricket Analytics Firms & Franchises
    * **True MVP Valuation:** Features a custom weighted algorithm (Q21) that aggregates batting, bowling, and fielding metrics into a singular "Total Value Score" for draft scouting.
    * **Clutch Performance:** Isolates extreme high-pressure scenarios (matches won by <5 wickets/50 runs) to identify players who consistently perform in the clutch (Q15).

    #### 🎓 4. Educational Institutions
    * **Real-World SQL Curriculum:** Serves as an interactive playground featuring 25 practice queries ranging from basic aggregations to complex Common Table Expressions (CTEs).
    * **Pipeline Demonstration:** Showcases a complete ETL pipeline—from REST API JSON extraction to database UPSERT logic and interactive UI deployment.

    #### 🎲 5. Sports Betting & Prediction
    * **Environmental Odds:** Calculates exact Home vs. Away win ratios (Q12) and Toss Advantage percentages (Q17) to assist algorithms in adjusting live betting lines.
    * **Player Prop Variance:** Calculates the mathematical variance of individual batsmen (Q19) to optimize over/under player prop betting odds.
    """)