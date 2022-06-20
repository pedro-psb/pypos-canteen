INSERT INTO canteen (name) VALUES ("Default Canteen");

INSERT INTO role (name, description)
VALUES
  ("owner", "The creator of the canteen"),
  ("manager", "Manager of products and reports"),
  ("cashier", "The operator of the point of sale"),
  ("client", "The responsible for the credit account"),
  ("client_dependent", "The kid client of the canteen"),
  ("temporary_client", "A kid without finacial responsible"),
  ("generic", "A first logged user")
  ;

INSERT INTO permission (slug)
VALUES
  ("acess_canteen_index"),
  ("acess_product_management"),
  ("acess_employee_management"),
  ("acess_client_management"),
  ("acess_reports"),
  ("acess_pos"),
  ("acess_client_dashboard"),
  ("acess_client_account_management"),
  ("initial_acess")
  ;

INSERT INTO role_permission (role_name, permission_slug)
VALUES
  ("owner", "acess_canteen_index"),
  ("owner", "acess_product_management"),
  ("owner", "acess_client_management"),
  ("owner", "acess_employee_management"),
  ("owner", "acess_reports"),
  ("owner", "acess_pos"),
  ("manager", "acess_canteen_index"),
  ("manager", "acess_product_management"),
  ("manager", "acess_client_management"),
  ("manager", "acess_reports"),
  ("cashier", "acess_canteen_index"),
  ("cashier", "acess_client_management"),
  ("cashier", "acess_reports"),
  ("cashier", "acess_pos"),
  ("client", "acess_client_dashboard"),
  ("client", "acess_client_account_management"),
  ("client_dependent", "acess_client_dashboard"),
  ("generic", "initial_acess")
  ;

INSERT INTO payment_method (name)
VALUES
  ("money"),
  ("credit_card"),
  ("debit_card"),
  ("user_account");