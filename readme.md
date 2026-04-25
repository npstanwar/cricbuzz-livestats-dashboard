🏏 Cricbuzz LiveStats
Cricbuzz LiveStats is a comprehensive cricket analytics dashboard that bridges the gap between real-time data streaming and robust historical SQL analysis. Moving beyond static CSV files, this dynamic, interactive web platform provides unparalleled insights into the game of cricket.

🌟 Key Features
Live Matches: Delivers real-time scorecards, team names, live scores, venues, and formats. It uses an intelligent caching mechanism to serve SQLite data if it is less than 5 minutes old, protecting the free tier API quota.
Top Stats: Features global ICC Rankings and a Player Search tool utilizing dynamic ui-avatars for a sleek, color-coordinated professional aesthetic.
SQL Analytics: An interactive SQL playground containing over 25 advanced queries. It showcases everything from basic filtering to advanced techniques like Common Table Expressions (CTEs), window functions, and custom weighted performance algorithms to rank players.
CRUD Operations: A dedicated form-based UI module allowing administrative users to Create, Read, Update, and Delete database records seamlessly without touching the backend code.

💼 Business Insights & Value
This dashboard translates raw data into actionable strategy for various industries:
Sports Media & Broadcasting: Commentators can use historical rivalry data and batting partnership success rates (averages) to create in-game context and pre-match narratives for live television.
Fantasy Cricket Platforms: Utilizes SQL Window Functions to calculate rolling averages, instantly identifying which players are currently in "Excellent Form" to aid in drafting decisions.
Team Management & Analytics Firms: Engineers a custom "Total Score" metric combining batting runs, bowling economy, and fielding points to identify true multi-dimensional MVPs. It also isolates matches won by tight margins to scout "clutch" performers.
Sports Betting: Analyzes exact win ratios for teams playing Home vs. Away and evaluates the "Toss Advantage" to help betting algorithms calculate live environmental odds.
Educational Institutions (EdTech): Serves as a full Extract, Transform, Load (ETL) pipeline teaching tool that demonstrates pulling nested JSON from an API, flattening it in Python, inserting it into SQLite, and building a Streamlit UI.

🛠️ Tools & Technologies
Frontend: Streamlit (Python)
Data Manipulation: Pandas
Database: SQLite3
Live Data: Cricbuzz RapidAPI

📂 Project Folder Structure
Plaintext
CRICBUZZ/
│
├── app.py # Home Page & Entry Point [cite: 107]
├── cricket.db # SQLite Local Database [cite: 107]
├── requirements.txt # Python Dependencies [cite: 107]
│
├── pages/ # Dashboard Modules [cite: 107]
│ ├── 1_Live_Matches.py [cite: 107]
│ ├── 2_Top_Stats.py [cite: 107]
│ ├── 3_SQL_Analytics.py [cite: 108]
│ └── 4_CRUD_Operations.py [cite: 108]
│
└── utils/ # Helper Scripts [cite: 108]
├── db_connection.py [cite: 108]
└── generate_mock_data.py [cite: 108]

🚀 Setup Instructions
Follow these step-by-step instructions to get the application running from scratch.

1. Install Dependencies
   Install the necessary Python libraries (like Streamlit, Pandas, and Requests) using the included requirements file.
   Bash
   pip install -r requirements.txt

2. API Key Configuration
   Because this dashboard pulls live match data from the Cricbuzz RapidAPI, you must securely configure your own access to avoid hardcoding your key.
   Get a free RapidAPI key from Cricbuzz.
   Create a hidden folder named .streamlit in the root directory of this project.
   Inside that folder, create a file named secrets.toml to securely store your key.
   Add the following code to the secrets.toml file:
   Ini, TOML
   RAPIDAPI_KEY = "your_api_key_here"

3. Run the Application
   Launch the dashboard locally using the exact Streamlit terminal command:
   Bash
   streamlit run app.py
