# MCA Insights Engine

MCA Insights Engine is a Python application designed to consolidate, track, enrich, and visualize company master data from the Ministry of Corporate Affairs (MCA), as published on [data.gov.in](https://data.gov.in). The application transforms raw, state-wise CSV files into an interactive, AI-powered dashboard for compliance, credit assessment, and risk monitoring.

---

## 🚀 Features

- **Data Consolidation:**  
  Merges and cleans raw company data from multiple state-wise CSV files into a single, canonical master dataset.

- **Data Enrichment:**  
  Gathers supplementary information (like Director Names and full addresses) for a sample of companies from public sources (e.g., ZaubaCorp).

- **Interactive Dashboard:**  
  A web-based interface built with Streamlit that allows users to:
  - Search for companies by CIN or Name.
  - Filter the dataset by State, Company Status, and Year of Incorporation.
  - View detailed company information and enriched data.
  - Visualize a company's change history over time.

- **AI-Powered Summaries:**  
  Automatically generates a concise daily summary report highlighting key changes and trends found in the data logs.

---

## 🛠️ Tech Stack

- **Language:** Python 3.x  
- **Data Manipulation:** Pandas  
- **Web Dashboard:** Streamlit  
- **Data Visualization:** Plotly Express  
- **Web Scraping (Optional):** BeautifulSoup4, Playwright/Selenium  

---

## 🔄 Data Workflow

1. **Raw Data:**  
   Starts with the `mca_master.csv` file containing foundational company data.

2. **Enrichment:**  
   The `Enriched.csv` and `log.csv` files provide supplementary data. Enrichment is done via manual or semi-automated scraping to gather details not present in the master file, such as director names.

3. **Loading & Cleaning:**  
   The `load_data()` function in the Streamlit app reads all CSV files, cleans column headers, and standardizes data types (e.g., converts dates).

4. **Interactive Visualization:**  
   Cleaned data is displayed in the Streamlit dashboard, enabling filtering, searching, and real-time visualization.

5. **AI Insights:**  
   The `log.csv` data feeds into the AI Summary Generator to produce high-level reports on corporate activity.

---
