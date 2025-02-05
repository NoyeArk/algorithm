SELECT
    b.name
FROM
    Employee a
LEFT JOIN
    Employee b
ON
    a.managerId = b.id
GROUP BY
    b.name,
    b.id
HAVING
    COUNT(b.id) >= 5