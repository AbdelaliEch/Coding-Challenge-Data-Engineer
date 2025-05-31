-- For each group of users who signed up in a specific month (e.g., January 2025), we're measuring:
-- How many of them came back in EACH (not in all) of the 8 weeks after they signed up. 


-- cte1: For each user and event, flag if the user was active in each of the first 8 weeks after signup
WITH cte1 AS (
	SELECT 
		events.user_id, 
		DATE_TRUNC('month', signup_date) AS signup_month,
		signup_date,
		timestamp,
		CASE 
			WHEN timestamp >= signup_date AND timestamp < (signup_date + INTERVAL '1 week') THEN 1
			ELSE 0
		END AS is_week1_active,
		CASE 
			WHEN timestamp >= (signup_date + INTERVAL '1 week') AND timestamp < (signup_date + INTERVAL '2 weeks') THEN 1
			ELSE 0
		END AS is_week2_active,
		CASE 
			WHEN timestamp >= (signup_date + INTERVAL '2 weeks') AND timestamp < (signup_date + INTERVAL '3 weeks') THEN 1
			ELSE 0
		END AS is_week3_active,
		CASE 
			WHEN timestamp >= (signup_date + INTERVAL '3 weeks') AND timestamp < (signup_date + INTERVAL '4 weeks') THEN 1
			ELSE 0
		END AS is_week4_active,
		CASE 
			WHEN timestamp >= (signup_date + INTERVAL '4 weeks') AND timestamp < (signup_date + INTERVAL '5 weeks') THEN 1
			ELSE 0
		END AS is_week5_active,
		CASE 
			WHEN timestamp >= (signup_date + INTERVAL '5 weeks') AND timestamp < (signup_date + INTERVAL '6 weeks') THEN 1
			ELSE 0
		END AS is_week6_active,
		CASE 
			WHEN timestamp >= (signup_date + INTERVAL '6 weeks') AND timestamp < (signup_date + INTERVAL '7 weeks') THEN 1
			ELSE 0
		END AS is_week7_active,
		CASE 
			WHEN timestamp >= (signup_date + INTERVAL '7 weeks') AND timestamp < (signup_date + INTERVAL '8 weeks') THEN 1
			ELSE 0
		END AS is_week8_active
	FROM users
	LEFT JOIN events 
	ON events.user_id = users.user_id
	WHERE signup_date < '2025-11-06' -- last date in our dataset 2025-12-31, so we only consider users who signed up 8 weeks before that date 
), 
-- cte2: For each user, keep only one row and mark if they were active in each week (1 if active at least once in that week)
cte2 AS (
	SELECT
		user_id, signup_month, signup_date,
		MAX(is_week1_active) AS is_week1_active,
		MAX(is_week2_active) AS is_week2_active,
		MAX(is_week3_active) AS is_week3_active,
		MAX(is_week4_active) AS is_week4_active,
		MAX(is_week5_active) AS is_week5_active,
		MAX(is_week6_active) AS is_week6_active,
		MAX(is_week7_active) AS is_week7_active,
		MAX(is_week8_active) AS is_week8_active
	FROM cte1
	GROUP BY user_id, signup_month, signup_date
), 
-- cte3: For each signup month, count how many users were active in each week
cte3 AS (
	SELECT
		signup_month,
		COUNT(DISTINCT CASE WHEN is_week1_active = 1 THEN user_id END) AS week1_active_users,
		COUNT(DISTINCT CASE WHEN is_week2_active = 1 THEN user_id END) AS week2_active_users,
		COUNT(DISTINCT CASE WHEN is_week3_active = 1 THEN user_id END) AS week3_active_users,
		COUNT(DISTINCT CASE WHEN is_week4_active = 1 THEN user_id END) AS week4_active_users,
		COUNT(DISTINCT CASE WHEN is_week5_active = 1 THEN user_id END) AS week5_active_users,
		COUNT(DISTINCT CASE WHEN is_week6_active = 1 THEN user_id END) AS week6_active_users,
		COUNT(DISTINCT CASE WHEN is_week7_active = 1 THEN user_id END) AS week7_active_users,
		COUNT(DISTINCT CASE WHEN is_week8_active = 1 THEN user_id END) AS week8_active_users
	FROM cte2 
	GROUP BY signup_month
), 
-- cohorts: For each signup month, count the total number of users who signed up
cohorts AS (
	SELECT 
		DATE_TRUNC('month', signup_date) AS cohort_month, 
		COUNT(DISTINCT(user_id)) AS total_users_count 
	FROM users 
	GROUP BY 1
)
-- Dividing active users by total users to get the weekly retention percentage for each cohort month 
SELECT 
	cohort_month::date,
	ROUND((week1_active_users::numeric/total_users_count)*100,2) AS week1_retention_rate,
	ROUND((week2_active_users::numeric/total_users_count)*100,2) AS week2_retention_rate,
	ROUND((week3_active_users::numeric/total_users_count)*100,2) AS week3_retention_rate,
	ROUND((week4_active_users::numeric/total_users_count)*100,2) AS week4_retention_rate,
	ROUND((week5_active_users::numeric/total_users_count)*100,2) AS week5_retention_rate,
	ROUND((week6_active_users::numeric/total_users_count)*100,2) AS week6_retention_rate,
	ROUND((week7_active_users::numeric/total_users_count)*100,2) AS week7_retention_rate,
	ROUND((week8_active_users::numeric/total_users_count)*100,2) AS week8_retention_rate 
FROM cte3
JOIN cohorts ON cte3.signup_month = cohorts.cohort_month
ORDER BY cohort_month;