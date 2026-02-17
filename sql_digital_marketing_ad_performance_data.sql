USE digital_marketing;

-- =====================================================
-- 1. Overall Business KPIs
-- =====================================================
SELECT
    COUNT(DISTINCT campaign_name) AS total_campaigns,
    SUM(ad_spend) AS total_spend,
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    SUM(conversions) AS total_conversions,
    ROUND(AVG(roi_score),2) AS avg_roi,
    ROUND(AVG(cost_efficiency_index),2) AS avg_cost_efficiency
FROM digital_marketing_ad_performance_data;


-- =====================================================
-- 2. Campaign Funnel Performance
-- =====================================================
SELECT
    campaign_name,
    SUM(impressions) AS impressions,
    SUM(clicks) AS clicks,
    SUM(conversions) AS conversions,
    ROUND(SUM(clicks)/NULLIF(SUM(impressions),0),4) AS ctr,
    ROUND(SUM(conversions)/NULLIF(SUM(clicks),0),4) AS conversion_rate
FROM digital_marketing_ad_performance_data
GROUP BY campaign_name
ORDER BY conversion_rate DESC;


-- =====================================================
-- 3. Channel Performance Summary
-- =====================================================
SELECT
    marketing_channel,
    SUM(ad_spend) AS spend,
    SUM(clicks) AS clicks,
    SUM(conversions) AS conversions,
    ROUND(AVG(roi_score),2) AS avg_roi
FROM digital_marketing_ad_performance_data
GROUP BY marketing_channel
ORDER BY avg_roi DESC;


-- =====================================================
-- 4. Best Channel per Campaign Type
-- =====================================================
SELECT campaign_type, marketing_channel, conversions
FROM (
    SELECT
        campaign_type,
        marketing_channel,
        SUM(conversions) AS conversions,
        ROW_NUMBER() OVER (
            PARTITION BY campaign_type
            ORDER BY SUM(conversions) DESC
        ) AS rn
    FROM digital_marketing_ad_performance_data
    GROUP BY campaign_type, marketing_channel
) t
WHERE rn = 1;


-- =====================================================
-- 5. ROI Ranking by Campaign
-- =====================================================
SELECT
    campaign_name,
    AVG(roi_score) AS avg_roi
FROM digital_marketing_ad_performance_data
GROUP BY campaign_name
ORDER BY avg_roi DESC;


-- =====================================================
-- 6. Quality Score Ranking (REQUESTED QUERY)
-- =====================================================
SELECT
    campaign_name,
    quality_score
FROM digital_marketing_ad_performance_data
ORDER BY quality_score DESC;


-- =====================================================
-- 7. Cost Efficiency Ranking (Lower is Better)
-- =====================================================
SELECT
    campaign_name,
    cost_efficiency_index
FROM digital_marketing_ad_performance_data
ORDER BY cost_efficiency_index ASC;


-- =====================================================
-- 8. High Spend but Low Conversion (Cost Leakage)
-- =====================================================
SELECT
    campaign_name,
    ad_spend,
    conversions,
    cost_efficiency_index
FROM digital_marketing_ad_performance_data
WHERE ad_spend >
      (SELECT AVG(ad_spend) FROM digital_marketing_ad_performance_data)
AND conversions <
      (SELECT AVG(conversions) FROM digital_marketing_ad_performance_data)
ORDER BY cost_efficiency_index DESC;


-- =====================================================
-- 9. Audience Segment Performance
-- =====================================================
SELECT
    audience_segment,
    ROUND(AVG(conversion_rate),4) AS avg_conversion_rate,
    ROUND(AVG(roi_score),2) AS avg_roi,
    ROUND(AVG(cost_efficiency_index),2) AS avg_cost_efficiency
FROM digital_marketing_ad_performance_data
GROUP BY audience_segment
ORDER BY avg_roi DESC;


-- =====================================================
-- 10. Device Type Analysis
-- =====================================================
SELECT
    device_type,
    ROUND(AVG(ctr),4) AS avg_ctr,
    ROUND(AVG(conversion_rate),4) AS avg_conversion_rate,
    ROUND(AVG(roi_score),2) AS avg_roi
