import sqlite3
import random
from datetime import datetime, timedelta

def inject_mock_data():
    conn = sqlite3.connect("cricket.db")
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS players (player_id INTEGER PRIMARY KEY, name TEXT, country TEXT, playing_role TEXT, batting_style TEXT, bowling_style TEXT);
    CREATE TABLE IF NOT EXISTS venues (venue_id INTEGER PRIMARY KEY, name TEXT, city TEXT, country TEXT, capacity INTEGER);
    CREATE TABLE IF NOT EXISTS career_stats (stat_id INTEGER PRIMARY KEY, player_id INTEGER, format TEXT, matches_played INTEGER, runs_scored INTEGER, highest_score INTEGER, batting_average REAL, centuries INTEGER, wickets_taken INTEGER, bowling_average REAL, economy_rate REAL, catches INTEGER, stumpings INTEGER);
    CREATE TABLE IF NOT EXISTS historical_matches (match_id INTEGER PRIMARY KEY, match_desc TEXT, series_name TEXT, team1 TEXT, team2 TEXT, winning_team TEXT, victory_margin INTEGER, victory_type TEXT, venue_id INTEGER, match_date DATE, match_format TEXT, toss_winner TEXT, toss_decision TEXT);
    CREATE TABLE IF NOT EXISTS player_match_logs (log_id INTEGER PRIMARY KEY, player_id INTEGER, match_id INTEGER, venue_id INTEGER, runs_scored INTEGER, balls_faced INTEGER, strike_rate REAL, overs_bowled REAL, runs_conceded INTEGER, wickets_taken INTEGER);
    CREATE TABLE IF NOT EXISTS batting_partnerships (partnership_id INTEGER PRIMARY KEY, match_id INTEGER, innings INTEGER, batter1_id INTEGER, batter2_id INTEGER, partnership_runs INTEGER, is_consecutive BOOLEAN);
    
    DELETE FROM players; DELETE FROM venues; DELETE FROM career_stats; 
    DELETE FROM historical_matches; DELETE FROM player_match_logs; DELETE FROM batting_partnerships;
    """)

    # Base Players & Venues
    players = [
        (1, 'Virat Kohli', 'India', 'Batsman', 'Right-hand bat', 'Right-arm medium'),
        (2, 'Jasprit Bumrah', 'India', 'Bowler', 'Right-hand bat', 'Right-arm fast'),
        (3, 'Ravindra Jadeja', 'India', 'All-rounder', 'Left-hand bat', 'Slow left-arm orthodox'),
        (4, 'Steve Smith', 'Australia', 'Batsman', 'Right-hand bat', 'Legbreak googly'),
        (5, 'Pat Cummins', 'Australia', 'Bowler', 'Right-hand bat', 'Right-arm fast'),
        (6, 'Ben Stokes', 'England', 'All-rounder', 'Left-hand bat', 'Right-arm fast-medium')
    ]
    cursor.executemany("INSERT INTO players VALUES (?,?,?,?,?,?)", players)

    venues = [(1, 'Narendra Modi Stadium', 'Ahmedabad', 'India', 132000), (2, 'MCG', 'Melbourne', 'Australia', 100024)]
    cursor.executemany("INSERT INTO venues VALUES (?,?,?,?,?)", venues)

    # Inflate Career Stats to pass minimum thresholds
    stats = [
        (1, 1, 'ODI', 292, 13848, 183, 58.67, 50, 5, 166.25, 6.22, 150, 0),
        (5, 1, 'T20', 115, 4008, 122, 52.7, 1, 4, 51.0, 8.1, 50, 0),
        (6, 1, 'TEST', 111, 8676, 254, 49.2, 29, 0, 0.0, 0.0, 110, 0),
        (2, 2, 'ODI', 100, 500, 20, 10.0, 0, 150, 24.3, 4.5, 30, 0),
        (3, 3, 'ODI', 150, 2500, 80, 32.4, 0, 200, 30.5, 4.9, 70, 0),
        (4, 4, 'TEST', 109, 9685, 239, 56.9, 32, 19, 54.1, 3.4, 150, 0)
    ]
    cursor.executemany("INSERT INTO career_stats VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", stats)

    # AUTO-GENERATE 50 MATCHES to satisfy advanced queries
    base_date = datetime.now() - timedelta(days=800)
    for i in range(1, 51):
        m_date = (base_date + timedelta(days=i*16)).strftime('%Y-%m-%d')
        # Ensure some close matches and specific teams
        margin = random.choice([2, 3, 4, 10, 55]) 
        v_type = 'wickets' if margin < 10 else 'runs'
        t1, t2 = ('India', 'Australia') if i % 2 == 0 else ('India', 'England')
        winner = t1 if i % 3 == 0 else t2
        cursor.execute("INSERT INTO historical_matches VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       (i, f'Match {i}', 'Test Series 2024', t1, t2, winner, margin, v_type, 1, m_date, 'ODI', t1, 'Bat'))
        
        # Give Kohli and Bumrah a log for every match
        cursor.execute("INSERT INTO player_match_logs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       (i*2, 1, i, 1, random.randint(10, 120), random.randint(15, 100), 110.5, 0, 0, 0))
        cursor.execute("INSERT INTO player_match_logs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       (i*2+1, 2, i, 1, 0, 0, 0, 10.0, random.randint(30, 60), random.randint(1, 4)))

        # Give Kohli and Jadeja 10 large partnerships to satisfy Q24
        if i <= 10:
            cursor.execute("INSERT INTO batting_partnerships VALUES (?, ?, ?, ?, ?, ?, ?)", 
                           (i, i, 1, 1, 3, random.randint(60, 150), True))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    inject_mock_data()