INSERT INTO role (name, description)
VALUES
  ("owner", "The creator of the canteen"),
  ("manager", "Manager of products and reports"),
  ("cashier", "The operator of the point of sale"),
  ("client", "The responsible for the credit account"),
  ("client_dependent", "The kid client of the canteen"),
  ("temporary_client", "A kid without finacial responsible")
  ;

INSERT INTO permission (slug)
VALUES
  ("acess_product_management"),
  ("acess_reports"),
  ("acess_pos"),
  ("acess_client_dashboard")
  ;

INSERT INTO role_permission (role_name, permission_slug)
VALUES
  ("owner", "acess_product_management"),
  ("owner", "acess_reports"),
  ("owner", "acess_pos"),
  ("manager", "acess_product_management"),
  ("manager", "acess_reports"),
  ("cashier", "acess_reports"),
  ("cashier", "acess_pos"),
  ("client", "acess_client_dashboard")
  ;