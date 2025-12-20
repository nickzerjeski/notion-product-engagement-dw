-- ==========================================================
-- NOTION DW: Full Mock Data Generation (One File)
-- Target: PostgreSQL
-- Schema: notion_dw
--
-- GOAL
--   Populate all dimension tables and the fact table with mock data
--   for the period 01.01.2024 .. 31.12.2024 (inclusive).
--
-- TEMPORAL CONSISTENCY GUARANTEES
--   1) Fact event date >= user.signup_date
--   2) Fact event timestamp is sampled inside the chosen session window
--      (session_start_time <= event_ts <= session_end_time)
--   3) Chosen session_start_date >= user.signup_date
--   4) Session window is within 2024 and has start < end
--
-- REQUIRED MINIMUM SIZES
--   - >= 100 users
--   - >= 50 workspaces
--   - >= 50 sessions
--
-- FACT ROW COUNT
--   Set in params.target_rows (default: 60000)
-- ==========================================================

SET search_path = notion_dw;

-- ==========================================================
-- (0) Optional reset (uncomment if needed)
-- ==========================================================
-- TRUNCATE TABLE
--   fact_product_usage_engagement,
--   dim_session, dim_event, dim_device, dim_content, dim_workspace, dim_user, dim_time
-- RESTART IDENTITY
-- CASCADE;

-- ==========================================================
-- (1) Ensure partitions for 2024 (monthly)
--     Required because fact_product_usage_engagement is PARTITION BY RANGE(time_key)
-- ==========================================================
DO $$
DECLARE
  m_start DATE;
  m_end   DATE;
  p_from  INT;
  p_to    INT;
  p_name  TEXT;
BEGIN
  m_start := DATE '2024-01-01';

  WHILE m_start <= DATE '2024-12-01' LOOP
    m_end := (m_start + INTERVAL '1 month')::DATE;

    p_from := (EXTRACT(YEAR FROM m_start)::INT * 10000
               + EXTRACT(MONTH FROM m_start)::INT * 100
               + EXTRACT(DAY FROM m_start)::INT);

    p_to := (EXTRACT(YEAR FROM m_end)::INT * 10000
             + EXTRACT(MONTH FROM m_end)::INT * 100
             + EXTRACT(DAY FROM m_end)::INT);

    p_name := format('fact_p_%s', to_char(m_start, 'YYYYMM'));

    EXECUTE format(
      'CREATE TABLE IF NOT EXISTS %I PARTITION OF fact_product_usage_engagement FOR VALUES FROM (%s) TO (%s);',
      p_name, p_from, p_to
    );

    m_start := m_end;
  END LOOP;
END $$;

-- ==========================================================
-- (2) TIME DIMENSION: 2024-01-01 .. 2024-12-31
-- ==========================================================
INSERT INTO dim_time (
  time_key, calendar_date, day_of_week, is_weekend,
  week_of_year, month, quarter, year, day_since_signup_bucket
)
SELECT
  (EXTRACT(YEAR FROM d)::INT * 10000
   + EXTRACT(MONTH FROM d)::INT * 100
   + EXTRACT(DAY FROM d)::INT) AS time_key,
  d::DATE AS calendar_date,
  EXTRACT(ISODOW FROM d)::SMALLINT AS day_of_week,
  (EXTRACT(ISODOW FROM d) IN (6,7)) AS is_weekend,
  EXTRACT(WEEK FROM d)::SMALLINT AS week_of_year,
  EXTRACT(MONTH FROM d)::SMALLINT AS month,
  EXTRACT(QUARTER FROM d)::SMALLINT AS quarter,
  EXTRACT(YEAR FROM d)::SMALLINT AS year,
  NULL::SMALLINT AS day_since_signup_bucket
FROM generate_series(DATE '2024-01-01', DATE '2024-12-31', INTERVAL '1 day') AS g(d)
ON CONFLICT (time_key) DO NOTHING;

-- ==========================================================
-- (3) DEVICE DIMENSION: small fixed set
-- ==========================================================
INSERT INTO dim_device (device_id_nat, platform, operating_system, app_version, device_form_factor)
VALUES
  ('dev_web_win', 'web',     'Windows', '3.08.0', 'desktop'),
  ('dev_web_mac', 'web',     'macOS',   '3.08.1', 'desktop'),
  ('dev_desktop', 'desktop', 'macOS',   '3.09.0', 'desktop'),
  ('dev_ios',     'mobile',  'iOS',     '3.07.9', 'phone'),
  ('dev_android', 'mobile',  'Android', '3.08.2', 'phone')
