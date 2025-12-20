-- Engagement over time accross subscription tiers
SET search_path = notion_dw;

SELECT
  t.year,
  t.month,
  u.subscription_tier,
  SUM(f.active_user_flag)      AS dau,
  SUM(f.event_count)           AS events,
  ROUND(
    SUM(f.event_count)::numeric / NULLIF(SUM(f.active_user_flag), 0),
    2
  )                            AS events_per_active_user
FROM fact_product_usage_engagement f
JOIN dim_time t ON t.time_key = f.time_key
JOIN dim_user u ON u.user_key = f.user_key
GROUP BY GROUPING SETS (
  (t.year, t.month, u.subscription_tier),  -- by tier per month
  (t.year, t.month),                       -- all tiers per month
  (u.subscription_tier),                   -- tier total across all time
  ()                                       -- grand total
)
ORDER BY t.year NULLS LAST, t.month NULLS LAST, u.subscription_tier NULLS LAST;
