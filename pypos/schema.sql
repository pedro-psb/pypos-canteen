DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS product_category;
DROP TABLE IF EXISTS product_category_item;
DROP TABLE IF EXISTS transaction_product;
DROP TABLE IF EXISTS transaction_product_item;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  price NUMBER NOT NULL,
  category NUMBER DEFAULT NULL,
  active INTEGER DEFAULT 1 NOT NULL 
);

CREATE TABLE product_category (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  active INTEGER DEFAULT 1 NOT NULL,
  FOREIGN KEY (id) REFERENCES product(category)
);


CREATE TABLE product_category_item (
  product_id INTEGER NOT NULL,
  product_category_id NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product(id),
  FOREIGN KEY (product_category_id) REFERENCES product_category(id)
);

CREATE TABLE transaction_product (
  id INTEGER PRIMARY KEY,
  date TEXT NOT NULL,
  total_value NUMBER NOT NULL
);

CREATE TABLE transaction_product_item (
  product_id INTEGER NOT NULL,
  product_transaction_id NOT NULL,
  active INTEGER DEFAULT 1 NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product(id),
  FOREIGN KEY (product_transaction_id) REFERENCES transaction_product(id)
);