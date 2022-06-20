DROP TABLE IF EXISTS product_category_item;
DROP TABLE IF EXISTS transaction_product_item;
DROP TABLE IF EXISTS transaction_product;
DROP TABLE IF EXISTS role_permission;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS product_category;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS permission;
DROP TABLE IF EXISTS payment_method;
DROP TABLE IF EXISTS canteen;

CREATE TABLE canteen (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE,
  adress TEXT,
  phone TEXT,
  email TEXT
);

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  phone_number TEXT,
  role_name TEXT NOT NULL,
  active INTEGER DEFAULT 1 NOT NULL,
  canteen_id INTEGER NOT NULL,
  FOREIGN KEY(canteen_id) REFERENCES canteen(id)
);

CREATE TABLE role (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  description TEXT NOT NULL,
  canteen_id INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY(canteen_id) REFERENCES canteen(id)
);

CREATE TABLE permission (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT UNIQUE NOT NULL,
  canteen_id INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY(canteen_id) REFERENCES canteen(id)
);


CREATE TABLE role_permission (
  role_name TEXT NOT NULL,
  permission_slug TEXT NOT NULL,
  FOREIGN KEY (role_name) REFERENCES role(name),
  FOREIGN KEY (permission_slug) REFERENCES permission(slug)
);

CREATE TABLE product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  price NUMBER NOT NULL,
  category NUMBER DEFAULT NULL,
  active INTEGER DEFAULT 1 NOT NULL,
  canteen_id INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY(canteen_id) REFERENCES canteen(id)
);

CREATE TABLE product_category (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  description TEXT DEFAULT '',
  active INTEGER DEFAULT 1 NOT NULL,
  canteen_id INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY(canteen_id) REFERENCES canteen(id),
  FOREIGN KEY(canteen_id) REFERENCES canteen(id)
  FOREIGN KEY (id) REFERENCES product(category)
);


CREATE TABLE product_category_item (
  product_id INTEGER NOT NULL,
  product_category_id NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product(id),
  FOREIGN KEY (product_category_id) REFERENCES product_category(id)
);

CREATE TABLE transaction_product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT NOT NULL,
  payment_method INTEGER NOT NULL,
  discount NUMBER NOT NULL DEFAULT 0,
  total_value NUMBER NOT NULL,
  active INTEGER DEFAULT 1 NOT NULL,
  canteen_id INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY(canteen_id) REFERENCES canteen(id)
);

CREATE TABLE transaction_product_item (
  product_id INTEGER NOT NULL,
  transaction_product_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product(id),
  FOREIGN KEY (transaction_product_id) REFERENCES transaction_product(id)
);

CREATE TABLE payment_method (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  canteen_id INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY(canteen_id) REFERENCES canteen(id)
);