SELECT
    stu.student_id,
    student_name,
    s.subject_name,
    COUNT(e.student_id) attended_exams
FROM
    Students stu
JOIN
    Subjects s
LEFT JOIN
    Examinations e
ON
    stu.student_id = e.student_id
AND
    s.subject_name = e.subject_name
GROUP BY
    stu.student_id,
    student_name,
    s.subject_name
ORDER BY
    stu.student_id,
    s.subject_name