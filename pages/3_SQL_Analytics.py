import streamlit as st
import pandas as pd
from utils.db_connection import get_connection
from utils.generate_mock_data import inject_mock_data

st.set_page_config(page_title="SQL Analytics", layout="wide")
st.title("SQL-Driven Analytics")
st.markdown("Explore the database using the 25 built-in SQL practice questions.")

if st.button("🛠️ Initialize Database (Run Once)", type="primary"):
    inject_mock_data()
    st.success("✅ Database populated with high-volume mock data! You can now run all queries.")
    st.rerun()

sql_queries = {
    "Q1: Find all players who represent India": """
        SELECT name, playing_role, batting_style, bowling_style 
        FROM players 
        WHERE country = 'India';
    """,
    "Q2: Show recent matches (Last 30 Days)": """
        SELECT hm.match_desc, hm.team1, hm.team2, 
               v.name || ', ' || v.city AS venue, hm.match_date 
        FROM historical_matches hm 
        JOIN venues v ON hm.venue_id = v.venue_id 
        WHERE hm.match_date >= date('now', '-30 days') 
        ORDER BY hm.match_date DESC;
    """,
    "Q3: Top 10 highest run scorers in ODI cricket": """
        SELECT p.name, c.runs_scored, c.batting_average, c.centuries 
        FROM players p 
        JOIN career_stats c ON p.player_id = c.player_id 
        WHERE c.format = 'ODI' 
        ORDER BY c.runs_scored DESC LIMIT 10;
    """,
    "Q4: Venues with capacity > 50,000": """
        SELECT name, city, country, capacity 
        FROM venues 
        WHERE capacity > 50000 
        ORDER BY capacity DESC;
    """,
    "Q5: Match wins by each team": """
        SELECT winning_team AS team, COUNT(*) AS total_wins 
        FROM historical_matches 
        WHERE winning_team IS NOT NULL 
        GROUP BY winning_team 
        ORDER BY total_wins DESC;
    """,
    "Q6: Player count by playing role": """
        SELECT playing_role, COUNT(*) AS player_count 
        FROM players 
        GROUP BY playing_role;
    """,
    "Q7: Highest individual score in each format": """
        SELECT format, MAX(highest_score) AS highest_score_recorded 
        FROM career_stats 
        GROUP BY format;
    """,
    "Q8: Series started in the year 2024": """
        SELECT series_name, match_format AS match_type, MIN(match_date) AS start_date 
        FROM historical_matches 
        WHERE strftime('%Y', match_date) = '2024' 
        GROUP BY series_name;
    """,
    "Q9: Elite All-rounders (>1000 runs AND >50 wickets)": """
        SELECT p.name, p.country, c.format, c.runs_scored, c.wickets_taken 
        FROM players p 
        JOIN career_stats c ON p.player_id = c.player_id 
        WHERE p.playing_role = 'All-rounder' 
          AND c.runs_scored > 1000 AND c.wickets_taken > 50 
        ORDER BY c.runs_scored DESC;
    """,
    "Q10: Details of the last 20 completed matches": """
        SELECT hm.match_desc, hm.team1, hm.team2, hm.winning_team, 
               hm.victory_margin || ' ' || hm.victory_type AS margin, v.name AS venue 
        FROM historical_matches hm 
        JOIN venues v ON hm.venue_id = v.venue_id 
        WHERE hm.winning_team IS NOT NULL 
        ORDER BY hm.match_date DESC LIMIT 20;
    """,
    "Q11: Compare player performance across formats": """
        SELECT p.name, 
               MAX(CASE WHEN c.format = 'TEST' THEN c.runs_scored ELSE 0 END) AS test_runs, 
               MAX(CASE WHEN c.format = 'ODI' THEN c.runs_scored ELSE 0 END) AS odi_runs, 
               MAX(CASE WHEN c.format = 'T20' THEN c.runs_scored ELSE 0 END) AS t20_runs 
        FROM players p 
        JOIN career_stats c ON p.player_id = c.player_id 
        GROUP BY p.player_id 
        HAVING COUNT(DISTINCT c.format) >= 2;
    """,
    "Q12: Home vs Away win ratio for teams": """
        WITH HomeAway AS (
            SELECT hm.winning_team AS team, 
                   CASE WHEN hm.winning_team = v.country THEN 1 ELSE 0 END AS home_win, 
                   CASE WHEN hm.winning_team != v.country THEN 1 ELSE 0 END AS away_win 
            FROM historical_matches hm 
            JOIN venues v ON hm.venue_id = v.venue_id 
            WHERE hm.winning_team IS NOT NULL
        ) 
        SELECT team, SUM(home_win) AS home_wins, SUM(away_win) AS away_wins 
        FROM HomeAway 
        GROUP BY team;
    """,
    "Q13: Consecutive batting partnerships >= 100 runs": """
        SELECT p1.name AS batter_1, p2.name AS batter_2, 
               bp.partnership_runs, bp.innings 
        FROM batting_partnerships bp 
        JOIN players p1 ON bp.batter1_id = p1.player_id 
        JOIN players p2 ON bp.batter2_id = p2.player_id 
        WHERE bp.partnership_runs >= 100 AND bp.is_consecutive = 1 
        ORDER BY bp.partnership_runs DESC;
    """,
    "Q14: Bowling performance at specific venues": """
        SELECT p.name, v.name AS venue, 
               ROUND(AVG(l.runs_conceded * 1.0 / l.overs_bowled), 2) AS avg_econ, 
               SUM(l.wickets_taken) AS total_wickets, 
               COUNT(l.log_id) AS matches_played 
        FROM player_match_logs l 
        JOIN players p ON l.player_id = p.player_id 
        JOIN venues v ON l.venue_id = v.venue_id 
        WHERE l.overs_bowled >= 4 
        GROUP BY p.player_id, v.venue_id 
        HAVING matches_played >= 3;
    """,
    "Q15: Players in close matches": """
        WITH CloseMatches AS (
            SELECT match_id, winning_team 
            FROM historical_matches 
            WHERE (victory_margin < 50 AND victory_type = 'runs') 
               OR (victory_margin < 5 AND victory_type = 'wickets')
        ) 
        SELECT p.name, ROUND(AVG(l.runs_scored), 2) AS avg_runs, 
               COUNT(l.log_id) AS close_matches_played 
        FROM player_match_logs l 
        JOIN CloseMatches c ON l.match_id = c.match_id 
        JOIN players p ON l.player_id = p.player_id 
        GROUP BY p.player_id;
    """,
    "Q16: Batting performance changes over years (since 2020)": """
        SELECT p.name, strftime('%Y', hm.match_date) AS play_year, 
               ROUND(AVG(l.runs_scored), 2) AS avg_runs, 
               ROUND(AVG(l.strike_rate), 2) AS avg_sr 
        FROM player_match_logs l 
        JOIN historical_matches hm ON l.match_id = hm.match_id 
        JOIN players p ON l.player_id = p.player_id 
        WHERE strftime('%Y', hm.match_date) >= '2020' 
        GROUP BY p.player_id, play_year 
        HAVING COUNT(l.log_id) >= 5;
    """,
    "Q17: Toss advantage analysis": """
        SELECT toss_decision, COUNT(*) AS total_matches, 
               SUM(CASE WHEN toss_winner = winning_team THEN 1 ELSE 0 END) AS wins, 
               ROUND(SUM(CASE WHEN toss_winner = winning_team THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS win_percentage 
        FROM historical_matches 
        WHERE toss_winner IS NOT NULL 
        GROUP BY toss_decision;
    """,
    "Q18: Most economical limited-overs bowlers": """
        SELECT p.name, c.format, c.economy_rate, c.wickets_taken 
        FROM players p 
        JOIN career_stats c ON p.player_id = c.player_id 
        WHERE c.format IN ('ODI', 'T20') 
          AND c.matches_played >= 10 
        ORDER BY c.economy_rate ASC;
    """,
    "Q19: Batsmen consistency (Variance Proxy)": """
        SELECT p.name, ROUND(AVG(l.runs_scored), 2) AS avg_runs, 
               ROUND(AVG(l.runs_scored * l.runs_scored) - (AVG(l.runs_scored) * AVG(l.runs_scored)), 2) AS run_variance 
        FROM player_match_logs l 
        JOIN players p ON l.player_id = p.player_id 
        JOIN historical_matches hm ON l.match_id = hm.match_id 
        WHERE l.balls_faced >= 10 AND strftime('%Y', hm.match_date) >= '2022' 
        GROUP BY p.player_id 
        ORDER BY run_variance ASC;
    """,
    "Q20: Match counts and avg across formats": """
        SELECT p.name, SUM(c.matches_played) AS total_matches, 
               ROUND(AVG(c.batting_average), 2) AS combined_batting_avg 
        FROM players p 
        JOIN career_stats c ON p.player_id = c.player_id 
        GROUP BY p.player_id 
        HAVING total_matches >= 20 
        ORDER BY combined_batting_avg DESC;
    """,
    "Q21: Custom weighted performance ranking": """
        SELECT p.name, c.format, 
               ROUND(((c.runs_scored*0.01) + (c.batting_average*0.5)) + 
                     ((c.wickets_taken*2) + ((50-c.bowling_average)*0.5)) + 
                     ((c.catches*3) + (c.stumpings*5)), 2) AS total_score 
        FROM players p 
        JOIN career_stats c ON p.player_id = c.player_id 
        ORDER BY total_score DESC;
    """,
    "Q22: Head-to-head match prediction": """
        SELECT hm.team1, hm.team2, COUNT(*) AS total_matches, 
               SUM(CASE WHEN hm.winning_team = hm.team1 THEN 1 ELSE 0 END) AS t1_wins, 
               SUM(CASE WHEN hm.winning_team = hm.team2 THEN 1 ELSE 0 END) AS t2_wins 
        FROM historical_matches hm 
        WHERE hm.match_date >= date('now', '-3 years') 
        GROUP BY hm.team1, hm.team2 
        HAVING total_matches >= 5;
    """,
    "Q23: Recent player form & momentum": """
        WITH Recent AS (
            SELECT player_id, runs_scored, 
                   ROW_NUMBER() OVER(PARTITION BY player_id ORDER BY log_id DESC) AS rn 
            FROM player_match_logs
        ), Form AS (
            SELECT player_id, 
                   AVG(CASE WHEN rn <= 5 THEN runs_scored END) AS avg_5, 
                   AVG(runs_scored) AS avg_10 
            FROM Recent 
            WHERE rn <= 10 
            GROUP BY player_id
        ) 
        SELECT p.name, ROUND(f.avg_5, 2) as avg_last_5, ROUND(f.avg_10, 2) as avg_last_10, 
               CASE WHEN f.avg_5 >= 50 AND f.avg_5 > f.avg_10 THEN 'Excellent Form' 
                    WHEN f.avg_5 >= 30 THEN 'Good Form' 
                    ELSE 'Average Form' END AS status 
        FROM Form f 
        JOIN players p ON f.player_id = p.player_id;
    """,
    "Q24: Successful batting partnerships": """
        SELECT p1.name AS batter_1, p2.name AS batter_2, 
               ROUND(AVG(bp.partnership_runs), 2) AS avg_runs, 
               SUM(CASE WHEN bp.partnership_runs > 50 THEN 1 ELSE 0 END) AS fifty_plus_stands 
        FROM batting_partnerships bp 
        JOIN players p1 ON bp.batter1_id = p1.player_id 
        JOIN players p2 ON bp.batter2_id = p2.player_id 
        WHERE bp.is_consecutive = 1 
        GROUP BY batter_1, batter_2 
        HAVING COUNT(*) >= 5 
        ORDER BY avg_runs DESC;
    """,
    "Q25: Time-series analysis (Quarterly)": """
        SELECT p.name, 
               strftime('%Y', hm.match_date) || '-Q' || ((CAST(strftime('%m', hm.match_date) AS INTEGER) + 2) / 3) AS quarter, 
               ROUND(AVG(l.runs_scored), 2) AS qtr_avg 
        FROM player_match_logs l 
        JOIN historical_matches hm ON l.match_id = hm.match_id 
        JOIN players p ON l.player_id = p.player_id 
        GROUP BY p.player_id, quarter 
        ORDER BY p.name, quarter;
    """
}

