# 🏏 Cricbuzz LiveStats Dashboard

### Real-time Cricket Analytics using Streamlit + SQL

Cricbuzz LiveStats is an interactive analytics dashboard that combines **live cricket data** with **historical SQL-based analysis** in a single unified interface. It eliminates the gap between real-time match tracking and deeper performance insights.

---

## 🌐 Live App

https://cricbuzz-livestats-dashboard.streamlit.app/

---

## 🎯 Problem

Most cricket platforms either:

* Show **live scores only**, OR
* Provide **static historical stats**

They do not combine both effectively.

This project solves that by integrating:

* Live API data
* Local SQL analytics
* Interactive dashboards

---

## 🚀 Key Features

### 🔴 Live Matches

* Real-time scorecards, teams, venues, formats
* Smart caching using SQLite (refresh every 5 minutes)

### 📊 Top Stats

* ICC rankings and player search
* Clean UI with dynamic visuals

### 🧠 SQL Analytics

* Interactive SQL playground (25+ queries)
* Supports:

  * CTEs
  * Window functions
  * Advanced filtering

### 🛠 CRUD Operations

* Create, Read, Update, Delete records
* No backend coding required

---

## 💼 Use Cases

* **Sports Media** → Pre-match and live insights
* **Fantasy Cricket** → Player performance tracking
* **Analytics Learning** → SQL + API + Streamlit pipeline
* **Betting Models** → Win probability and trend analysis

---

## 🧰 Tech Stack

* **Frontend**: Streamlit
* **Backend**: Python
* **Database**: SQLite
* **API**: Cricbuzz RapidAPI
* **Libraries**: Pandas, Requests

---

## 📸 Screenshots

```markdown
<img width="1555" height="814" alt="image" src="https://github.com/user-attachments/assets/ab237a6f-6fd4-46f6-bc17-c6d22612456f" />

<img width="1532" height="872" alt="image" src="https://github.com/user-attachments/assets/a669e4b1-6186-4c7a-b3b1-d30941c2040e" />

```

---

## 📁 Project Structure

```
Cricbuzz/
│
├── app.py
├── requirements.txt
├── pages/
│   ├── 1_Live_Matches.py
│   ├── 2_Top_Stats.py
│   ├── 3_SQL_Analytics.py
│   └── 4_CRUD_Operations.py
├── utils/
│   ├── db_connection.py
│   └── generate_mock_data.py
└── .streamlit/
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/npstanwar/cricbuzz-livestats-dashboard.git
cd cricbuzz-livestats-dashboard
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

---

## 🔐 API Key Setup

Create a file:

```
.streamlit/secrets.toml
```

Add:

```toml
API_KEY = "your_api_key_here"
```

⚠️ Do NOT commit this file to GitHub.

---

## 🗄 Database Note

* SQLite database is **generated dynamically**
* No need to manually add `cricket.db`
* Ensures compatibility with Streamlit Cloud

---

## ☁️ Deployment

Deployed using **Streamlit Community Cloud**

Steps:

1. Push code to GitHub
2. Go to https://share.streamlit.io/
3. Select repo and `app.py`
4. Add secrets in dashboard
5. Deploy

---

## ⚠️ Important Notes

* Do NOT commit:

  * `venv/`
  * `__pycache__/`
  * `.streamlit/secrets.toml`
* Ensure `requirements.txt` is updated
* Avoid hardcoded file paths

---

## 📌 Future Improvements

* Add user authentication
* Replace SQLite with cloud DB (PostgreSQL)
* Improve UI/UX with advanced components
* Add caching optimization

---

## 👤 Author

**Nishant Pratap Singh**
GitHub: https://github.com/npstanwar

Give the repo a star — it helps visibility.
