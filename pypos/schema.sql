DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS product_category;
DROP TABLE IF EXISTS product_category_item;
DROP TABLE IF EXISTS transaction_product;
DROP TABLE IF EXISTS transaction_product_item;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  phone_number TEXT,
  active INTEGER DEFAULT 1 NOT NULL
);

CREATE TABLE role (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  description TEXT NOT NULL
);

CREATE TABLE permission (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT UNIQUE NOT NULL
);

CREATE TABLE user_role (
  user_id INTEGER NOT NULL,
  role_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE role_permission (
  role_id INTEGER NOT NULL,
  permission_id INTEGER NOT NULL,
  FOREIGN KEY (role_id) REFERENCES role(id),
  FOREIGN KEY (permission_id) REFERENCES permission(id)
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
  active INTEGER DEFAULT 1 NOT NULL,
  total_value NUMBER NOT NULL
);

CREATE TABLE transaction_product_item (
  product_id INTEGER NOT NULL,
  transaction_product_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product(id),
  FOREIGN KEY (transaction_product_id) REFERENCES transaction_product(id)
);