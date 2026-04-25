import sqlite3
import streamlit as st

def get_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect("cricket.db", check_same_thread=False)
    return conn

def init_db():
    """Initializes the database with the correct schema."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # The complete schema we figured out earlier
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        match_id INTEGER PRIMARY KEY,
        match_type TEXT,
        match_format TEXT,
        series_name TEXT,
        venue TEXT,
        team1 TEXT,
        team2 TEXT,
        team1_runs INTEGER,
        team1_wickets INTEGER,
        team2_runs INTEGER,
        team2_wickets INTEGER,
        status TEXT,
        last_updated TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()