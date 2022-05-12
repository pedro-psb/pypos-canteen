# General

- Use markdown extesion

# Frontend

- [ ] Create site map and implement basic pages and navigation
- [ ] Redefine routes so products are inside /manager

# Sistema de gerenciamento de produtos/categorias

- [ ] Create package for this system /management/
- [ ] Add models for Products and Categories. /management/models.py
  - These model responsabiliies will be
    - to validate it's own data
    - do CRUD operations.

## product.py

- [ ] Refactor Database acess with GEneral purpose DAO
- [ ] Refactor validationss with some Pattern.
- [ ] Add auth restriction to the product management.

## erros.py and dependencies

- [ ] Lookup for better error message convention ex:  ADD_PRODUCT_INTEGRITY_ERROR

## Tests

### tests/test_products.py::test_add_product_validation

- [x] Assert message in request.text (it shows the redirect content, not it destination)
- [ ] Not finding error message in response data for encoding reasons.
