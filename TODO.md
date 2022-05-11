
# Sistema de gerenciamento de produtos/categorias

product.py

* Refactor CRUD
* Lookup for better error message convention ex:  ADD_PRODUCT_INTEGRITY_ERROR
* Fix tests/test_products.py::test_add_product_validation
  * Assert message in request.text (it shows the redirect content, not ir destination)
