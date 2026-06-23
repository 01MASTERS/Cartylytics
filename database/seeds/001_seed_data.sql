-- ============================================================
-- Cartlytics – Seed Data (minimal smoke-test dataset)
-- Run AFTER the ETL pipeline if you want a quick sanity check
-- without generating the full 3,000-order CSV dataset.
-- ============================================================

USE cartlytics;

-- Categories
INSERT IGNORE INTO categories (id, name, slug, description, parent_id, is_active) VALUES
(1,  'Electronics',       'electronics',       'Consumer electronics',           NULL, 1),
(2,  'Clothing',          'clothing',          'Apparel and fashion',             NULL, 1),
(3,  'Home & Garden',     'home-and-garden',   'Home improvement and garden',     NULL, 1),
(4,  'Sports & Outdoors', 'sports-and-outdoors','Fitness and outdoor gear',       NULL, 1),
(5,  'Books',             'books',             'Books and publications',          NULL, 1),
(6,  'Laptops',           'laptops',           'Laptop computers',                1,    1),
(7,  'Smartphones',       'smartphones',       'Mobile phones',                   1,    1),
(8,  'Accessories',       'accessories',       'Tech accessories',                1,    1),
(9,  'Mens Wear',         'mens-wear',         'Men\'s clothing',                 2,    1),
(10, 'Womens Wear',       'womens-wear',       'Women\'s clothing',               2,    1);

-- Products
INSERT IGNORE INTO products (id,sku,name,description,category_id,cost_price,selling_price,stock_qty,brand,is_active) VALUES
(1,  'EL-LAP-001', 'ProBook 15 Laptop',              'High-performance 15-inch laptop',     6,  450.00, 899.99,  120, 'TechPro',   1),
(2,  'EL-LAP-002', 'UltraSlim 13 Laptop',            'Portable 13-inch ultrabook',          6,  520.00, 1099.99, 80,  'NovaTech',  1),
(3,  'EL-PHN-001', 'Galaxy X12 Smartphone',          '6.5-inch Android flagship',           7,  180.00, 499.99,  200, 'Samsung',   1),
(4,  'EL-PHN-002', 'iPhone 15 Pro',                  'Apple flagship smartphone',           7,  550.00, 1199.99, 150, 'Apple',     1),
(5,  'EL-PHN-003', 'Pixel 8 Pro',                    'Google flagship smartphone',          7,  300.00, 699.99,  100, 'Google',    1),
(6,  'EL-ACC-001', 'Noise-Cancelling Headphones',    'Premium wireless headphones',         8,  45.00,  149.99,  300, 'SoundWave', 1),
(7,  'EL-ACC-002', 'Wireless Charger 20W',           'Fast wireless charging pad',          8,  12.00,  39.99,   500, 'ChargeFast',1),
(8,  'CL-MEN-001', 'Classic Chino Pants',            'Slim-fit chino trousers',             9,  18.00,  59.99,   400, 'UrbanWear', 1),
(9,  'CL-MEN-002', 'Oxford Button Shirt',            'Classic Oxford weave shirt',          9,  14.00,  49.99,   350, 'UrbanWear', 1),
(10, 'CL-WOM-001', 'Floral Wrap Dress',              'Summer floral wrap dress',            10, 16.00,  54.99,   300, 'Blossom',   1),
(11, 'CL-WOM-002', 'Slim Fit Jeans',                 'High-waist slim fit denim',           10, 20.00,  64.99,   280, 'DenimCo',   1),
(12, 'HG-001',     'Cordless Drill Set',             '18V cordless drill with bits',        3,  55.00,  129.99,  180, 'BuildRight',1),
(13, 'HG-002',     'Ceramic Plant Pots Set',         'Set of 3 ceramic pots',               3,  8.00,   29.99,   450, 'GreenHome', 1),
(14, 'HG-003',     'Smart Air Purifier',             'HEPA smart air purifier',             3,  85.00,  199.99,  120, 'AirPure',   1),
(15, 'SO-001',     'Yoga Mat Premium',               'Non-slip premium yoga mat',           4,  12.00,  44.99,   500, 'FlexFit',   1),
(16, 'SO-002',     'Running Shoes Pro',              'Cushioned road running shoes',        4,  45.00,  119.99,  250, 'SpeedRun',  1),
(17, 'SO-003',     'Resistance Bands Set',           'Set of 5 resistance bands',           4,  8.00,   24.99,   600, 'FlexFit',   1),
(18, 'BK-001',     'Python for Data Science',        'Hands-on guide to Python analytics',  5,  15.00,  39.99,   300, 'TechBooks', 1),
(19, 'BK-002',     'The Lean Startup',               'Build-measure-learn methodology',     5,  9.00,   19.99,   400, 'BizPress',  1),
(20, 'BK-003',     'Atomic Habits',                  'Building good habits, breaking bad',  5,  8.00,   17.99,   500, 'LifeBooks', 1);

