$(document).ready(function () {
    $(document).on('select2:open', () => {
        document.querySelector('.select2-search__field').focus();
    });

    $('#user_select').select2();
    console.log($('#user_select'))
});

function add_item_to_order(id, price, name) {
    const order_items = document.querySelector('#order');
    const order_ids = order_items.querySelectorAll('tr');
    const order_items_len = order_items.children.length;

    // check if id exist in order items
    let item_exist = false;
    for (i of order_ids) {
        if (id == i.dataset.id) {
            item_exist = i.dataset.id;
        }
    }

    // handle add or update of item row
    if (item_exist) {
        const current_row = order_items.querySelector(`tr[data-id="${item_exist}"]`);
        var row_quantity = current_row.dataset.quantity;
        var row_price = current_row.dataset.price;
        var row_total = parseFloat((parseInt(row_quantity) + 1) * row_price);
        row_total = row_total.toFixed(2);
        row_quantity = parseInt(row_quantity) + 1;

        current_row.querySelector('.row_quantity').value = row_quantity;
        current_row.querySelector('.row_total').innerHTML = row_total;
        current_row.dataset.quantity = row_quantity;
        current_row.dataset.total = row_total;
    }
    else {
        var row = order_items.insertRow(order_items_len);
        price = parseFloat(price).toFixed(2);

        row.dataset.id = id;
        row.dataset.name = name;
        row.dataset.price = price;
        row.dataset.total = price;
        row.dataset.quantity = 1;
        row.innerHTML = `
                <td"><span class="text-muted">
                <button type="button" class="btn-close btn-secondary" aria-label="Close"></button>
                </td></span>
                <td class="">${name}</td>
                <td class="">${price}</td>
                <td class="w-25">
                <input class="form-control row_quantity" type="number" name="quantity" value="1"></td>
                <td class="row_total">${price}</td>
            `
        var quantity_input = row.querySelector('input[name="quantity"');
        var clear_row = row.querySelector('button');

        quantity_input.addEventListener('input', function () {
            row.dataset.quantity = quantity_input.value;
            row.dataset.total = (parseFloat(parseInt(row.dataset.quantity)) * row.dataset.price).toFixed(2);
            row.querySelector('.row_total').innerHTML = row.dataset.total;
            update_form();
        });
        clear_row.addEventListener('click', function () {
            document.querySelector(`tr[data-id="${id}"]`).remove();
            update_form();
        });
    }
    update_form();
}

function update_form() {
    let order_items = document.querySelector('#order').children;

    let order = {
        products: [],
        discount: document.querySelector('#discount').value,
        payment_method: '1'
    };

    // add products to order
    for (row of order_items) {
        var product = {
            id: row.dataset.id,
            quantity: row.dataset.quantity
        }
        order.products.push(product);
    }

    // update products and discount form values
    document.querySelector('#form_products').value = JSON.stringify(order.products);
    document.querySelector('#form_discount').value = order.discount;
    document.querySelector('#form_payment_method').value = order.payment_method;
    update_order_total();
    console.log(document.querySelector('#form_products').value)
    console.log(document.querySelector('#form_discount').value)
    console.log(document.querySelector('#form_payment_method').value)
}

function update_order_total() {
    // calculate final total
    let order_items = document.querySelector('#order').children;
    let discount = document.querySelector('#discount').value;

    // handle discount input
    if (discount) {
        discount = parseFloat(discount).toFixed(2);
    } else {
        discount = 0.0.toFixed(2);
    }

    // calculate total
    let total = 0.0;
    for (item of order_items) {
        total = total + parseFloat(item.dataset.total);
    }
    total = (total - discount).toFixed(2);
    if (total > 0) {
        document.querySelector('#final_total').innerHTML = `$${total}`;
    } else {
        document.querySelector('#final_total').innerHTML = "$0";
    }
}

// add onclick event to cards (can be made harcoded to the html onclick, since it is generated in the backend)
var products = document.querySelectorAll('.product');
for (card of products) {
    card.onclick = function (e) {
        var current_card = e.currentTarget.dataset;
        var card_id = current_card.id;
        var card_price = current_card.price;
        var card_name = current_card.name;
        add_item_to_order(card_id, card_price, card_name);
    }
}

// updating form triggers
var discount_input = document.querySelector('#discount');
var order = document.querySelector('#order');
var clear_order = document.querySelector('#clear_order_button');

discount.addEventListener('input', update_form);
clear_order.addEventListener('click', function () {
    document.querySelector('#order').innerHTML = null;
    update_form();
});