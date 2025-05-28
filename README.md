# Data Engineer for E-commerce Platform

## Overview

This repository contains my solution for the Data Engineer coding challenge for an e-commerce platform.  
The goal was to improve database performance, understand retention and behavior trends and create intelligent user segments using AI.

---

## Contents

- `docker-compose.yml`  
  Docker setup to run PostgreSQL and pgAdmin for easy database management.

- `populate_database.sql`  
  SQL script to create and fill users, products, and events tables with 12 months of related e-commerce data.

- `part1/`  
  - `queries.sql` — SQL queries for Part I.  
  - `script.py` — Python script to execute the SQL queries and benchmark performance.  
  - `report.md` — Summary of bottlenecks and optimizations, and important clarifications.

---