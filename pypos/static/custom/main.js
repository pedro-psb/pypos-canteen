function add_item_to_order(id, price, name) {
    const order_items = document.querySelector('#order_items');
    const order_ids = order_items.querySelectorAll('tr');

    // check if id exist in order items
    let item_exist = false;
    for (i of order_ids) {
        if (id == i.id) {
            item_exist = i.id;
        }
    }

    // handle add or update of item row
    if (item_exist) {
        const current_row = order_items.querySelector(`tr[id="${item_exist}"]`);
        let row_quantity = current_row.querySelector('.row_quantity').value;
        let row_price = current_row.querySelector('.row_price').innerHTML;
        let row_total = parseFloat((parseInt(row_quantity) + 1) * row_price);
        current_row.querySelector('.row_quantity').value = parseInt(row_quantity) + 1;
        current_row.querySelector('.row_total').innerHTML = row_total.toFixed(2);
    } else {
        const order_items_len = order_items.children.length;
        const row_total = parseFloat(price).toFixed(2);
        var row = order_items.insertRow(order_items_len);
        row.id = id;
        row.innerHTML = `
            <td><button onclick="remove_item_from_order(${id});" class="btn btn-secondary">x</button></td>
            <td>
                <div class="row_id">${id}</div>
            </td>
            <td>
                <div class="row_name">${name}</div>
            </td>
            <td>
                <input type="number" class="row_quantity" value="1">
            </td>
            <td>
                <div class="row_price">${price}</div>
            </td>
            <td>
                <div class="row_total">${row_total}</div>
            </td>
        `
    }
    update_order_total();
}

function update_order_total() {
    let order_items = document.querySelector('#order_items');
    let order_item_prices = order_items.querySelectorAll('.row_total');
    let total = 0.0;
    for (price of order_item_prices) {
        total = total + parseFloat(price.innerHTML);
    }
    if (total > 0) {
        document.querySelector('#order_foot').innerHTML = `
            <tr>
                <td colspan=5 class="text-end">Total</td>
                <td>${total}</td>
            </tr>
        `
    } else {
        document.querySelector('#order_foot').innerHTML = "";
    }
    update_form();
}

function remove_item_from_order(id) {
    document.querySelector(`tr[id="${id}"]`).remove();
    update_order_total();
}

function reset_order() {
    document.querySelector('#order_items').innerHTML = null;
    update_order_total();
}

function update_form() {
    let order_items = document.querySelector('#order_items');
    let order_rows = order_items.querySelectorAll('tr');

    let order = {
        products: [],
        discount: document.querySelector('#discount').value
    };

    // add products to order
    for (row of order_rows) {
        var product = {
            id: row.querySelector('.row_id').innerHTML,
            quantity: row.querySelector('.row_quantity').value
        }
        order.products.push(product);
    }

    // update products and discount form values
    document.querySelector('#form_products').value = JSON.stringify(order.products);
    document.querySelector('#form_discount').value = order.discount;
    console.log(document.querySelector('#form_products').value)
    console.log(document.querySelector('#form_discount').value)
}

// add onclick event to cards (can be made harcoded to the html onclick, since it is generated in the backend)
var products = document.querySelector('#products').children;
for (card of products) {
    card.onclick = function (e) {
        var current_card = e.currentTarget;
        var row_id = current_card.querySelector('.row_id').innerHTML;
        var row_price = current_card.querySelector('.row_price').innerHTML;
        var row_name = current_card.querySelector('.row_name').innerHTML;
        add_item_to_order(row_id, row_price, row_name);
    }
}