ON CONFLICT (device_id_nat) DO NOTHING;

-- ==========================================================
-- (4) CONTENT DIMENSION: small fixed set
-- ==========================================================
INSERT INTO dim_content (content_id_nat, content_type, is_template_based, is_shared, ownership_type)
VALUES
  ('cnt_page',      'page',       FALSE, FALSE, 'personal'),
  ('cnt_database',  'database',   TRUE,  TRUE,  'workspace'),
  ('cnt_wiki',      'wiki',       TRUE,  TRUE,  'team_space'),
  ('cnt_taskboard', 'task_board', FALSE, TRUE,  'workspace'),
  ('cnt_template',  'page',       TRUE,  FALSE, 'personal')
ON CONFLICT (content_id_nat) DO NOTHING;

-- ==========================================================
-- (5) EVENT DIMENSION: small fixed set
-- ==========================================================
INSERT INTO dim_event (event_type, feature_category, interaction_intent)
VALUES
  ('view',         'Core',          'consumption'),
  ('create',       'Core',          'creation'),
  ('edit',         'Core',          'creation'),
  ('comment',      'Collaboration', 'collaboration'),
  ('share',        'Collaboration', 'collaboration'),
  ('db_query',     'Databases',     'consumption'),
  ('api_call',     'Integrations',  'creation'),
  ('template_use', 'Templates',     'creation')
ON CONFLICT (event_type, feature_category, interaction_intent) DO NOTHING;

-- ==========================================================
-- (6) USER DIMENSION: >= 100 users
--     IMPORTANT: signup_date restricted to 2024-01-01 .. 2024-11-30
--     so that users have time to generate events after signup in 2024.
-- ==========================================================
INSERT INTO dim_user (
  user_id_nat, signup_date, subscription_tier,
  user_type, region, lifecycle_stage
)
SELECT
  'usr_' || LPAD(i::TEXT, 4, '0') AS user_id_nat,
  DATE '2024-01-01' + ((random() * 334)::INT) AS signup_date, -- up to 2024-11-30
  (ARRAY['Free','Plus','Business','Enterprise'])[1 + (random()*3)::INT] AS subscription_tier,
  (ARRAY['individual','member','guest'])[1 + (random()*2)::INT] AS user_type,
  (ARRAY['EU','NA','APAC'])[1 + (random()*2)::INT] AS region,
  (ARRAY['onboarding','active','active','dormant'])[1 + (random()*3)::INT] AS lifecycle_stage
FROM generate_series(1,100) i
ON CONFLICT (user_id_nat) DO NOTHING;

-- ==========================================================
-- (7) WORKSPACE DIMENSION: >= 50 workspaces
-- ==========================================================
INSERT INTO dim_workspace (
  workspace_id_nat, workspace_plan,
  workspace_size_bucket, industry_segment, workspace_region
)
SELECT
  'ws_' || LPAD(i::TEXT, 3, '0') AS workspace_id_nat,
  (ARRAY['Free','Plus','Business','Enterprise'])[1 + (random()*3)::INT] AS workspace_plan,
  (ARRAY['1','2--10','11--50','50+'])[1 + (random()*3)::INT] AS workspace_size_bucket,
  (ARRAY['Education','Software','Finance','Consulting'])[1 + (random()*3)::INT] AS industry_segment,
  (ARRAY['EU','NA'])[1 + (random())::INT] AS workspace_region
FROM generate_series(1,50) i
ON CONFLICT (workspace_id_nat) DO NOTHING;

-- ==========================================================
-- (8) SESSION DIMENSION: >= 50 sessions
--     - session_start_time within 2024
--     - duration 5..65 minutes
--     - session_end_time capped at end of 2024
-- ==========================================================
INSERT INTO dim_session (
  session_id_nat, session_start_time, session_end_time, session_origin
)
SELECT
  'sess_' || LPAD(i::TEXT, 4, '0') AS session_id_nat,
  ts AS session_start_time,
  LEAST(
    ts + ((300 + random()*3600)::INT || ' seconds')::INTERVAL,
    TIMESTAMP '2024-12-31 23:59:59'
  ) AS session_end_time,
  (ARRAY['direct','link','notification'])[1 + (random()*2)::INT] AS session_origin
