import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Top Stats", layout="wide")
st.title("📊 Top Stats & Player Spotlight")

headers = {
    "x-rapidapi-key": st.secrets["RAPIDAPI_KEY"],
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

tab1, tab2 = st.tabs(["🏆 Global ICC Rankings", "🔍 Player Search"])

with tab1:
    st.subheader("Current ICC Rankings")
    
    col1, col2 = st.columns(2)
    with col1:
        format_choice = st.selectbox("Match Format", ["test", "odi", "t20"])
    with col2:
        category_choice = st.selectbox("Ranking Category", ["batsmen", "bowlers", "allrounders"])
        
    if st.button("Fetch Rankings", type="primary"):
        url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/{category_choice}"
        querystring = {"formatType": format_choice}
        
        with st.spinner("Fetching global rankings..."):
            try:
                response = requests.get(url, headers=headers, params=querystring)
                response.raise_for_status()
                data = response.json()
                
                rankings = data.get("rank", [])
                
                if not rankings:
                    st.warning("No rankings found for this selection at the moment.")
                else:
                    st.markdown("### Top 10 Leaderboard")
                    chart_data = pd.DataFrame(
                        [(p.get('name'), int(p.get('rating', 0))) for p in rankings[:10]],
                        columns=['Player', 'Rating']
                    ).set_index('Player')
                    
                    st.markdown("#### 📈 Rating Visualization")
                    st.bar_chart(chart_data, color="#00A86B")
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    for player in rankings[:10]:
                        with st.container(border=True):
                            c1, c2, c3, c4 = st.columns([1, 1, 3, 1])
                            
                            with c1:
                                st.markdown(f"### #{player.get('rank')}")
                                
                            with c2:
                                player_name = player.get('name', 'Unknown')
                                formatted_name = player_name.replace(" ", "+")
                                img_url = f"https://ui-avatars.com/api/?name={formatted_name}&background=262730&color=00A86B&size=150&font-size=0.4&bold=true"
                                st.image(img_url, width=60)
                                    
                            with c3:
                                st.markdown(f"**{player.get('name')}**")
                                st.caption(f"Country: {player.get('country')}")
                                
                            with c4:
                                st.markdown(f"**Rating:** {player.get('rating')}")
                                
            except Exception as e:
                st.error(f"Error fetching rankings: {e}")

with tab2:
    st.subheader("Player Spotlight")
    
    search_query = st.text_input("Search for any player (e.g., Virat Kohli, Rashid Khan)", placeholder="Enter player name...")
    
    if st.button("Search Player", type="primary"):
        if search_query:
            url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"
            querystring = {"plrN": search_query}
            
            with st.spinner(f"Searching for {search_query}..."):
                try:
                    response = requests.get(url, headers=headers, params=querystring)
                    response.raise_for_status()
                    data = response.json()
                    
                    players = data.get("player", [])
                    
                    if not players:
                        st.warning("No players found. Try checking the spelling!")
                    else:
                        for p in players:
                            with st.container(border=True):
                                c1, c2 = st.columns([1, 5])
                                
                                player_name = p.get('name', 'Unknown')
                                formatted_name = player_name.replace(" ", "+")
                                img_url = f"https://ui-avatars.com/api/?name={formatted_name}&background=262730&color=00A86B&size=150&font-size=0.4&bold=true"
                                
                                with c1:
                                    st.image(img_url, width=80)
                                
                                with c2:
                                    st.subheader(p.get("name"))
                                    st.write(f"**Team:** {p.get('teamName')}")
                                    
                except Exception as e:
                    st.error(f"Error searching for player: {e}")