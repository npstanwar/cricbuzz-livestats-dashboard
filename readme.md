# 🏏 Cricbuzz LiveStats Dashboard

Cricbuzz LiveStats is a comprehensive cricket analytics dashboard that bridges the gap between real-time data streaming and robust historical SQL analysis.

---

## 🚀 Key Features

### 🔴 Live Matches
- Real-time scorecards, team names, live scores, venues, and formats  
- Smart caching using SQLite (refreshes every 5 minutes)

### 📊 Top Stats
- ICC rankings and player search  
- Clean UI with dynamic avatars

### 🧠 SQL Analytics
- Interactive SQL playground with 25+ queries  
- Includes:
  - CTEs
  - Window functions
  - Advanced filtering

### 🛠 CRUD Operations
- Create, Read, Update, Delete records  
- No backend code required

---

## 💼 Use Cases

- **Sports Media** → Pre-match and live insights  
- **Fantasy Cricket** → Player performance analysis  
- **Analytics Learning** → SQL + Streamlit + API pipeline  
- **Betting Models** → Win probability & trends  

---

## 🧰 Tech Stack

- **Frontend**: Streamlit  
- **Backend**: Python  
- **Database**: SQLite  
- **Data Source**: Cricbuzz RapidAPI  
- **Libraries**: Pandas, Requests  

---

### 📂 Project Structure

```text
Cricbuzz/
├── app.py
├── requirements.txt
├── cricket.db
├── pages/
│   ├── 1_Live_Matches.py
│   ├── 2_Top_Stats.py
│   ├── 3_SQL_Analytics.py
│   └── 4_CRUD_Operations.py
├── utils/
│   ├── db_connection.py
│   └── generate_mock_data.py
└── .streamlit/
