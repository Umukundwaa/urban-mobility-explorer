# 🚕 Urban Mobility Data Explorer

> A fullstack data engineering and visualization project built on 7.6 million real NYC Yellow Taxi trips.
> We clean the raw data, store it in a structured database, serve it through an API, and display it on an interactive dashboard — so anyone can explore how New York City moves.

---

## 🎥 Video Walkthrough
👉 [Click here to watch our 5-minute demo](https://youtu.be/rnV_QDDyIZg)
---

## 🏗️ System Architecture
👉 [Click here to watch our full architecture diagram ](https://drive.google.com/file/d/11ibrQFI9G2c76QvUy9ejxQvccgbNtEfe/view?usp=sharing)
                                                                                    
```

📎 Full architecture diagram: 
<img width="1811" height="1677" alt="NYC System Architecture drawio" src=docs/NYC System Architecture.drawio.png/>

---

## 📖 What Is This Project?

New York City generates millions of taxi trip records every single month. On their own, these records are just rows of numbers — timestamps, distances, fare amounts, location IDs. Nobody can read a spreadsheet with 7 million rows and understand anything useful from it.

This project solves that problem. We take that raw, messy data and turn it into a story anyone can explore:

- **Which neighborhoods generate the most trips?**
- **Does fare per mile change depending on time of day?**
- **What payment methods do NYC taxi riders prefer?**
- **Which times of day are the busiest for taxis?**

We answer all of these through a live, interactive web dashboard backed by a real database and a real API.

---

## 👥 Team
| Name | Role | GitHub Contributions |
|------|------|----------------------|
| Ange Umukundwa | Backend Developer — data pipeline, Flask API, algorithm | `clean_data.py`, `app.py`, all API routes, `top_zones.py` |
| Dan Gisa | Frontend Developer — dashboard, charts, filters | `index.html`, `charts.js`, `filters.js` |
| Prince Hugue | Database design and implementation — schema design, data loading, dump | `schema.sql`, `load_to_db.py`, `dump.sql` |

---

## 🛠️ Tech Stack
| Layer | Technology | Why we chose it |
|-------|-----------|-----------------|
| Data Processing | Python + Pandas | Best library for cleaning large datasets |
| Backend API | Flask (Python) | Lightweight, easy to build REST APIs |
| Database | MySQL | Relational structure fits our linked tables perfectly |
| Frontend | HTML + CSS + JavaScript | No framework needed for this scale |

---

## 📁 Project Structure
```
urban-mobility-explorer/
│
├── README.md                          ← You are here
├── .gitignore                         ← Keeps large files and secrets off GitHub
├── docker-compose.yml                 ← Optional: spin up MySQL with one command
│
├── backend/
│   ├── app.py                         ← Flask server entry point (runs on port 5000)
│   ├── config.py                      ← Reads database credentials from .env
│   ├── requirements.txt               ← All Python packages needed
│   ├── .env.example                   ← Template for your own .env file
│   │
│   ├── data_pipeline/
│   │   ├── clean_data.py              ← Cleans raw CSV, engineers features, logs bad rows
│   │   ├── load_to_db.py              ← Inserts cleaned data into MySQL
│   │   └── data_quality_log.csv       ← Record of all 177k excluded rows and why
│   │
│   ├── database/
│   │   ├── schema.sql                 ← CREATE TABLE statements with indexes
│   │   └── dump.sql                   ← Full database export for easy restore
│   │
│   ├── api/
│   │   ├── trips_routes.py            ← /api/trips endpoints
│   │   ├── zones_routes.py            ← /api/zones endpoints
│   │   └── insights_routes.py         ← /api/insights endpoints
│   │
│   └── algorithms/
│       └── top_zones.py               ← Custom selection sort (no built-in sort used)
│
├── frontend/
│   ├── index.html                     ← Main dashboard page
│   ├── css/style.css                  ← Styling
│   └── js/
│       ├── api.js                     ← Fetch calls to Flask backend
│       ├── charts.js                  ← Chart rendering
│       └── filters.js                 ← Filter and sort UI logic
│
├── data/
│   ├── raw/                           ← Download dataset here (gitignored, too large)
│   │   ├── taxi_zone_lookup.csv       ← Already committed (small file)
│   │   └── taxi_zones.zip             ← Already committed (small file)
│   └── sample/                        ← Cleaned CSV lives here locally (gitignored)
│
└── docs/
    ├── report.pdf                     ← Technical documentation report
    ├── architecture_diagram.png       ← System architecture visual
    └── team_participation_sheet_link.md
```

---

## 📊 Dataset
We use three official NYC Taxi & Limousine Commission (TLC) datasets:

| File | Type | Description |
|------|------|-------------|
| `yellow_tripdata_2019-01.csv` | Fact Table | 7.6M raw trip records — timestamps, distances, fares, location IDs |
| `taxi_zone_lookup.csv` | Dimension Table | Maps location IDs to real zone and borough names |
| `taxi_zones.zip` | Spatial Metadata | Geographic boundaries for each taxi zone (shapefile) |

---

## 🧹 Data Cleaning Summary
Our cleaning pipeline (`clean_data.py`) removed **177,068 bad rows** from the original 7,667,792:

| Rule | Reason |
|------|--------|
| passenger_count = 0 | A trip with no passengers never happened |
| trip_distance ≤ 0 or > 100 miles | Impossible in NYC |
| fare_amount ≤ 0 | Negative or zero fares are data errors |
| total_amount ≤ 0 | Negative totals make no sense |
| RatecodeID not in (1-6) | Only 6 valid rate codes exist |
| congestion_surcharge = NULL | Filled with 0 (pre-policy trips, not missing data) |

All excluded rows are logged in `backend/data_pipeline/data_quality_log.csv` with their reason.

### 3 Derived Features Engineered:
1. **`trip_duration_minutes`** — dropoff time minus pickup time, in minutes
2. **`fare_per_mile`** — fare amount divided by trip distance
3. **`time_of_day`** — morning_rush (6-10am), daytime (10am-4pm), evening_rush (4-8pm), night (8pm-6am)

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL 8.0+ (or MySQL Workbench)
- Git

### Step 1 — Clone the repository
```bash
git clone https://github.com/Umukundwaa/urban-mobility-explorer.git
cd urban-mobility-explorer
```

### Step 2 — Download the raw dataset
The trip data is too large for GitHub. You need to download it manually:
1. Go to your Canvas assignment page
2. Click **"Download Fact Table"** → save as `yellow_tripdata_2019-01.csv`
3. Place it inside `data/raw/`

The other two files (`taxi_zone_lookup.csv` and `taxi_zones.zip`) are already in `data/raw/` in the repo.

### Step 3 — Set up Python environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate

pip install -r backend/requirements.txt
```

### Step 4 — Set up environment variables
```bash
cp backend/.env.example backend/.env
```
Open `backend/.env` and fill in your MySQL credentials:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=urban_mobility
```

### Step 5 — Set up the database
Open MySQL Workbench, connect to your local server, and run:
```sql
CREATE DATABASE IF NOT EXISTS urban_mobility;
USE urban_mobility;
```
Then run the contents of `backend/database/schema.sql`

Or if you want to restore from our full dump:
```bash
mysql -u root -p urban_mobility < backend/database/dump.sql
```

### Step 6 — Clean and load the data
```bash
# From project root
python backend/data_pipeline/clean_data.py
```
Wait for: `Cleaned data saved: 7490724 rows remaining`

```bash
python backend/data_pipeline/load_to_db.py
```
Wait for: `Trips inserted successfully`
⚠️ This may take 10-20 minutes for 7.4 million rows.

### Step 7 — Start the backend
```bash
cd backend
python app.py
```
You should see: `Running on http://127.0.0.1:5000`

### Step 8 — Open the frontend
Open `frontend/index.html` in your browser directly, or use Live Server in VS Code.

---

## 🔌 API Endpoints

### Zones
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/zones` | GET | All 265 taxi zones with borough names |
| `/api/zones/boroughs` | GET | List of 5 NYC boroughs |

### Trips
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/trips` | GET | Trip records (supports filters) |

**Trip filters:**
```
/api/trips?borough=Manhattan
/api/trips?time_of_day=morning_rush
/api/trips?borough=Brooklyn&limit=50
/api/trips?time_of_day=night&limit=100
```

### Insights
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/insights/top-zones` | GET | Top 5 boroughs by trip count (custom algorithm) |
| `/api/insights/avg-fare-by-time` | GET | Average fare and duration by time of day |
| `/api/insights/payment-types` | GET | Payment type breakdown with average tips |

---

## 🧠 Custom Algorithm — Selection Sort for Top Zones

Located in `backend/algorithms/top_zones.py`

We manually implemented a **selection sort** algorithm to rank NYC boroughs by trip count — without using any built-in Python sort functions, `heapq`, or `Counter`.

**How it works:**
1. Loop through all zones
2. Find the one with the highest trip count
3. Swap it to the front
4. Repeat for the remaining items
5. Return the top K results

**Time complexity:** O(n²)
**Space complexity:** O(n)

This satisfies the assignment's requirement for a custom algorithm implementation with no library shortcuts.

---

## 💡 Key Insights From The Data
1. **Manhattan dominates** — generates far more trips than any other borough
2. **Evening rush is most expensive** — highest average fare per trip between 4-8pm
3. **Credit card users tip more** — payment type 1 (credit card) has significantly higher average tips than cash

---

## 📋 Submission Checklist
- [x] GitHub repository with meaningful commit history
- [x] Backend data pipeline (clean + load)
- [x] Normalized MySQL schema with foreign keys and indexes
- [x] Flask API with multiple endpoints and filters
- [x] Custom algorithm (selection sort, no built-in functions)
- [x] Data quality log (177k excluded rows)
- [ ] Frontend dashboard with charts and filters
- [ ] Database dump (dump.sql)
- [ ] PDF technical report (docs/report.pdf)
- [ ] Architecture diagram (docs/architecture_diagram.png)
- [ ] Video walkthrough (5 minutes)
- [ ] Team participation sheet

--

## 📄 Documentation
Full technical report including system architecture, algorithmic analysis, data insights, and reflection is available in `docs/report.pdf`


## Database Dump

The database dump file (dump.sql) is not included in this repository due to its large size (1GB).
You can download it from Google Drive using the link below:

https://drive.google.com/file/d/1t-HCdBhs4MYHVrlV3u68na2LQJLyawlW/view?usp=sharing

To restore the database locally:
1. Make sure MySQL is running in XAMPP
2. Open phpMyAdmin and create a database called urban_mobility
3. Click on urban_mobility, then click the Import tab
4. Upload the dump.sql file and click Go


## Codebase Download

The full codebase zip file is available for download via Google Drive:

https://drive.google.com/file/d/1fe9xKF8ZiPZOnXUCqMeGJNArvGA1HW6B/view?usp=sharing

## Team Participation Sheet

https://docs.google.com/spreadsheets/d/10suewgUe0o7ktnC5matnHS6AtNpQ-qgoYFi7ef6Y4uU/edit?usp=sharing