FROM (
  SELECT
    i,
    (TIMESTAMP '2024-01-01'
     + (random() * INTERVAL '365 days')
     + (random() * INTERVAL '24 hours')) AS ts
  FROM generate_series(1,50) i
) s
ON CONFLICT (session_id_nat) DO NOTHING;

-- ==========================================================
-- (9) FACT TABLE: EXACT N events with temporal consistency
--     - N defined in params.target_rows
-- ==========================================================
WITH params AS (
  SELECT 60000::INT AS target_rows
),
rows AS (
  SELECT generate_series(1, (SELECT target_rows FROM params)) AS rn
),
picked AS (
  SELECT
    u.user_key,
    u.signup_date,

    s.session_key,
    s.session_start_time,
    s.session_end_time,

    (s.session_start_time + (random() * (s.session_end_time - s.session_start_time))) AS event_ts,

    w.workspace_key,
    c.content_key,
    d.device_key,
    e.event_key
  FROM rows r
  CROSS JOIN LATERAL (
    SELECT *
    FROM dim_user
    ORDER BY random()
    LIMIT 1
  ) u
  CROSS JOIN LATERAL (
    SELECT *
    FROM dim_session s
    WHERE s.session_start_time::date >= u.signup_date
      AND s.session_start_time::date <= DATE '2024-12-31'
    ORDER BY random()
    LIMIT 1
  ) s
  CROSS JOIN LATERAL (SELECT workspace_key FROM dim_workspace ORDER BY random() LIMIT 1) w
  CROSS JOIN LATERAL (SELECT content_key   FROM dim_content   ORDER BY random() LIMIT 1) c
  CROSS JOIN LATERAL (SELECT device_key    FROM dim_device    ORDER BY random() LIMIT 1) d
  CROSS JOIN LATERAL (SELECT event_key     FROM dim_event     ORDER BY random() LIMIT 1) e
),
dated AS (
  SELECT
    p.*,
    (p.event_ts)::date AS event_date
  FROM picked p
  WHERE (p.event_ts)::date BETWEEN DATE '2024-01-01' AND DATE '2024-12-31'
    AND (p.event_ts)::date >= p.signup_date
)
INSERT INTO fact_product_usage_engagement (
  time_key,
  user_key,
  workspace_key,
  content_key,
  device_key,
  event_key,
  session_key,
  event_count,
  active_user_flag,
  activation_event_flag,
  feature_usage_flag,
  collaboration_event_flag,
  session_event_count,
  session_duration_sec
)
SELECT
  t.time_key,
  d.user_key,
  d.workspace_key,
  d.content_key,
  d.device_key,
  d.event_key,
  d.session_key,
  1 AS event_count,
  CASE WHEN random() < 0.25 THEN 1 ELSE 0 END AS active_user_flag,
  CASE
    WHEN d.event_date < (d.signup_date + INTERVAL '7 days') AND random() < 0.25 THEN 1
    ELSE 0
  END AS activation_event_flag,
  CASE WHEN random() < 0.30 THEN 1 ELSE 0 END AS feature_usage_flag,
  CASE WHEN random() < 0.35 THEN 1 ELSE 0 END AS collaboration_event_flag,
  (1 + random()*15)::INT AS session_event_count,
  GREATEST(0, EXTRACT(EPOCH FROM (d.session_end_time - d.session_start_time))::INT) AS session_duration_sec
FROM dated d
JOIN dim_time t ON t.calendar_date = d.event_date;

-- ==========================================================
-- (10) Verification queries (run manually)
-- ==========================================================
-- SELECT COUNT(*) AS fact_rows FROM fact_product_usage_engagement;
--
-- SELECT COUNT(*) AS signup_violations
-- FROM fact_product_usage_engagement f
-- JOIN dim_time t ON t.time_key = f.time_key
-- JOIN dim_user u ON u.user_key = f.user_key
-- WHERE t.calendar_date < u.signup_date;
--
-- SELECT COUNT(*) AS coarse_session_violations
-- FROM fact_product_usage_engagement f
-- JOIN dim_time t ON t.time_key = f.time_key
-- JOIN dim_session s ON s.session_key = f.session_key
-- WHERE t.calendar_date < s.session_start_time::date
--    OR t.calendar_date > s.session_end_time::date;
