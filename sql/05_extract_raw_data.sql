-- ================================================================
-- 05_extract_raw_data.sql — Ecommerce Data Extraction Query
-- ================================================================
-- PURPOSE:
--   This is the query that DataExtractor.run() executes via Python.
--   It joins customers + orders + products + reviews + sellers
--   to produce raw-data.csv.
--
--   raw-data.csv is the input to Module 05 ETL.
--
-- WHY THIS QUERY EXISTS:
--   The database is normalized for OLTP performance.
--   Analytics, BI dashboards, and ML models need a single flat table.
--   This is the "denormalisation layer" of the pipeline.
--
-- THE DATA IS INTENTIONALLY MESSY:
--   After seeding, the database may contain:
--     - NULL ratings or missing reviews
--     - Missing delivery dates
--     - Returned orders mixed with completed orders
--     - Extreme discounts or pricing anomalies
--     - Customers with incomplete profiles
--
--   Module 05 ETL will clean and transform these issues.
--   We intentionally do NOT fix them here.
--
-- CHANGE SCHEMA BEFORE RUNNING:
--   The {schema} placeholder is replaced by Python config.
-- ================================================================

SELECT

    -- ── Customer Master Data ─────────────────────────────────────
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.country,
    c.city,
    c.segment,
    c.is_active,

    -- ── Product Master Data ──────────────────────────────────────
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    p.cost,
    p.rating AS product_rating,
    p.review_count AS product_review_count,

    -- ── Seller Master Data ───────────────────────────────────────
    s.seller_id,
    s.store_name,
    s.country AS seller_country,
    s.category AS seller_category,
    s.rating AS seller_rating,
    s.total_sales,

    -- ── Order Facts (base transaction data) ──────────────────────
    o.order_id,
    o.order_date,
    o.quantity,
    o.unit_price,
    o.discount_pct,
    o.total_amount,
    o.shipping_cost,
    o.payment_method,
    o.status,
    o.delivery_date,
    o.is_returned,

    -- ── Review Data (may be NULL if no review exists) ────────────
    r.review_id,
    r.rating AS review_rating,
    r.review_title,
    r.helpful_votes,
    r.is_verified AS review_verified,

    -- ── Derived Features (light enrichment, NOT ETL cleaning) ────
    (o.quantity * o.unit_price) AS gross_order_value,
    (o.unit_price * (1 - COALESCE(o.discount_pct, 0))) AS net_unit_price,

    CASE
        WHEN o.is_returned = TRUE THEN 1 ELSE 0
    END AS return_flag,

    CASE
        WHEN o.status = 'Delivered' THEN 1 ELSE 0
    END AS delivered_flag,

        -- ── Metadata ────────────────────────────────────────────────
    '{industry}'::VARCHAR AS source_schema,
    NOW()::DATE AS extracted_date

FROM {industry}.orders o

-- Customer join (who placed the order)
LEFT JOIN {industry}.customers c
    ON o.customer_id = c.customer_id

-- Product join (what was ordered)
LEFT JOIN {industry}.products p
    ON o.product_id = p.product_id

-- Seller join (who fulfilled the product)
LEFT JOIN {industry}.sellers s
    ON p.seller_id = s.seller_id

-- Reviews join (optional, not all orders are reviewed)
LEFT JOIN {industry}.reviews r
    ON o.order_id = r.order_id
    AND o.product_id = r.product_id
    AND o.customer_id = r.customer_id

-- Easier CSV reading
ORDER BY
    o.order_date DESC,
    o.order_id;