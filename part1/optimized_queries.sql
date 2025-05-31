-- Dates table
CREATE TABLE dates AS 
SELECT DATE(
    generate_series('2025-01-01'::date, '2025-12-31'::date, '1 day'::interval)
) AS date;


-- rolling 7-day WAU
SELECT 
    dates.date, 
    COUNT(DISTINCT(events.user_id)) AS "Rolling Weekly active users"
FROM dates LEFT JOIN events 
ON 
    events.timestamp::date <= dates.date 
AND 
    events.timestamp::date > (dates.date - INTERVAL '7 days')
GROUP BY 
    dates.date
ORDER BY 
    dates.date;


-- Convert Rolling 7-day WAU to Calendar WAU
SELECT 
    dates.date AS "End of the week", 
    COUNT(DISTINCT(events.user_id)) AS "Weekly active users"
FROM 
    dates 
LEFT JOIN 
    events 
ON 
    events.timestamp::date <= dates.date 
AND 
    events.timestamp::date > (dates.date - INTERVAL '7 days')
WHERE 
    extract(dow from dates.date) = 0
GROUP BY 
    dates.date
ORDER BY 
    dates.date;


-- Revenue per category
SELECT 
    category, 
    SUM(price::numeric(10, 2)) AS "Revenue per category"
FROM 
    events 
LEFT JOIN 
    products 
ON 
    events.product_id = products.product_id
WHERE 
    event_type = 'purchased'
GROUP BY 
    category
ORDER BY 
    "Revenue per category" DESC;