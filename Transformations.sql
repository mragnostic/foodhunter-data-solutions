-- processing and creating staging tables for dashboard views in order to minimize processing time and computational overhead by utilizing pre-prepared datasets.

CREATE OR REPLACE TABLE foodhunter_reports.daily_order_summary AS
(
    SELECT
        order_date,
        day_category,
        COUNT(distinct order_id) AS total_orders,
        COUNT(distinct Customer_id) AS total_Customers,
        SUM(delivery_duration) / COUNT(distinct order_id) AS avg_delivery_duration,
        SUM(total_price) AS total_price,
        SUM(delivery_fee) AS delivery_fee,
        SUM(revenue) AS revenue
    FROM
        (SELECT
          order_date,
          CASE WHEN DAYOFWEEK(order_date) IN (1,7) THEN "Week-End" ELSE "Week-Day" END AS day_category,
          order_id,
          customer_id,
          TIME_TO_SEC(TIMEDIFF(delivered_time, order_time))/60 AS delivery_duration,
          total_price,
          delivery_fee,
          discount,
          final_price AS revenue
        FROM 
          foodhunter.orders) t1
    GROUP BY order_date, day_category
);

CREATE OR REPLACE TABLE foodhunter.reports.weekly_order_summary AS
(
    WITH base_data AS(
      SELECT
        week_,
        COUNT(distinct order_id) AS total_orders,
        COUNT(distinct Customer_id) AS total_Customers,
        SUM(delivery_duration) / COUNT(distinct order_id) AS avg_delivery_duration,
        SUM(total_price) AS total_price,
        SUM(delivery_fee) AS delivery_fee,
        SUM(revenue) AS revenue
      FROM
        (SELECT
          order_date,
          DATE_ADD(order_date, INTERVAL((4 - WEEKDAY(order_date) + 7) % 7) DAY) AS week_,
          order_id,
          customer_id,
          TIME_TO_SEC(TIMEDIFF(delivered_time, order_time))/60 AS delivery_duration,
          total_price,
          delivery_fee,
          discount,
          final_price AS revenue
        FROM 
          foodhunter.orders) t1
      GROUP BY week_
    )
)


-- https://github.com/MbawithTech/Data-Science/blob/main/Synergix_data_preprocessed_new.csv