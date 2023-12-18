select Waitername, Orderamount, Ordersum
from `cr_restaurant`.order join waiters using(idWaiters)
where Orderdate = '$date'