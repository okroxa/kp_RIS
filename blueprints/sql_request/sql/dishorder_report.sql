SELECT
    Menuname,
    COUNT(*) AS Amount,
    SUM(Dishamount) * Menucost AS Summ
FROM
    Menu
        JOIN
    Orderstring USING (idMenu)
        JOIN
    (SELECT
        idOrder
    FROM
        `cr_restaurant`.order
    WHERE
        YEAR(Orderdate) = '$year'
            AND MONTH(Orderdate) = '$month') forDate USING (idOrder)
GROUP BY Menuname