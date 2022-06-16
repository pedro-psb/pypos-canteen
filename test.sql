/*
Run this to test:
cat test.sql | sqlite3 instance/pypos.sqlite 
*/

SELECT * FROM transaction_product;

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