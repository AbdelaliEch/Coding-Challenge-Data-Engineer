# Data Engineer for E-commerce Platform

## Overview

This repository contains my solution for the Data Engineer coding challenge for an e-commerce platform.  
The goal was to improve database performance, understand retention and behavior trends and create intelligent user segments using AI.

---

## Contents

- `docker-compose.yml`  
  Docker setup to run PostgreSQL and pgAdmin for easy database management.

- `data_population/`  
  Mockaroo-generated datasets simulating 12 months of users, products, and events data.

- `part1/`  
  - `queries.sql` — SQL queries for Part I.  
  - `script.py` — Python script to execute the SQL queries and benchmark performance.  
  - `report.md` — Summary of bottlenecks and optimizations, and important clarifications.

---

## Setup Instructions

### 1. Started the Docker environment

Run the following command to start PostgreSQL and pgAdmin containers:

```bash
docker-compose up -d
```
Once running:
- Access **pgAdmin** in your browser at http://localhost:8080
- Use the credentials defined in `docker-compose.yml` to log in and connect to the PostgreSQL server

### 2. Data Population

The data was generated using **Mockaroo** with SQL export to simulate realistic user behavior over a 12-month period.

### Steps:
1. Created mock datasets for the following tables in Mockaroo:  
   - `users` (user_id, signup_date, country)  
   - `products` (product_id, category, price)  
   - `events` (user_id, event_type, product_id, timestamp)

2. Exported the data from Mockaroo as SQL create and insert statements.

3. Uploaded the sql files into pgAdmin and executed them  