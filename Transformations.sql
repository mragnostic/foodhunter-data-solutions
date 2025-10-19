-- getting down the columns from the orders table
select
column_name from information_schema.columns
where
table_schema = "foodhunter" and table_name = "orders";

--
desc foodhunter.orders;

--
select min(order_date) as first_date_orders, 
max(order_date) as last_date_orders 
from foodhunter.orders;

--
select
column_name from information_schema.columns
where
table_schema = "foodhunter" and table_name = "orders_items";

--
desc foodhunter.orders_items;

--
select
column_name from information_schema.columns
where
table_schema = "foodhunter" and table_name = "restaurants";

--
desc foodhunter.restaurants;

--
