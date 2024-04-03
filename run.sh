docker compose run -p 9090:9090 marketsvc
# curl -v http://localhost:9090/
# curl http://localhost:9090/api/customers
# curl http://localhost:9090/api/orders?cust_id=1
# curl http://localhost:9090/api/order_total?order_id=1
# curl "http://localhost:9090/api/orders_between_dates?after=2024-03-14&before=2024-03-22"
# curl -H "Content-Type: application/json" -d '{"customer_id":1,"items":[{"id":2,"quantity":4},{"id":3,"quantity":6}]}' http://localhost:9090/api/add_new_order