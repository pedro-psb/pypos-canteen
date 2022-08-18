"""Sample product and category data for the demo release"""

from typing import Dict, List

from pypos.models import dao_products

sample_categories = [
    {"name": "Lunch", "description": "All lunch products"},
    {"name": "Breakfast", "description": "All breakfast products"},
    {"name": "Juice", "description": "All juices"},
]


def sample_products() -> List[Dict]:
    return [
        {
            "name": "Big Meal",
            "category_id": dao_products.get_category_by_name("Lunch")["id"],
            "price": 10,
            "file": "big_meal.jpg",
        },
        {
            "name": "Small Meal",
            "category_id": dao_products.get_category_by_name("Lunch")["id"],
            "price": 15,
            "file": "small_meal.jpg",
        },
        {
            "name": "Vegetarian Sandwich",
            "category_id": dao_products.get_category_by_name("Breakfast")["id"],
            "price": 3,
            "file": "vegetarian_sandwich.jpg",
        },
        {
            "name": "Chicken Sandwich",
            "category_id": dao_products.get_category_by_name("Breakfast")["id"],
            "price": 3.5,
            "file": "chicken_sandwich.jpg",
        },
        {
            "name": "Pizza Slice",
            "category_id": dao_products.get_category_by_name("Breakfast")["id"],
            "price": 4,
            "file": "pizza_slice.jpg",
        },
        {
            "name": "Orange Juice",
            "category_id": dao_products.get_category_by_name("Juice")["id"],
            "price": 6,
            "file": "orange_juice.jpg",
        },
        {
            "name": "Grape Juice",
            "category_id": dao_products.get_category_by_name("Juice")["id"],
            "price": 6.5,
            "file": "grape_juice.jpg",
        },
        {
            "name": "Apple Juice",
            "category_id": dao_products.get_category_by_name("Juice")["id"],
            "price": 7,
            "file": "apple_juice.jpg",
        },
    ]
