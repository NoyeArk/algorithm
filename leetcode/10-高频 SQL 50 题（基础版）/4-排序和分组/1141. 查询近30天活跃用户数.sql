SELECT
    activity_date day,
    COUNT(DISTINCT user_id) active_users
FROM
    Activity
WHERE
    activity_date BETWEEN DATE_SUB('2019-07-27', INTERVAL 29 DAY) AND '2019-07-27'
GROUP BY
    activity_date
ORDER BY
    activity_date