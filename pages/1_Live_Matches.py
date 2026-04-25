import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from utils.db_connection import get_connection

st.set_page_config(page_title="Live Matches", layout="wide")
st.title("📡 Live Match Updates")

# Initialize database schema
conn = get_connection()
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        match_id INTEGER PRIMARY KEY,
        match_type TEXT,
        match_format TEXT,
        series_name TEXT,
        venue TEXT,
        team1 TEXT,
        team2 TEXT,
        team1_runs REAL,
        team1_wickets REAL,
        team1_overs REAL,
        team2_runs REAL,
        team2_wickets REAL,
        team2_overs REAL,
        status TEXT,
        last_updated TIMESTAMP
    )
""")
conn.commit()
conn.close()

def fetch_and_store_data():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
    headers = {
        "x-rapidapi-key": st.secrets["RAPIDAPI_KEY"],
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        remaining_quota = response.headers.get("x-ratelimit-requests-remaining")
        if remaining_quota is not None:
            st.sidebar.info(f"API Requests Remaining: **{remaining_quota}**")
        
        data = response.json()
        matches_data = []
        now = datetime.now()

        for type_match in data.get("typeMatches", []):
            m_type = type_match.get("matchType")
            for series in type_match.get("seriesMatches", []):
                s_wrapper = series.get("seriesAdWrapper")
                if not s_wrapper: continue
                
                s_name = s_wrapper.get("seriesName")
                for match in s_wrapper.get("matches", []):
                    info = match.get("matchInfo", {})
                    score = match.get("matchScore", {})
                    
                    venue = f"{info.get('venueInfo', {}).get('ground')}, {info.get('venueInfo', {}).get('city')}"
                    
                    matches_data.append((
                        info.get("matchId"), m_type, info.get("matchFormat"),
                        s_name, venue, info.get("team1", {}).get("teamName"),
                        info.get("team2", {}).get("teamName"),
                        score.get("team1Score", {}).get("inngs1", {}).get("runs"),
                        score.get("team1Score", {}).get("inngs1", {}).get("wickets"),
                        score.get("team1Score", {}).get("inngs1", {}).get("overs"),
                        score.get("team2Score", {}).get("inngs1", {}).get("runs"),
                        score.get("team2Score", {}).get("inngs1", {}).get("wickets"),
                        score.get("team2Score", {}).get("inngs1", {}).get("overs"),
                        info.get("status"), now
                    ))

        conn = get_connection()
        cursor = conn.cursor()
        cursor.executemany("""
            INSERT OR REPLACE INTO matches VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, matches_data)
        conn.commit()
        conn.close()
        st.toast("Live scores updated!", icon="✅")
    except Exception as e:
        st.error(f"API Error: {e}")

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🔄 Refresh", use_container_width=True):
        fetch_and_store_data()

st.markdown("---")

conn = get_connection()
df = pd.read_sql_query("SELECT * FROM matches", conn)
conn.close()

if not df.empty:
    st.sidebar.header("🎯 Filter Matches")
    
    formats = df['match_format'].dropna().unique()
    selected_formats = st.sidebar.multiselect("🏏 Match Format", options=formats, default=[])
    
    series_list = df['series_name'].dropna().unique()
    selected_series = st.sidebar.multiselect("🏆 Series / League", options=series_list, default=[])
    
    filtered_df = df.copy()
    
    if selected_formats:
        filtered_df = filtered_df[filtered_df['match_format'].isin(selected_formats)]
        
    if selected_series:
        filtered_df = filtered_df[filtered_df['series_name'].isin(selected_series)]
    
    if filtered_df.empty:
        st.warning("No matches match your current filter criteria.")
    else:
        types = filtered_df['match_type'].dropna().unique()
        tabs = st.tabs(list(types))
        
        for i, tab in enumerate(tabs):
            with tab:
                tab_df = filtered_df[filtered_df['match_type'] == types[i]]
                
                for _, row in tab_df.iterrows():
                    with st.container(border=True):
                        st.caption(f"🏆 **{row['series_name']}** • {row['match_format']} • 📍 {row['venue']}")
                        
                        # Team 1
                        if pd.notna(row.get('team1_runs')):
                            r1 = int(row['team1_runs'])
                            w1 = int(row['team1_wickets']) if pd.notna(row.get('team1_wickets')) else 0
                            t1_score = f"{r1}/{w1}"
                            if pd.notna(row.get('team1_overs')):
                                t1_score += f" ({row['team1_overs']} Ovs)"
                        else:
                            t1_score = "Yet to bat"
                            
                        # Team 2
                        if pd.notna(row.get('team2_runs')):
                            r2 = int(row['team2_runs'])
                            w2 = int(row['team2_wickets']) if pd.notna(row.get('team2_wickets')) else 0
                            t2_score = f"{r2}/{w2}"
                            if pd.notna(row.get('team2_overs')):
                                t2_score += f" ({row['team2_overs']} Ovs)"
                        else:
                            t2_score = "Yet to bat"
                        
                        col3, col4 = st.columns([3, 1])
                        with col3:
                            st.markdown(f"#### {row['team1']}")
                        with col4:
                            st.markdown(f"<h4 style='text-align: right; color: #00A86B;'>{t1_score}</h4>", unsafe_allow_html=True)
                            
                        col5, col6 = st.columns([3, 1])
                        with col5:
                            st.markdown(f"#### {row['team2']}")
                        with col6:
                            st.markdown(f"<h4 style='text-align: right; color: #00A86B;'>{t2_score}</h4>", unsafe_allow_html=True)
                            
                        st.markdown("---")
                        st.info(f"**{row['status']}**")
else:
    st.info("No live matches in the database. Click Refresh.")