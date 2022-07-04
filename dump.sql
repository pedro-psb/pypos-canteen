BEGIN TRANSACTION;
CREATE TABLE canteen (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE,
  adress TEXT,
  phone TEXT,
  email TEXT
);
INSERT INTO "canteen" VALUES(1,'Default Canteen',NULL,NULL,NULL);
CREATE TABLE canteen_account(
  id INTEGER PRIMARY KEY,
  cash_balance NUMBER NOT NULL DEFAULT 0,
  bank_account_balance NUMBER NOT NULL DEFAULT 0,
  canteen_id INTEGER UNIQUE NOT NULL,
  FOREIGN KEY (canteen_id) REFERENCES canteen(id)
);
INSERT INTO "canteen_account" VALUES(1,61,0,1);
CREATE TABLE canteen_account_transaction (
  operation_add INTEGER NOT NULL,
  canteen_account_id INTEGER NOT NULL,
  generic_transaction_id INTEGER NOT NULL,
  FOREIGN KEY(canteen_account_id) REFERENCES canteen_account(id),
  FOREIGN KEY(generic_transaction_id) REFERENCES generic_transaction(id)
);
INSERT INTO "canteen_account_transaction" VALUES(1,1,1);
CREATE TABLE generic_transaction (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date_time TEXT NOT NULL,
  total NUMBER NOT NULL,
  canteen_id INTEGER NOT NULL,
  active INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY (canteen_id) REFERENCES canteen(id)
);
INSERT INTO "generic_transaction" VALUES(1,'2022-07-04 13:40:14',61,1,1);
CREATE TABLE payment_info (
  discount NUMBER NOT NULL DEFAULT 0,
  pending INTEGER NOT NULL DEFAULT 0,
  payment_method TEXT NOT NULL,
  generic_transaction_id INTEGER NOT NULL,
  FOREIGN KEY(generic_transaction_id) REFERENCES generic_transaction(id),
  FOREIGN KEY(payment_method) REFERENCES payment_method(name)
);
INSERT INTO "payment_info" VALUES(0,0,'cash',1);
CREATE TABLE payment_method (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);
INSERT INTO "payment_method" VALUES(1,'money');
INSERT INTO "payment_method" VALUES(2,'debit_card');
INSERT INTO "payment_method" VALUES(3,'credit_card');
INSERT INTO "payment_method" VALUES(4,'pix');
CREATE TABLE payment_voucher (
  timestamp_code TEXT NOT NULL,
  generic_transaction_id INTEGER NOT NULL,
  FOREIGN KEY (generic_transaction_id) REFERENCES generic_transaction(id)
);
CREATE TABLE permission (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT UNIQUE NOT NULL,
  canteen_id INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY(canteen_id) REFERENCES canteen(id)
);
INSERT INTO "permission" VALUES(1,'acess_canteen_index',1);
INSERT INTO "permission" VALUES(2,'acess_product_management',1);
INSERT INTO "permission" VALUES(3,'acess_employee_management',1);
INSERT INTO "permission" VALUES(4,'acess_client_management',1);
INSERT INTO "permission" VALUES(5,'acess_reports',1);
INSERT INTO "permission" VALUES(6,'acess_pos',1);
INSERT INTO "permission" VALUES(7,'acess_client_dashboard',1);
INSERT INTO "permission" VALUES(8,'acess_client_account_management',1);
INSERT INTO "permission" VALUES(9,'initial_acess',1);
CREATE TABLE product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  price NUMBER NOT NULL,
  category NUMBER DEFAULT NULL,
  active INTEGER DEFAULT 1 NOT NULL,
  canteen_id INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY(canteen_id) REFERENCES canteen(id)
);
INSERT INTO "product" VALUES(1,'torta',15.5,1,1,1);
INSERT INTO "product" VALUES(2,'Pão de Queijo',10,1,1,1);
INSERT INTO "product" VALUES(3,'Prato Feito',10,2,1,1);
CREATE TABLE product_category (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  description TEXT DEFAULT '',
  active INTEGER DEFAULT 1 NOT NULL,
  canteen_id INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY(canteen_id) REFERENCES canteen(id),
  FOREIGN KEY (id) REFERENCES product(category)
);
INSERT INTO "product_category" VALUES(1,'Lanche','',1,1);
INSERT INTO "product_category" VALUES(2,'Almoço','',1,1);
CREATE TABLE product_category_item (
  product_id INTEGER NOT NULL,
  product_category_id NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product(id),
  FOREIGN KEY (product_category_id) REFERENCES product_category(id)
);
CREATE TABLE role (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  description TEXT NOT NULL,
  canteen_id INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY(canteen_id) REFERENCES canteen(id)
);
INSERT INTO "role" VALUES(1,'owner','The creator of the canteen',1);
INSERT INTO "role" VALUES(2,'manager','Manager of products and reports',1);
INSERT INTO "role" VALUES(3,'cashier','The operator of the point of sale',1);
INSERT INTO "role" VALUES(4,'client','The responsible for the credit account',1);
INSERT INTO "role" VALUES(5,'client_dependent','The kid client of the canteen',1);
INSERT INTO "role" VALUES(6,'temporary_client','A kid without finacial responsible',1);
CREATE TABLE role_permission (
  role_name TEXT NOT NULL,
  permission_slug TEXT NOT NULL,
  FOREIGN KEY (role_name) REFERENCES role(name),
  FOREIGN KEY (permission_slug) REFERENCES permission(slug)
);
INSERT INTO "role_permission" VALUES('owner','acess_canteen_index');
INSERT INTO "role_permission" VALUES('owner','acess_product_management');
INSERT INTO "role_permission" VALUES('owner','acess_client_management');
INSERT INTO "role_permission" VALUES('owner','acess_employee_management');
INSERT INTO "role_permission" VALUES('owner','acess_reports');
INSERT INTO "role_permission" VALUES('owner','acess_pos');
INSERT INTO "role_permission" VALUES('manager','acess_canteen_index');
INSERT INTO "role_permission" VALUES('manager','acess_product_management');
INSERT INTO "role_permission" VALUES('manager','acess_client_management');
INSERT INTO "role_permission" VALUES('manager','acess_reports');
INSERT INTO "role_permission" VALUES('cashier','acess_canteen_index');
INSERT INTO "role_permission" VALUES('cashier','acess_client_management');
INSERT INTO "role_permission" VALUES('cashier','acess_reports');
INSERT INTO "role_permission" VALUES('cashier','acess_pos');
INSERT INTO "role_permission" VALUES('client','acess_client_dashboard');
INSERT INTO "role_permission" VALUES('client','acess_client_account_management');
INSERT INTO "role_permission" VALUES('client_dependent','acess_client_dashboard');
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('canteen',1);
INSERT INTO "sqlite_sequence" VALUES('role',6);
INSERT INTO "sqlite_sequence" VALUES('permission',9);
INSERT INTO "sqlite_sequence" VALUES('payment_method',4);
INSERT INTO "sqlite_sequence" VALUES('user',6);
INSERT INTO "sqlite_sequence" VALUES('product_category',2);
INSERT INTO "sqlite_sequence" VALUES('product',3);
INSERT INTO "sqlite_sequence" VALUES('generic_transaction',1);
CREATE TABLE transaction_product_item (
  product_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  sub_total NUMBER NOT NULL DEFAULT 0,
  generic_transaction_id INTEGER NOT NULL,
  FOREIGN KEY (product_id) REFERENCES product(id),
  FOREIGN KEY (generic_transaction_id) REFERENCES generic_transaction(id)
);
INSERT INTO "transaction_product_item" VALUES(1,2,31,1);
INSERT INTO "transaction_product_item" VALUES(2,3,30,1);
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
INSERT INTO "user" VALUES(1,NULL,'test','pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',NULL,'owner',1,1);
INSERT INTO "user" VALUES(2,NULL,'fake_owner','pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',NULL,'owner',1,1);
INSERT INTO "user" VALUES(3,NULL,'fake_manager','pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',NULL,'manager',1,1);
INSERT INTO "user" VALUES(4,NULL,'fake_cashier','pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',NULL,'cashier',1,1);
INSERT INTO "user" VALUES(5,NULL,'fake_client','pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',NULL,'client',1,1);
INSERT INTO "user" VALUES(6,NULL,'client_canten_2','pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',NULL,'client',1,2);
CREATE TABLE user_account (
  id INTEGER PRIMARY KEY,
  balance NUMBER NOT NULL DEFAULT 0,
  negative_limit REAL NOT NULL DEFAULT 50,
  user_id INTEGER UNIQUE NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id)
);
INSERT INTO "user_account" VALUES(1,100,50.0,1);
INSERT INTO "user_account" VALUES(2,10,50.0,2);
INSERT INTO "user_account" VALUES(3,0,50.0,3);
INSERT INTO "user_account" VALUES(4,0,50.0,4);
INSERT INTO "user_account" VALUES(5,0,50.0,5);
CREATE TABLE user_account_transaction (
  operation_add INTEGER NOT NULL,
  user_account_id INTEGER NOT NULL,
  generic_transaction_id INTEGER NOT NULL,
  FOREIGN KEY(user_account_id) REFERENCES user_account(id),
  FOREIGN KEY(generic_transaction_id) REFERENCES generic_transaction(id)
);
COMMIT;