FROM digital_marketing_ad_performance_data
GROUP BY device_type;


-- =====================================================
-- 11. Country Performance Benchmark
-- =====================================================
SELECT
    country,
    SUM(conversions) AS conversions,
    ROUND(AVG(roi_score),2) AS avg_roi,
    ROUND(AVG(cost_per_click),2) AS avg_cpc
FROM digital_marketing_ad_performance_data
GROUP BY country
ORDER BY avg_roi DESC;


-- =====================================================
-- 12. Engagement-Driven Campaigns
-- =====================================================
SELECT
    campaign_name,
    engagement_to_spend_ratio,
    ctr,
    roi_score
FROM digital_marketing_ad_performance_data
WHERE engagement_to_spend_ratio >
      (SELECT AVG(engagement_to_spend_ratio)
       FROM digital_marketing_ad_performance_data)
ORDER BY engagement_to_spend_ratio DESC;


-- =====================================================
-- 13. Weekly Performance Trend
-- =====================================================
SELECT
    week_number,
    SUM(impressions) AS impressions,
    SUM(clicks) AS clicks,
    SUM(conversions) AS conversions
FROM digital_marketing_ad_performance_data
GROUP BY week_number
ORDER BY week_number;


-- =====================================================
-- 14. Weekly Conversion Growth (Momentum)
-- =====================================================
SELECT
    week_number,
    SUM(conversions) AS conversions,
    SUM(conversions)
      - LAG(SUM(conversions)) OVER (ORDER BY week_number) AS weekly_growth
FROM digital_marketing_ad_performance_data
GROUP BY week_number
ORDER BY week_number;


-- =====================================================
-- 15. Monthly Spend & Performance
-- =====================================================
SELECT
    month,
    SUM(ad_spend) AS spend,
    SUM(conversions) AS conversions,
    ROUND(AVG(roi_score),2) AS avg_roi
FROM digital_marketing_ad_performance_data
GROUP BY month
ORDER BY month;


-- =====================================================
-- 16. Ad Format Effectiveness
-- =====================================================
SELECT
    ad_format,
    ROUND(AVG(ctr),4) AS avg_ctr,
    ROUND(AVG(conversion_rate),4) AS avg_conversion_rate,
    ROUND(AVG(roi_score),2) AS avg_roi
FROM digital_marketing_ad_performance_data
GROUP BY ad_format
ORDER BY avg_roi DESC;


-- =====================================================
-- 17. Pareto (80/20) ROI Contribution
-- =====================================================
SELECT
    campaign_name,
    roi_score,
    SUM(roi_score) OVER (ORDER BY roi_score DESC) /
    SUM(roi_score) OVER () AS cumulative_roi_share
FROM digital_marketing_ad_performance_data
ORDER BY roi_score DESC;


-- =====================================================
-- 18. Anomaly Detection (Very High ROI)
-- =====================================================
SELECT
    campaign_name,
    roi_score,
    cost_efficiency_index
FROM digital_marketing_ad_performance_data
WHERE roi_score >
      (SELECT AVG(roi_score) + 2 * STDDEV(roi_score)
       FROM digital_marketing_ad_performance_data)
ORDER BY roi_score DESC;


-- =====================================================
-- 19. Campaign Fatigue Detection
-- =====================================================
SELECT
    campaign_name,
    SUM(ad_spend) AS total_spend,
    AVG(ctr) AS avg_ctr
FROM digital_marketing_ad_performance_data
GROUP BY campaign_name
HAVING total_spend >
       (SELECT AVG(ad_spend)
        FROM digital_marketing_ad_performance_data)
AND avg_ctr <
       (SELECT AVG(ctr)
        FROM digital_marketing_ad_performance_data);


-- =====================================================
-- 20. Underperforming Campaigns (Action Needed)
-- =====================================================
SELECT
    campaign_name,
    marketing_channel,
    ctr,
    conversion_rate,
    roi_score
FROM digital_marketing_ad_performance_data
WHERE ctr < 0.05
  AND conversion_rate < 0.20
  AND roi_score < 1;
