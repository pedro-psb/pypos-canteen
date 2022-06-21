/*
Run this to test:
cat test.sql | sqlite3 instance/pypos.sqlite
*/

SELECT tp.date, pm.name AS payment_method, tp.discount, tp.total_value,
group_concat('{"name":"' || p.name || '","quantity":"' || tpi.quantity || '"}') AS products
FROM transaction_product tp
INNER JOIN transaction_product_item tpi ON tp.id=tpi.transaction_product_id
INNER JOIN product p ON p.id = tpi.product_id
INNER JOIN payment_method pm ON tp.payment_method = pm.id
GROUP BY tp.id HAVING p.canteen_id=2;


/* PRODUCT CATEGORY IS WORKING
SELECT p.id, p.name, p.price, p.active, pc.name as category_name
FROM product p LEFT JOIN product_category pc ON p.category = pc.id
WHERE p.canteen_id=2;

/*
-- SELECT pm.name FROM transaction_product tp
-- INNER JOIN transaction_product_item tpi ON tp.id=tpi.transaction_product_id
-- INNER JOIN product p ON p.id = tpi.product_id
-- INNER JOIN payment_method pm ON tp.payment_method = pm.id
-- GROUP BY tp.id;


/* Nested structure of Transactions
-- SELECT tp.date, tp.payment_method, tp.discount, tp.total_value,
-- group_concat('{"name":' || p.name || ',"quantity":' || tpi.quantity || '}') as products
-- FROM transaction_product tp
-- INNER JOIN transaction_product_item tpi ON tp.id=tpi.transaction_product_id
-- INNER JOIN product p ON p.id = tpi.product_id
-- GROUP BY tp.id;

/* SELECT pc.id, pc.name as category_name, COUNT(*) as products_inside
-- FROM product p INNER JOIN product_category pc ON p.category = pc.id
-- GROUP BY pc.id;

/*
-- SELECT * FROM product;
-- INSERT INTO product(name, price, category) VALUES('bar', 2.0, 1);
-- SELECT * FROM product;
 
/*
-- DELETE FROM product WHERE id=7;
-- SELECT * FROM user;
-- SELECT * FROM product;
-- SELECT * FROM product_category;


/* select category id, name and count of products belonging to it
-- SELECT pc.id, pc.name, COUNT(*) as products_inside
-- FROM product_category pc INNER JOIN product p ON p.category = pc.id
-- GROUP BY pc.id UNION
-- SELECT pc.id, pc.name, '0' as products_inside
-- FROM product_category pc LEFT JOIN product p ON p.category = pc.id
-- WHERE p.id IS NULL;