-- Sample customers (10 rows)
INSERT IGNORE INTO customers
  (id,email,first_name,last_name,phone,gender,date_of_birth,city,state,region,country,zip_code,segment,is_active,created_at)
VALUES
(1,'sophia.m@example.com','Sophia','Martinez','555-0101','Female','1988-03-14','Los Angeles','CA','West','United States','90001','Consumer',1,'2022-01-15 09:00:00'),
(2,'james.w@example.com','James','Wilson','555-0102','Male','1975-07-22','New York','NY','Northeast','United States','10001','Corporate',1,'2022-01-20 10:30:00'),
(3,'emma.j@example.com','Emma','Johnson','555-0103','Female','1992-11-05','Austin','TX','South','United States','73301','Consumer',1,'2022-02-01 08:15:00'),
(4,'liam.a@example.com','Liam','Anderson','','Male','1985-05-18','Chicago','IL','Central','United States','60601','Small Business',1,'2022-02-10 14:00:00'),
(5,'olivia.d@example.com','Olivia','Davis','555-0105','Female','1997-09-30','Seattle','WA','West','United States','98101','Consumer',1,'2022-03-05 11:45:00'),
(6,'noah.b@example.com','Noah','Brown','555-0106','Male','1983-12-12','Miami','FL','South','United States','33101','Corporate',1,'2022-03-18 09:30:00'),
(7,'isabella.g@example.com','Isabella','Garcia','555-0107','Female','1990-04-25','Denver','CO','Northwest','United States','80201','Home Office',1,'2022-04-02 13:20:00'),
(8,'william.t@example.com','William','Taylor','555-0108','Male','1979-08-08','Boston','MA','Northeast','United States','02101','Consumer',1,'2022-04-14 10:00:00'),
(9,'mia.j@example.com','Mia','Jackson','555-0109','Female','1995-01-19','Atlanta','GA','Southeast','United States','30301','Consumer',1,'2022-05-01 15:30:00'),
(10,'james.l@example.com','James','Lee','555-0110','Male','1987-06-27','Portland','OR','Northwest','United States','97201','Small Business',1,'2022-05-15 08:45:00');

-- Sample orders (5 rows)
INSERT IGNORE INTO orders
  (id,order_number,customer_id,status,order_date,shipped_date,delivered_date,
   shipping_city,shipping_state,shipping_region,shipping_country,shipping_zip,
   payment_method,discount_pct,shipping_fee,subtotal,discount_amount,total_amount)
VALUES
(1,'ORD-2022-000001',1,'delivered','2022-02-10 10:00:00','2022-02-11 12:00:00','2022-02-14 15:00:00','Los Angeles','CA','West','United States','90001','Credit Card',10,0,1199.99,120.00,1079.99+0),
(2,'ORD-2022-000002',2,'delivered','2022-03-05 14:30:00','2022-03-06 09:00:00','2022-03-09 11:00:00','New York','NY','Northeast','United States','10001','Credit Card',0,7.99,899.99,0,907.98),
(3,'ORD-2022-000003',3,'delivered','2022-04-18 09:15:00','2022-04-19 10:00:00','2022-04-22 14:00:00','Austin','TX','South','United States','73301','PayPal',5,4.99,209.98,10.50,204.47),
(4,'ORD-2022-000004',1,'delivered','2022-06-22 16:00:00','2022-06-23 08:00:00','2022-06-26 13:00:00','Los Angeles','CA','West','United States','90001','Credit Card',0,0,149.99,0,149.99),
(5,'ORD-2022-000005',4,'shipped','2022-07-11 11:30:00','2022-07-12 09:00:00',NULL,'Chicago','IL','Central','United States','60601','Debit Card',15,9.99,1099.99,165.00,944.98);

-- Sample order items
INSERT IGNORE INTO order_items
  (id,order_id,product_id,quantity,unit_price,unit_cost,discount_pct,line_revenue,line_cost,line_profit)
VALUES
(1, 1, 4, 1, 1199.99, 550.00, 10, 1079.99, 550.00, 529.99),
(2, 2, 1, 1, 899.99,  450.00, 0,  899.99,  450.00, 449.99),
(3, 3, 15,2, 44.99,   12.00,  5,  85.48,   24.00,  61.48),
(4, 3, 7, 3, 39.99,   12.00,  5,  113.97,  36.00,  77.97),
(5, 4, 6, 1, 149.99,  45.00,  0,  149.99,  45.00,  104.99),
(6, 5, 2, 1, 1099.99, 520.00, 15, 934.99,  520.00, 414.99);
