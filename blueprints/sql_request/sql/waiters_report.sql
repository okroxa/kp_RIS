SELECT
    Waitername,
    COUNT(*) AS Amount,
    SUM(Ordersum) AS Summ
FROM
    (SELECT
        idWaiters, Ordersum
    FROM
        `cr_restaurant`.order
    WHERE
        YEAR(Orderdate) = '$year'
            AND MONTH(Orderdate) = '$month') ordForDate
        JOIN
    Waiters USING (idWaiters)
GROUP BY Waitername