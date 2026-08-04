CREATE MATERIALIZED VIEW IF NOT EXISTS negotiation_mv AS
SELECT
    ready_to_negotiate,
    COUNT(*)
FROM silver_apartments
GROUP BY ready_to_negotiate;
