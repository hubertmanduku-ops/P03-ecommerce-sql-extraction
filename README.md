# P03 ⭐⭐⭐ — E-Commerce SQL Extraction

## The Darko Method 2026 | Student Data Engineering Project

---

## Project Overview

This project demonstrates advanced SQL data extraction and transformation for an e-commerce analytics use case.

It simulates a real-world scenario where a global e-commerce company requires a unified dataset combining customers, orders, products, sellers, and reviews. The dataset is used for revenue forecasting, customer segmentation, and business intelligence.

The project connects to a PostgreSQL database hosted on Supabase, executes SQL queries against the `ecommerce` schema, and generates a consolidated CSV dataset for downstream analytics and machine learning workflows.

---

## Business Scenario

### Company

ShopStream Global

### Role

Data Analyst

ShopStream Global operates a large-scale e-commerce platform with thousands of daily transactions. Data is distributed across multiple relational tables covering customers, orders, products, sellers, and product reviews.

The Chief Data Officer requires a unified dataset to support:

* Revenue forecasting
* Customer segmentation
* Seller performance analysis
* Product return rate tracking
* Review sentiment insights

To achieve this, all relevant tables must be joined into a single analytics-ready dataset.

---

## Project Objective

The goal of this project is to:

* Connect to a PostgreSQL database via Supabase
* Query the `ecommerce` schema using SQL
* Demonstrate advanced SQL techniques including joins, aggregations, CTEs, and window functions
* Integrate five core datasets into a single analytical view
* Generate a clean CSV output for analytics and ML pipelines
* Build a reusable Python-based extraction workflow

---

## Data Sources

The project uses the following tables:

| Table     | Description                    |
| --------- | ------------------------------ |
| orders    | Customer order transactions    |
| customers | Customer profile data          |
| products  | Product catalog information    |
| sellers   | Seller/vendor information      |
| reviews   | Product review and rating data |

---

## Output Deliverable

The final output of this project is:

```text id="ecom001"
data/raw-data.csv
```

This file contains a fully joined dataset combining order, customer, product, seller, and review information in a single flat structure.

---

## Technical Stack

* Python 3.x
* PostgreSQL (Supabase)
* SQL
* Pandas
* DBeaver
* Git & GitHub

---

## Project Structure

```text id="ecom002"
P03-ecommerce-sql/
│
├── data/
│   └── raw-data.csv
│
├── sql/
│   ├── 01_basics.sql
│   ├── 02_aggregation.sql
│   ├── 03_joins.sql
│   ├── 04_cte_window_functions.sql
│   └── 05_extract_raw_data.sql
│
├── src/
│   ├── config.py
│   ├── database.py
│   └── extractor.py
│
├── logs/
│
├── run.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## Key SQL Concepts Covered

### Basic SQL

* SELECT queries
* Filtering with WHERE
* Sorting and limiting results

### Aggregations

* Revenue calculations
* GROUP BY analysis
* Seller performance metrics
* Return rate computations

### Joins

* Multi-table INNER JOIN
* LEFT JOIN for missing relationships
* Five-table join (orders, customers, products, sellers, reviews)

### Advanced SQL

* Common Table Expressions (CTEs)
* Window functions
* Ranking customers by total spend
* Partition-based analytics

---

## Data Pipeline Flow

1. Connect to Supabase PostgreSQL database
2. Query ecommerce schema tables
3. Extract and validate each dataset independently
4. Join all five tables into a unified dataset
5. Apply transformations using SQL + Python (Pandas)
6. Export final dataset as `raw-data.csv`

---

## Success Criteria

* All five tables successfully queried and validated
* Aggregation queries completed:

  * Revenue by seller
  * Return rates by product category
  * Average review score per seller
* Successful five-table join producing order-level dataset
* At least one CTE implemented
* At least one window function ranking customers by spend
* `data/raw-data.csv` generated using Python
* Project pushed to GitHub with proper structure

---

## Learning Outcomes

By completing this project, you will demonstrate:

* Advanced SQL development skills
* Multi-table relational data modeling
* Analytical thinking for business intelligence
* ETL pipeline design using Python
* Data engineering best practices
* GitHub portfolio-level project structuring

---

## Author

Hubert Manduku

Data Analyst | SAP Consultant | Data Engineering Practitioner

Part of The Darko Method 2026 Data Engineering Program.
