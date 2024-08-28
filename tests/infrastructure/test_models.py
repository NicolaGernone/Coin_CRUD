import time
from django.test import TestCase
from api.infrastructure.models import Cart, CartItem
from api.application.services import CartServices
from tests.application.domain.factories import CartFactory, CartItemFactory


class CartModelTest(TestCase):
    def setUp(self):
        self.cart = CartFactory.create()

    def test_cart_creation(self):
        self.assertIsInstance(self.cart, Cart)
        self.assertEqual(self.cart.__str__(), str(self.cart.id))

    def test_cart_hash(self):
        self.assertIsNotNone(self.cart.hash)


class CartItemModelTest(TestCase):
    def setUp(self):
        self.cart = CartFactory.create()
        self.cart_item = CartItemFactory.create(cart=self.cart)

    def test_cart_item_creation(self):
        self.assertIsInstance(self.cart_item, CartItem)
        self.assertEqual(self.cart_item.__str__(), self.cart_item.id)

    def test_cart_item_hash(self):
        self.assertIsNotNone(self.cart_item.hash)

    def test_cart_item_linked_to_cart(self):
        self.assertEqual(self.cart, self.cart_item.cart)

    def test_cart_item_previous_hash(self):
        self.assertIsNotNone(self.cart_item.previous_hash)