query_names = list(sql_queries.keys())

if 'query_idx' not in st.session_state:
    st.session_state.query_idx = 0

col1, col2, col3 = st.columns([1, 8, 1])

with col1:
    if st.button("⬅️ Prev", use_container_width=True):
        st.session_state.query_idx = (st.session_state.query_idx - 1) % len(query_names)

with col3:
    if st.button("Next ➡️", use_container_width=True):
        st.session_state.query_idx = (st.session_state.query_idx + 1) % len(query_names)

with col2:
    selected_q = st.selectbox(
        "Select an Analytical Query:",
        options=query_names,
        index=st.session_state.query_idx,
        label_visibility="collapsed"
    )
    st.session_state.query_idx = query_names.index(selected_q)

st.markdown("---")

st.subheader("📝 SQL Query")
st.code(sql_queries[selected_q], language="sql")
st.markdown("<br>", unsafe_allow_html=True)

st.subheader("📊 Query Results")
try:
    conn = get_connection()
    result_df = pd.read_sql_query(sql_queries[selected_q], conn)
    conn.close()
    
    if result_df.empty:
        st.warning("Query executed successfully, but returned 0 rows.")
    else:
        st.caption(f"Rows returned: {len(result_df)}")
        st.dataframe(result_df, hide_index=True, use_container_width=True)
except Exception as e:
    st.error(f"SQL Execution Error: {e}")