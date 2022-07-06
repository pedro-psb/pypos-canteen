INSERT INTO user (username, password, role_name, canteen_id)
VALUES
  ('test',
  'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',
  'owner', 1),
   ('fake_owner',
  'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',
  'owner', 1),
  ('fake_manager',
  'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',
  'manager', 1),
  ('fake_cashier',
  'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',
  'cashier', 1),
  ('fake_client',
  'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',
  'client', 1),
  ('client_canten_2',
  'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',
  'client', 2),
  ('user_child_1',
  'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',
  'client', 1),
  ('user_child_2',
  'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',
  'client', 1);

INSERT INTO user_account (balance, user_id)
VALUES
(100, 1),
(10, 2),
(0, 3),
(0, 4),
(0, 5);

INSERT INTO user_child (age,grade,user_provider_id, user_id)
VALUES
  (5, '4th', 1, 7),
  (7, '5th', 1, 8);

INSERT INTO product_category (name)
VALUES
  ("Lanche"),
  ("Almoço")
  ;

INSERT INTO product (name,price,category)
VALUES
  ("torta", 15.5, 1),
  ("Pão de Queijo", 10, 1),
  ("Prato Feito", 10, 2)
  ;