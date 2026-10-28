# Weather Data Pipeline

A reproducible, local data engineering pipeline that ingests weather observations, transforms them into analytics-ready models, and provides insights into historical weather patterns.

## Features

- Automated data workflows using Kestra
- Data transformation and testing with dbt
- Analytical storage using DuckDB
- Interactive weather dashboard with Streamlit

## Setup

**1. Clone the repository**
```bash
git clone <github-repo-url>
cd <project-directory>
```

**2. Build the project**
```bash
make build
```

**3. Start the project**
```bash
make up
```

## Technologies

- Python
- Kestra
- dbt
- DuckDB
- Streamlit
- Docker

## Pipeline

Weather Data Ingestion → DuckDB → dbt Transformations → Weather Analytics Dashboard