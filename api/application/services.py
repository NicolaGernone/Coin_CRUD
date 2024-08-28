import hashlib
import time
import uuid
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from api.models import Cart, CartItem

class CartServices:

    @staticmethod
    def calculate_hash(index: str, previous_hash: str, timestamp: int, data: str) -> str:
        value = str(index) + str(previous_hash) + str(timestamp) + str(data)
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    @staticmethod
    def calculate_previous_hash(item: CartItem) -> CartItem:
        if not item.previous_hash:
            try:
                last_item = CartItem.objects.filter(cart=item.cart).latest("created")
                item.previous_hash = last_item.hash
            except CartItem.DoesNotExist:
                item.previous_hash = item.cart.hash

        if not item.hash:
            item.hash = CartServices.calculate_hash(
                item.id, item.previous_hash, int(time.time()), item.name
            )
        item.save()
        return item

    @staticmethod
    def create_item(cart: Cart, items: list) -> None:
        cart_item = list(CartItem.objects.filter(cart=cart))
        for item in items:
            previous_hash = cart.hash if len(cart_item) == 0 else cart_item[-1].hash
            cart_item.append(
                CartItem.objects.create(
                    cart=cart,
                    id=item["id"],
                    name=item["name"],
                    quantity=item["quantity"],
                    price=item["price"],
                    previous_hash=previous_hash,
                    hash=CartServices.calculate_hash(
                        item["id"], previous_hash, int(time.time()), item["name"]
                    ),
                )
            )

    @staticmethod
    def create_cart(data: dict) -> Cart:
        id = uuid.uuid4()
        hash = CartServices.calculate_hash(id, "0", int(time.time()), "Genesis Block")
        cart = Cart.objects.create(id=id, hash=hash)
        CartServices.create_item(cart=cart, items=list(data["items"]))
        return cart

    @staticmethod
    def update_cart(cart: Cart, data: dict) -> Cart:
        CartServices.create_item(cart=cart, items=list(data["items"]))
        return cart

    @staticmethod
    def delete_cart_item(cart: Cart, item_id: str, quantity: int) -> Cart:
        cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)

        if cart_item.quantity <= quantity:
            cart_item.delete()
        else:
            cart_item.quantity -= quantity
            cart_item.save()

        return cart
