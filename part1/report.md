# Data Engineer Coding Challenge - Part I Report

The SQL queries aimed to compute **Weekly Active Users (WAU)** and **Revenue per Category**

## Important clarifications
### Weekly Active Users (WAU) Calculation Approaches
There are two common ways to measure Weekly Active Users:
1. **Calendar Week WAU:** Counts unique users active during each week based on the calendar (Monday to Sunday), which can sometimes be less accurate for incomplete and partial weeks (For example in my case: the start date of my dataset is 2025-01-01 which is a Wednesday, so if we used CWAU way we will get a low number because Monday and Tuesday aren't counted). 
2. **Rolling 7-day WAU:** Counts unique users active in the past 7 days, updated every day, giving a better view of engagement.  

Since the challenge did not specify the WAU type, I first implemented the rolling 7-day WAU query for more accurate insights, then I converted it to compute the calendar WAU.

### Assumption on Purchase Quantity
There is no quantity column in the events table, so I assumed each purchase event equals buying one piece of the product.

## Bottlenecks
Queries were slow due to missing indexes on important columns that we were using in JOIN and WHERE statements.

## Improvements
Created indexes on key columns to speed up filtering and joins.
These changes reduced query execution times, improving performance significantly.