# Strategy Document

## Part I: Data Exploration & SQL Query Optimization

### Key Clarifications:
- Implemented both **Rolling 7-day** and **Calendar Week** Weekly Active Users (WAU) calculations for comprehensive insights (Read `report.md` for better understanding).
- Created a `dates` helper table to cover all dates, including those without events, ensuring accurate rolling window calculations.
- Assumed each purchase event corresponds to one unit sold due to lack of quantity data.

### Approach:
- Wrote initial SQL queries for WAU and revenue per category.
- Refactored queries and added appropriate indexes on filtering and joining columns.
- Created a Python script to measure execution time before and after indexing.
- **Result:** Optimized queries now run efficiently with low execution time.

---

## Part II: Cohort Analysis

### Approach:
- Grouped users by their signup month to form cohorts.
- Used SQL to track, for each cohort, the percentage of users who returned in each of the first 8 weeks after signup.
    - Used CTEs to get weekly activity and aggregate retention rates.
- Used Python (Pandas and Matplotlib) to visualize the retention matrix as a line graph.
- **Result:** The retention matrix clearly highlights drop-off trends and high-retention cohorts, providing actionable insights for user engagement strategies.

---

## Part III: Behavioral Segmentation with Elasticsearch & AI

### Approach:
- Pulled user search history for each user from Elasticsearch using aggregation queries.
- Used a pre-trained SentenceTransformer model to convert each user's combined search history into a vector embedding.
- Applied K-means clustering to group users into behavioral segments based on their search patterns.
- Analyzed top queries per cluster to assign meaningful segment labels (e.g., "Tech shoppers", "Budget-conscious buyers", etc.).
- Stored segmented users and their labels back into Elasticsearch.
- **Result:** Successfully identified and labeled distinct user segments, enabling targeted marketing.

---


**Thank you for reviewing my work. I am happy to provide any further explanations or enhancements upon request.**