# MySQL
################### 1
# a
SELECT
    ProductId,
    COUNT(*) AS ActiveSubscriptions
FROM Subscriptions
WHERE SubscriptionEndDate is NULL OR SubscriptionEndDate > CURDATE()
GROUP BY ProductId
ORDER BY 1 DESC

# b
WITH RECURSIVE UsersSubscriptions AS (
    SELECT
        UserId,
        COUNT(*) AS Subscriptions
    FROM Subscriptions
    WHERE SubscriptionEndDate is NULL OR SubscriptionEndDate > CURDATE()
    GROUP BY UserId
),

SubscriptionsUsers AS (
	SELECT
		Subscriptions,
		COUNT(*) AS Users
	FROM UsersSubscriptions
	GROUP BY Subscriptions
),

Sequence (n) AS (
  SELECT 0
  UNION ALL
  SELECT n + 1 FROM Sequence WHERE n < (SELECT MAX(Subscriptions) FROM SubscriptionsUsers)
)

SELECT 
	s.n AS Subscriptions,
	COALESCE(su.Users, 0) AS Users
FROM SubscriptionsUsers AS su
RIGHT JOIN Sequence AS s ON s.n = su.Subscriptions


################### 2
# 1
WITH distincted_users AS (
	SELECT DISTINCT UserId, ts_date, Platform FROM events WHERE UserId IS NOT NULL 
)

SELECT
	ts_date,
	SUM(CASE WHEN Platform = 'desktop' THEN 1 ELSE 0 END) desktop_count, 
	SUM(CASE WHEN Platform = 'tablet' THEN 1 ELSE 0 END) tablet_count, 
	SUM(CASE WHEN Platform = 'mobile' THEN 1 ELSE 0 END) mobile_count, 
	COUNT(UserId) AS total
FROM distincted_users
GROUP BY 1;


# 2
WWITH dates_platforms AS (
	SELECT
		ts_date,
		SUM(CASE WHEN Platform = 'desktop' THEN 1 ELSE 0 END) desktop_count, 
		SUM(CASE WHEN Platform = 'tablet' THEN 1 ELSE 0 END) tablet_count, 
		SUM(CASE WHEN Platform = 'mobile' THEN 1 ELSE 0 END) mobile_count 
	FROM events
	WHERE UserId IS NOT NULL 
	GROUP BY 1
)

SELECT 
	IF (tablet_count = 0 AND mobile_count = 0, 1, 0) AS used_only_desktop,
	IF (desktop_count = 0 AND mobile_count = 0, 1, 0) AS used_only_tablet,
	IF (desktop_count = 0 AND tablet_count = 0, 1, 0) AS used_only_mobile
FROM dates_platforms


# 3
WITH ActiveSubscriptions AS (
    SELECT
    	DISTINCT
        UserId,
		ProductId
    FROM Subscriptions
    WHERE SubscriptionEndDate is NULL OR SubscriptionEndDate > CURDATE()
),

UniqueUsers AS (
	SELECT DISTINCT UserId, ts_date FROM events WHERE UserId IS NOT NULL 
),

ProductsCounts AS (
	SELECT 
		uu.ts_date,
		SUM(CASE WHEN acs.ProductId = 'pro' THEN 1 ELSE 0 END) AS pro_count, 
		SUM(CASE WHEN acs.ProductId = 'mp' THEN 1 ELSE 0 END) AS mp_count
	FROM
		UniqueUsers AS uu
	LEFT JOIN ActiveSubscriptions AS acs ON
		acs.UserId = uu.UserId
	GROUP BY
		1
)

SELECT 
	ts_date,
	pro_count,
	mp_count,
	pro_count + mp_count AS total
FROM ProductsCounts
ORDER BY 1


################### 3
WITH MaxTotalSubscriptionByDate AS (
	SELECT 
		ts_date,
		MAX(total_subscriptions) AS max_total_subscriptions,
		SUM(total_subscriptions) AS day_total_subscriptions
	FROM Subscriptions_v1
	GROUP BY 1
),

TotalSubscriptionByType AS (
	SELECT 
		page_before_subscription,
		SUM(total_subscriptions) AS type_total_subscriptions
	FROM Subscriptions_v1
	GROUP BY 1
)

SELECT 
	s.ts_date,
	s.page_before_subscription,
	CONCAT(TRUNCATE(total_subscriptions / day_total_subscriptions, 2), '%') AS `Percentage out of total subscription that day`,
	CONCAT(TRUNCATE(total_subscriptions / type_total_subscriptions, 2), '%') AS `Percentage out of total subscription`
FROM
	Subscriptions_v1 AS s
RIGHT JOIN MaxTotalSubscriptionByDate AS ms ON ms.ts_date = s.ts_date
	AND ms.max_total_subscriptions = s.total_subscriptions
LEFT JOIN TotalSubscriptionByType AS ts ON ts.page_before_subscription = s.page_before_subscription

