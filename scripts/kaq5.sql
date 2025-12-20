-- Proportion of activity from collaborative versus individual work

SET search_path = notion_dw;

WITH base AS (
  SELECT
    t.year,
    t.month,
    CASE WHEN f.collaboration_event_flag = 1 THEN 'collaborative' ELSE 'individual' END AS work_mode,
    SUM(f.event_count) AS events
  FROM fact_product_usage_engagement f
  JOIN dim_time t ON t.time_key = f.time_key
  GROUP BY t.year, t.month, CASE WHEN f.collaboration_event_flag = 1 THEN 'collaborative' ELSE 'individual' END
),
totals AS (
  SELECT
    year, month,
    SUM(events) AS total_events
  FROM base
  GROUP BY year, month
)
SELECT
  b.year,
  b.month,
  b.work_mode,
  b.events,
  ROUND(b.events::numeric / NULLIF(t.total_events,0), 4) AS proportion
FROM base b
JOIN totals t USING (year, month)
ORDER BY b.year, b.month, b.work_mode;

