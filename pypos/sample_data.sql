INSERT INTO user (username, password,role_name)
VALUES
  ('owner-user', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'owner'),
  ('manager-user', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'manager'),
  ('cashier-user', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'cashier'),
  ('client', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'client'),
  ('dependent-user', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'client_dependent');

INSERT INTO product_category (name)
VALUES
  ("Sem categoria"),
  ("Lanche"),
  ("Almoço")
  ;

INSERT INTO product (name,price,category)
VALUES
  ("torta", 15, 1),
  ("Pão de Queijo", 10, 1),
  ("Prato Feito", 10, 2)
  ;