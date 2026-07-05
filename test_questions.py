test_cases = [

    # ---------- SIMPLE (single table, basic filters) ----------
    {
        "question": "Show me all customers from Chicago",
        "expected_sql": "SELECT * FROM customers WHERE city = 'Chicago';"
    },
    {
        "question": "How many orders had late delivery?",
        "expected_sql": "SELECT COUNT(*) AS late_orders FROM orders WHERE delivery_status = 'Late delivery';"
    },
    {
        "question": "List all customers from the Corporate segment",
        "expected_sql": "SELECT * FROM customers WHERE segment = 'Corporate';"
    },
    {
        "question": "How many customers are there in the West region?",
        "expected_sql": "SELECT COUNT(*) AS total FROM customers WHERE region = 'West';"
    },
    {
        "question": "Show all orders shipped using Same Day shipping",
        "expected_sql": "SELECT * FROM orders WHERE shipping_type = 'Same Day';"
    },
    {
        "question": "How many products are in the Furniture category?",
        "expected_sql": """
            SELECT COUNT(*) AS total
            FROM products p
            JOIN categories cat ON p.category_id = cat.category_id
            WHERE cat.category_name = 'Furniture';
        """
    },
    {
        "question": "How many orders were canceled?",
        "expected_sql": "SELECT COUNT(*) AS canceled_orders FROM orders WHERE delivery_status = 'Shipping canceled';"
    },

    # ---------- MEDIUM (one JOIN + GROUP BY) ----------
    {
        "question": "What is the total sales for each category?",
        "expected_sql": """
            SELECT cat.category_name, SUM(oi.sales_per_order) AS total_sales
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            JOIN categories cat ON p.category_id = cat.category_id
            GROUP BY cat.category_name;
        """
    },
    {
        "question": "What is the total profit for each region?",
        "expected_sql": """
            SELECT c.region, SUM(oi.profit_per_order) AS total_profit
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            JOIN customers c ON o.customer_id = c.customer_id
            GROUP BY c.region;
        """
    },
    {
        "question": "How many orders were placed by each customer segment?",
        "expected_sql": """
            SELECT c.segment, COUNT(*) AS total_orders
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            GROUP BY c.segment;
        """
    },
    {
        "question": "What is the average discount given per category?",
        "expected_sql": """
            SELECT cat.category_name, AVG(oi.order_item_discount) AS avg_discount
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            JOIN categories cat ON p.category_id = cat.category_id
            GROUP BY cat.category_name;
        """
    },
    {
        "question": "How many orders were shipped using each shipping type?",
        "expected_sql": """
            SELECT shipping_type, COUNT(*) AS total_orders
            FROM orders
            GROUP BY shipping_type;
        """
    },
    {
        "question": "What is the total quantity ordered for each category?",
        "expected_sql": """
            SELECT cat.category_name, SUM(oi.order_quantity) AS total_quantity
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            JOIN categories cat ON p.category_id = cat.category_id
            GROUP BY cat.category_name;
        """
    },
    {
        "question": "How many orders had late delivery in each shipping type?",
        "expected_sql": """
            SELECT shipping_type, COUNT(*) AS late_orders
            FROM orders
            WHERE delivery_status = 'Late delivery'
            GROUP BY shipping_type;
        """
    },
    {
        "question": "What is the total profit for each customer segment?",
        "expected_sql": """
            SELECT c.segment, SUM(oi.profit_per_order) AS total_profit
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            JOIN customers c ON o.customer_id = c.customer_id
            GROUP BY c.segment;
        """
    },
    {
        "question": "How many customers are there in each state?",
        "expected_sql": """
            SELECT state, COUNT(*) AS total_customers
            FROM customers
            GROUP BY state;
        """
    },

    # ---------- HARDER (multi-JOIN, ORDER BY + LIMIT, nested logic) ----------
    {
        "question": "Which region has the highest profit?",
        "expected_sql": """
            SELECT c.region, SUM(oi.profit_per_order) AS total_profit
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            JOIN customers c ON o.customer_id = c.customer_id
            GROUP BY c.region
            ORDER BY total_profit DESC
            LIMIT 1;
        """
    },
    {
        "question": "Show me the top 5 products by quantity sold",
        "expected_sql": """
            SELECT p.product_name, SUM(oi.order_quantity) AS total_quantity
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            GROUP BY p.product_name
            ORDER BY total_quantity DESC
            LIMIT 5;
        """
    },
    {
        "question": "List the top 5 customers by total profit",
        "expected_sql": """
            SELECT c.customer_id, c.first_name, c.last_name, SUM(oi.profit_per_order) AS total_profit
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            JOIN customers c ON o.customer_id = c.customer_id
            GROUP BY c.customer_id, c.first_name, c.last_name
            ORDER BY total_profit DESC
            LIMIT 5;
        """
    },
    {
        "question": "Which category generates the least total sales?",
        "expected_sql": """
            SELECT cat.category_name, SUM(oi.sales_per_order) AS total_sales
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            JOIN categories cat ON p.category_id = cat.category_id
            GROUP BY cat.category_name
            ORDER BY total_sales ASC
            LIMIT 1;
        """
    },
    {
        "question": "What are the top 3 states by number of orders?",
        "expected_sql": """
            SELECT c.state, COUNT(*) AS total_orders
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            GROUP BY c.state
            ORDER BY total_orders DESC
            LIMIT 3;
        """
    },
    {
        "question": "Which shipping type has the highest average real shipment days?",
        "expected_sql": """
            SELECT shipping_type, AVG(days_for_shipment_real) AS avg_days
            FROM orders
            GROUP BY shipping_type
            ORDER BY avg_days DESC
            LIMIT 1;
        """
    },
    {
        "question": "Show me the top 5 products by total profit",
        "expected_sql": """
            SELECT p.product_name, SUM(oi.profit_per_order) AS total_profit
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            GROUP BY p.product_name
            ORDER BY total_profit DESC
            LIMIT 5;
        """
    },
    {
        "question": "Which customer segment has the highest average sales per order?",
        "expected_sql": """
            SELECT c.segment, AVG(oi.sales_per_order) AS avg_sales
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            JOIN customers c ON o.customer_id = c.customer_id
            GROUP BY c.segment
            ORDER BY avg_sales DESC
            LIMIT 1;
        """
    },
    {
        "question": "What is the total number of orders per region for the Technology category?",
        "expected_sql": """
            SELECT c.region, COUNT(*) AS total_orders
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN products p ON oi.product_id = p.product_id
            JOIN categories cat ON p.category_id = cat.category_id
            WHERE cat.category_name = 'Technology'
            GROUP BY c.region;
        """
    },

]