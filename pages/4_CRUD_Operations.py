import streamlit as st
import pandas as pd
from utils.db_connection import get_connection

st.set_page_config(page_title="Data Management", layout="wide")
st.title("⚙️ Administrative Data Management")
st.markdown("Perform Create, Read, Update, and Delete (CRUD) operations on the Player database.")

tab_create, tab_read, tab_update, tab_delete = st.tabs(["🟢 Create", "📖 Read", "🟡 Update", "🔴 Delete"])


# CREATE
with tab_create:
    st.subheader("Add a New Player")
    with st.form("create_player_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Player Name*")
            new_country = st.text_input("Country*")
            new_role = st.selectbox("Playing Role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
        with col2:
            new_bat = st.selectbox("Batting Style", ["Right-hand bat", "Left-hand bat"])
            new_bowl = st.text_input("Bowling Style (e.g., Right-arm fast)")
            
        submitted = st.form_submit_button("➕ Add Player to Database", type="primary")
        
        if submitted:
            if not new_name or not new_country:
                st.error("Name and Country are required fields!")
            else:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO players (name, country, playing_role, batting_style, bowling_style) 
                        VALUES (?, ?, ?, ?, ?)
                    """, (new_name, new_country, new_role, new_bat, new_bowl))
                    conn.commit()
                    conn.close()
                    st.success(f"Successfully added {new_name} to the database!")
                except Exception as e:
                    st.error(f"Database Error: {e}")

# ==========================================
# READ
# ==========================================
with tab_read:
    st.subheader("Player Directory")
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("🔄 Refresh Directory", use_container_width=True)
        
    try:
        conn = get_connection()
        df_players = pd.read_sql_query("SELECT * FROM players ORDER BY player_id DESC", conn)
        conn.close()
        
        with col1:
            search_term = st.text_input("🔍 Search by Player Name or Country:", placeholder="e.g., Virat Kohli or India")
            if search_term:
                df_players = df_players[
                    df_players['name'].str.contains(search_term, case=False, na=False) | 
                    df_players['country'].str.contains(search_term, case=False, na=False)
                ]
                
        if not df_players.empty:
            df_players['Avatar'] = df_players['name'].apply(
                lambda x: f"https://ui-avatars.com/api/?name={x.replace(' ', '+')}&background=262730&color=00A86B&rounded=true"
            )
            
            cols = ['Avatar', 'player_id', 'name', 'country', 'playing_role', 'batting_style', 'bowling_style']
            df_players = df_players[cols]
            
            st.dataframe(
                df_players,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Avatar": st.column_config.ImageColumn("Profile"),
                    "player_id": st.column_config.NumberColumn("ID", format="%d"),
                    "name": st.column_config.TextColumn("Player Name", width="medium"),
                    "country": st.column_config.TextColumn("Country"),
                    "playing_role": st.column_config.TextColumn("Role"),
                    "batting_style": st.column_config.TextColumn("Batting Style"),
                    "bowling_style": st.column_config.TextColumn("Bowling Style")
                }
            )
        else:
            st.info("No players found in the database. Add some in the Create tab!")
            
    except Exception as e:
        st.error(f"Error loading data: {e}")

# ==========================================
# UPDATE

with tab_update:
    st.subheader("Update Player Information")
    if not df_players.empty:
        player_dict = dict(zip(df_players['name'] + " (" + df_players['country'] + ")", df_players['player_id']))
        selected_player_str = st.selectbox("Select Player to Edit:", options=list(player_dict.keys()))
        
        if selected_player_str:
            selected_id = player_dict[selected_player_str]
            current_details = df_players[df_players['player_id'] == selected_id].iloc[0]
            
            with st.form("update_player_form"):
                st.info(f"Editing Database ID: {selected_id}")
                upd_name = st.text_input("Name", value=current_details['name'])
                upd_country = st.text_input("Country", value=current_details['country'])
                
                roles = ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"]
                current_role_idx = roles.index(current_details['playing_role']) if current_details['playing_role'] in roles else 0
                upd_role = st.selectbox("Playing Role", roles, index=current_role_idx)
                
                bat_styles = ["Right-hand bat", "Left-hand bat"]
                current_bat_idx = bat_styles.index(current_details['batting_style']) if current_details['batting_style'] in bat_styles else 0
                upd_bat = st.selectbox("Batting Style", bat_styles, index=current_bat_idx)
                
                upd_bowl = st.text_input("Bowling Style", value=current_details['bowling_style'])
                
                if st.form_submit_button("💾 Save Changes"):
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("""
                            UPDATE players 
                            SET name=?, country=?, playing_role=?, batting_style=?, bowling_style=? 
                            WHERE player_id=?
                        """, (upd_name, upd_country, upd_role, upd_bat, upd_bowl, selected_id))
                        conn.commit()
                        conn.close()
                        st.success(f"Successfully updated {upd_name}'s profile!")
                        st.rerun() 
                    except Exception as e:
                        st.error(f"Error updating record: {e}")

# DELETE
with tab_delete:
    st.subheader("Remove a Player")
    st.warning("⚠️ Warning: Deleting a player cannot be undone. It may also affect their historical match logs if cascade delete isn't enabled.")
    
    if not df_players.empty:
        del_player_dict = dict(zip(df_players['name'] + " (" + df_players['country'] + ")", df_players['player_id']))
        del_selected_player_str = st.selectbox("Select Player to Delete:", options=list(del_player_dict.keys()), key="del_select")
        
        if del_selected_player_str:
            del_selected_id = del_player_dict[del_selected_player_str]
            
            if st.button("🗑️ Permanently Delete Player", type="primary"):
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM players WHERE player_id=?", (del_selected_id,))
                    conn.commit()
                    conn.close()
                    st.success(f"Player deleted successfully from the database.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting record: {e}")