INSERT INTO canteen (name) VALUES ("Canteen 2");
INSERT INTO user (username, password, role_name, canteen_id)
VALUES
  ('owner-user', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'owner', 1),
  ('manager-user', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'manager', 1),
  ('cashier-user', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'cashier', 1),
  ('client', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'client', 1),
  ('dependent-user', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'client_dependent', 1),
  ('canteen_2', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'owner', 2);

INSERT INTO user_account (balance, user_id)
VALUES
(100, 1),
(10, 2),
(0, 3),
(0, 4),
(0, 5);

INSERT INTO product_category (name)
VALUES
  ("Bebidas"),
  ("Lanche"),
  ("Almoço")
  ;

INSERT INTO product (name,price,category)
VALUES
  ("torta de banana", 15, NULL),
  ("torta de maçã", 15, 1),
  ("biscoito de Queijo", 10, 1),
  ("Pão de Queijo", 10, 1),
  ("Prato Feito G", 10, 3),
  ("Prato Feito P", 10, 3)
  ;