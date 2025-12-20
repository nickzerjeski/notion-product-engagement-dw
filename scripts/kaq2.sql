-- Which content types generate the highest sustained interaction rates

SET search_path = notion_dw;

SELECT
  t.year,
  t.month,
  c.content_type,
  SUM(f.event_count)      AS events,
  SUM(f.active_user_flag) AS dau,
  ROUND(
    SUM(f.event_count)::numeric / NULLIF(SUM(f.active_user_flag), 0),
    2
  )                       AS events_per_active_user
FROM fact_product_usage_engagement f
JOIN dim_time t    ON t.time_key = f.time_key
JOIN dim_content c ON c.content_key = f.content_key
GROUP BY CUBE (t.year, t.month, c.content_type)
ORDER BY t.year NULLS LAST, t.month NULLS LAST, c.content_type NULLS LAST;
