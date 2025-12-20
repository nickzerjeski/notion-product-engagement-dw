-- Device usage affects user activity and session duration

SET search_path = notion_dw;

SELECT
  t.year,
  t.month,
  d.platform,
  SUM(f.event_count)                         AS events,
  SUM(f.active_user_flag)                    AS dau,
  ROUND(AVG(NULLIF(f.session_duration_sec,0))::numeric, 1) AS avg_session_duration_sec
FROM fact_product_usage_engagement f
JOIN dim_time t    ON t.time_key = f.time_key
JOIN dim_device d  ON d.device_key = f.device_key
GROUP BY ROLLUP (t.year, t.month, d.platform)
ORDER BY t.year NULLS LAST, t.month NULLS LAST, d.platform NULLS LAST;

