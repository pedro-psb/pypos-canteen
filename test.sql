SELECT pc.id, pc.name as category_name, COUNT(*) as products_inside
FROM product p INNER JOIN product_category pc ON p.category = pc.id
GROUP BY pc.id;