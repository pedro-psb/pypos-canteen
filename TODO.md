
# Fronend

* Create site map and implement basic pages and navigation
* Redefine routes so products are inside /manager

# Sistema de gerenciamento de produtos/categorias

## product.py

* Refactor Database acess with DAO
* Refactor validationss with some Pattern.
* Add auth restriction to the product management.

## erros.py and dependencies

* Lookup for better error message convention ex:  ADD_PRODUCT_INTEGRITY_ERROR

## tests/test_products.py::test_add_product_validation

* Assert message in request.text (it shows the redirect content, not ir destination)
