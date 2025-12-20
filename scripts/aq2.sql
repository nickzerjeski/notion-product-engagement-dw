SET search_path = notion_dw;

WITH monthly AS (
  SELECT
    DATE_TRUNC('month', t.calendar_date)::date AS month_start,
    SUM(f.active_user_flag) AS dau
  FROM fact_product_usage_engagement f
  JOIN dim_time t ON t.time_key = f.time_key
  WHERE t.calendar_date >= DATE '2024-01-01'
    AND t.calendar_date <  DATE '2026-01-01'
  GROUP BY DATE_TRUNC('month', t.calendar_date)
),
with_prev AS (
  SELECT
    month_start,
    dau,
    LAG(dau) OVER (ORDER BY month_start) AS prev_month_dau
  FROM monthly
)
SELECT
  month_start,
  dau AS dau_current_month,
  prev_month_dau AS dau_previous_month,
  (dau - prev_month_dau) AS abs_change,
  ROUND(
    (dau - prev_month_dau)::numeric / NULLIF(prev_month_dau, 0),
    4
  ) AS rel_change
FROM with_prev
ORDER BY month_start;
