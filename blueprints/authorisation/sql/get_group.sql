SELECT
    groupName, idWaiter
FROM
    user_groups
WHERE
   login = '$login' AND password = '$password'