# Data Engineer for E-commerce Platform

## Overview

This repository contains my solution for the Data Engineer coding challenge for an e-commerce platform.  
The goal was to improve database performance, understand retention and behavior trends and create intelligent user segments using AI.

---

## Project structure

- `README.md` — Project overview and structure.  

- `strategy.md` — One-page document explaining optimizations, retention insights, and segmentation rationale.  

- `requirements.txt` — Python dependencies for all scripts.  

- `docker-compose.yaml` — Docker setup to run PostgreSQL and pgAdmin for easy database management for Part1 and 2.

- `populate_database.sql` —  SQL script to create and fill users, products, and events tables with 12 months of related e-commerce data.

- `command.txt` — Docker command to run a local Elasticsearch container for Part3.

- `part1/`  
  - `optimized_queries.sql` — Optimized SQL queries for weekly active users and revenue per category.   
  - `benchmark_queries.py` — Python script to execute the SQL queries and benchmark performance before and after optimization.  
  - `report.md` — Important clarifications and summary of bottlenecks and optimizations. 

- `part2/`  
  - `cohort_analysis.sql` — SQL query to generate weekly retention matrix by monthly cohorts.  
  - `cohort_analysis.py` — Python script to execute the SQL query and visualize the retention matrix.  
  - `cohort_plot.png` — Retention visualization output.

- `part3/`  
  - `populating_elastic_data.py` — Script to insert mock data from `mock_data.json` into Elasticsearch.  
  - `user_segmentation_pipeline.py` — Main pipeline script of Part3.  

---