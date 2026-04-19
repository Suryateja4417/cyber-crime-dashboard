# India Cyber Crime Cases Dashboard

## Overview

This project analyzes cyber crime cases across Indian states from 2002 to 2020 and presents the results through an interactive Streamlit dashboard.

The goal is to identify trends, compare states, and highlight peak activity periods using clear visualizations and geospatial mapping.

---

## Features

### 1. Overall Analysis

* Total cyber crime cases across India
* Maximum and minimum cases recorded

### 2. Top 5 States

* States with the highest total cases
* Peak case value and corresponding year for each state

### 3. Filtered Insights

* Dynamic filtering by:

  * State
  * Year range
* Real-time KPI updates based on selection

### 4. Trend Analysis

* Year-wise growth trends
* Multi-state comparison

### 5. Geospatial Visualization

* Interactive India map
* Displays:

  * Total cases per state
  * Peak and minimum values
  * Corresponding years

---

## Dataset

The project uses two processed datasets:

* **cleaned_data.csv**

  * State-wise aggregated metrics
  * Total, Growth, Peak Year, Median

* **data_long.csv**

  * Long format dataset
  * Columns:

    * State
    * Year
    * Cases

---

## Tech Stack

* Python
* Pandas
* Streamlit
* Plotly

---

## Project Structure

```
project/
│
├── cc_dashboardapp.py
├── cleaned_data.csv
├── data_long.csv
├── india_state.geojson
├── README.md 
```

---

## How to Run

1. Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/cyber-crime-dashboard.git
cd cyber-crime-dashboard
```

2. Install dependencies:

```
pip install pandas streamlit plotly
```

3. Run the application:

```
streamlit run cc_dashboardapp.py
```
4. Output Preview

```

check cc_output.pdf
```
---

## Key Insights

* Cyber crime cases show significant growth after 2010
* A small number of states contribute disproportionately to total cases
* Peak years vary across states, indicating region-specific trends
* Some states consistently show low activity, highlighting uneven distribution

---

## Limitations

* Data is historical (up to 2020)
* No predictive modeling included
* GeoJSON compatibility depends on correct state naming

---

## Future Improvements

* Add forecasting (time series models)
* Introduce anomaly detection
* Improve UI with multi-page layout
* Deploy live dashboard for public access

---

## Conclusion

This project demonstrates how data analysis and visualization can be used to uncover meaningful insights from crime datasets and present them in an interactive, user-friendly format.

---

## Author

Surya Teja
