# 🏢 Unified Manager Dashboard & Employee Performance Tracker

> **A bridge between data collection and actionable management insights.**

## 🌟 Executive Summary (Business Perspective)

In modern distributed work environments, tracking employee daily progress and weekly milestones across various departments can be challenging. This project provides a **seamless, automated solution** for managers to monitor team health, project progress, and operational efficiency without manual reporting overhead.

### Why this matters:
*   **Data-Driven Decisions:** Transition from "gut feeling" to hard data regarding team performance.
*   **Early Warning System:** Automatically identify employees facing challenges or showing decreased engagement.
*   **Operational Visibility:** Real-time tracking of where your team is working (Office, Home, Field).
*   **Zero Barrier to Entry:** Uses familiar tools like Google Forms for data entry, making it easy for employees to adopt.

---

## 🛠 Technical Overview (Developer Perspective)

This repository contains a robust **Streamlit-based dashboard** integrated with the **Google Workspace Ecosystem**. It leverages `gspread` for real-time data ingestion from Google Sheets (which act as the backend for Google Forms) and `Plotly` for dynamic data visualization.

### Architecture
1.  **Data Ingress:** Employees submit data via Google Forms.
2.  **Storage:** Responses are automatically aggregated in Google Sheets.
3.  **Processing Layer (`google_forms_integration.py`):** A helper module that authenticates with Google Cloud via Service Accounts, cleanses the data, and standardizes it into Pandas DataFrames.
4.  **Visualization Layer (`manager_dashboard.py`):** The main Streamlit application that renders KPIs, alerts, and trend charts.

### Tech Stack
*   **Frontend:** [Streamlit](https://streamlit.io/) (with custom RTL/Arabic CSS support).
*   **Data Visualization:** [Plotly Express & Graph Objects](https://plotly.com/python/).
*   **Data Processing:** [Pandas](https://pandas.pydata.org/).
*   **Backend Integration:** [Google Sheets API](https://developers.google.com/sheets/api) via `gspread`.
*   **Authentication:** [Google OAuth2](https://google-auth.readthedocs.io/) (Service Accounts).

---

## ✨ Key Features

*   **📈 KPI Scorecards:** Instant visibility into total employees, average completion rates, and "On-Track" vs "Needs Attention" metrics.
*   **🚨 Intelligent Alerting:** Automated triggers for low performance (<60% completion) and reported blockers/challenges.
*   **🌍 Work Location Tracking:** Pie charts visualizing the distribution of the workforce (Remote vs. Office vs. Field).
*   **📅 Weekly Progress Trends:** Time-series analysis of completed vs. delayed tasks.
*   **🇸🇦 Full RTL Support:** Native Arabic language support with Right-to-Left UI layout.
*   **📧 Action Center:** Quick-action buttons for sending reminders and exporting data to Excel.

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repo-url>
cd <repo-name>
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Google Cloud Configuration (The Backend)
To connect the dashboard to your live data:
1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project.
3.  **Enable APIs:** Search for and enable "Google Sheets API" and "Google Drive API".
4.  **Create Service Account:**
    *   Navigate to **IAM & Admin > Service Accounts**.
    *   Create a service account and download the **JSON Key file**.
5.  **Rename/Move Key:** Place the JSON file in the project directory and update the `SERVICE_ACCOUNT_FILE` path in `google_forms_integration.py`.
    *   **⚠️ Security Note:** Ensure your `.json` key file is added to `.gitignore` to prevent accidental exposure of credentials.

### 4. Google Sheets Setup
1.  Create two Google Forms (Daily Check-in and Weekly Progress).
2.  Link them to a Google Sheet.
3.  **Share the Sheet:** Open your Google Sheet and click **Share**. Add the `client_email` found in your Service Account JSON file with "Editor" permissions.
4.  Update the `spreadsheet_id` in `google_forms_integration.py`.

---

## 📂 Project Structure

*   `manager_dashboard.py`: The heart of the application. Handles UI layout, state management, and visualization.
*   `google_forms_integration.py`: Logic for connecting to Google APIs, fetching data, and transforming raw sheet data into clean formats.
*   `requirements.txt`: List of all Python dependencies.

---

## 📖 Usage Guide

1.  **Launch the Dashboard:**
    ```bash
    streamlit run manager_dashboard.py
    ```
2.  **Filter Results:** Use the sidebar to filter by Department (IT, HR, Marketing, etc.) or specific Date Ranges.
3.  **Monitor Alerts:** Check the "Alerts and Warnings" section for immediate issues requiring managerial intervention.
4.  **Analyze Trends:** Scroll to the bottom to see how project velocity changes week-over-week.

---

## 🛤 Roadmap & Future Improvements
*   [ ] **Authentication:** Add a login system for different management levels.
*   [ ] **Direct Messaging:** Integrate with Slack/Teams for the "Action Center" notifications.
*   [ ] **AI Insights:** Implement predictive analysis to forecast project delays based on historical "Daily Check-in" challenges.

---
*Developed with ❤️ for efficient management.*
