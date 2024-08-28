import time
from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TestCase
from api.application.domain.entities import Cart, CartItem
from api.application.services import CartServices
from tests.application.domain.factories import CartFactory, CartItemFactory


class CartServicesTestCase(TestCase):
    def setUp(self):
        self.cart = CartFactory()
        self.cart_item = CartItemFactory(cart=self.cart)

    def test_calculate_hash(self):
        index = "1"
        previous_hash = "0"
        timestamp = int(time.time())
        data = "Genesis Block"
        hash = CartServices.calculate_hash(index, previous_hash, timestamp, data)
        self.assertIsInstance(hash, str)

    def test_calculate_previous_hash(self):
        item = CartServices.calculate_previous_hash(self.cart_item)
        self.assertIsNotNone(item.previous_hash)

    def test_create_item(self):
        items = [
            {
                "id": "dc26df26-684d-11ec-95f2-3c5282ead1f8",
                "name": "test_item",
                "quantity": 1,
                "price": "9.99",
            }
        ]
        CartServices.create_item(self.cart, items)
        cart_item = CartItem.objects.get(id="dc26df26-684d-11ec-95f2-3c5282ead1f8")
        self.assertEqual(cart_item.name, "test_item")

    def test_create_cart(self):
        data = {
            "items": [
                {
                    "id": "dc26df26-684d-11ec-95f2-3c5282ead1f8",
                    "name": "test_item",
                    "quantity": 1,
                    "price": "9.99",
                }
            ]
        }
        cart = CartServices.create_cart(data)
        self.assertIsInstance(cart, Cart)

    def test_update_cart(self):
        data = {
            "items": [
                {
                    "id": "e692679a-684d-11ec-96c3-3c5282ead1f8",
                    "name": "test_item_2",
                    "quantity": 2,
                    "price": "19.99",
                }
            ]
        }
        updated_cart = CartServices.update_cart(self.cart, data)
        self.assertEqual(updated_cart.items.count(), 2)

    def test_create_item_negative_quantity(self):
        items = [
            {"id": "test-id", "name": "test_item", "quantity": -1, "price": "9.99"}
        ]
        with self.assertRaises(ValidationError):
            CartServices.create_item(self.cart, items)

    def test_create_item_negative_price(self):
        items = [
            {"id": "test-id", "name": "test_item", "quantity": 1, "price": "-9.99"}
        ]
        with self.assertRaises(ValidationError):
            CartServices.create_item(self.cart, items)

    def test_create_item_empty_name(self):
        items = [{"id": "test-id", "name": "", "quantity": 1, "price": "9.99"}]
        with self.assertRaises(ValidationError):
            CartServices.create_item(self.cart, items)

    def test_create_item_duplicate_id(self):
        items = [
            {
                "id": self.cart_item.id,
                "name": "test_item",
                "quantity": 1,
                "price": "9.99",
            }
        ]
        with self.assertRaises(IntegrityError):
            CartServices.create_item(self.cart, items)
