# Apple Watch Smart Data Analysis (EDA + Visualizations)

Analyze Apple Watch / fitness data to understand activity patterns, cardio response, and relationships across steps, heart rate, calories, and distance.

## 🔍 Summary

- **Goal:** Exploratory data analysis & clear visualizations for health/activity metrics.
- **Data:** Apple Watch / Fitbit–like CSVs; combined and cleaned into `clean_apple_watch.csv`.
- **Notebook:** `notebooks/AppleWatch_EDA.ipynb` (Colab-ready, cell-by-cell).

### Key Insights (from current run)
- Top activities by avg steps: **Running 7 METs (140)**, **Sitting (132)**, **Running 5 METs (112)**
- Top activities by avg heart rate: **Running 7 METs (97.8 bpm)**, **Running 5 METs (91.1 bpm)**, **Running 3 METs (85.1 bpm)**
- Correlation between steps and heart rate: **0.16 (Pearson)**  
  *Note:* The high steps under “Sitting” suggests possible label noise or blended windows; see “Data Quality Notes”.

---

## 🗂️ Data Dictionary (post-cleaning)

The notebook standardizes column names:
- `steps` — step count (unitless)
- `heart_rate` — instantaneous/avg HR (bpm)
- `calories` — energy estimate
- `distance` — distance covered
- `entropy_heart`, `entropy_steps` — signal entropy features
- `resting_heart` — resting heart rate (bpm)
- `corr_heart_steps` — correlation (windowed) between HR & steps
- `normalized_heart_rate` — normalized HR index
- `intensity_karvonen` — effort via Karvonen formula index
- `sd_normalized_heart_rate` — std. dev. of normalized HR
- `steps_x_distance` — interaction feature
- `activity` — activity label (e.g., Running 7 METs, Sitting, Walking…)
- `device`, `gender`, `age`, `height`, `weight`

The cleaner also fixes common typos (e.g., `hear_rate` → `heart_rate`, `entropy_setps` → `entropy_steps`) and drops `Unnamed:*` columns.

---

## 🧪 Reproduce Locally

### 1) Create env & install deps
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
