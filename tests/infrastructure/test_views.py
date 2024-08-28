from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from tests.application.domain.factories import CartFactory


class CartViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cart = CartFactory()
        self.url = reverse("api:carts-list")

    def test_get_cart_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_cart(self):
        url = reverse("api:carts-detail", kwargs={"pk": self.cart.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.cart.id))

    def test_create_cart(self):
        data = {
            "items": [
                {
                    "id": "d29d573d-b5d3-4419-85a8-81c91fe22724",
                    "name": "item_6",
                    "quantity": 1,
                    "price": 34,
                }
            ]
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_cart(self):
        url = reverse("api:carts-detail", kwargs={"pk": self.cart.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_cart_empty_items(self):
        data = {"items": []}
        response = self.client.post("/api/carts/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_cart_invalid_item_id(self):
        data = {
            "items": [
                {"id": "invalid-id", "name": "test_item", "quantity": 1, "price": 9.99}
            ]
        }
        response = self.client.patch(f"/api/carts/{self.cart.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_cart_non_existent_cart(self):
        data = {
            "items": [
                {"id": "test-id", "name": "test_item", "quantity": 1, "price": 9.99}
            ]
        }
        response = self.client.patch("/api/carts/non_existent_id/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_cart_non_existent(self):
        response = self.client.delete("/api/carts/non_existent_id/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_cart_conflict(self):
        data = {
            "items": [
                {
                    "id": "d29d573d-b5d3-4419-85a8-81c91fe22724",
                    "name": "item_6",
                    "quantity": 1,
                    "price": 34,
                }
            ]
        }
        # Firstly, create the cart normally
        response = self.client.patch(f"/api/carts/{self.cart.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Now, attempt to update the cart with the previous data
        # This should create a conflict as the cart state has already been updated
        response = self.client.patch(f"/api/carts/{self.cart.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
