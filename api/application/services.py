import hashlib
import time
import uuid

from api.application.domain.entities import Cart, CartItem


class CartServices:
    """
    Calculates a SHA256 hash using the provided index, previous_hash, timestamp, and data.

    Parameters:
    index (str): The index of the item.
    previous_hash (str): The hash of the previous item.
    timestamp (int): The creation timestamp of the item.
    data (str): The name of the item.

    Returns:
    str: The calculated hash.
    """

    @staticmethod
    def calculate_hash(
        index: str, previous_hash: str, timestamp: int, data: str
    ) -> str:
        value = str(index) + str(previous_hash) + str(timestamp) + str(data)
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    """
    Calculates the previous hash of an item and assigns it to the item.

    Parameters:
    item (CartItem): The item to calculate the previous hash for.

    Returns:
    CartItem: The item with assigned previous_hash and hash.
    """

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

    """
    Creates new items for a cart.

    Parameters:
    cart (Cart): The cart to add items to.
    items (list): The items to add to the cart.

    Returns:
    None
    """

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

    """
    Creates a new cart and its associated items.

    Parameters:
    data (dict): The data for the new cart and items.

    Returns:
    Cart: The created cart.
    """

    @staticmethod
    def create_cart(data: dict) -> Cart:
        id = uuid.uuid4()
        hash = CartServices.calculate_hash(id, "0", int(time.time()), "Genesis Block")
        cart = Cart.objects.create(id=id, hash=hash)
        CartServices.create_item(cart=cart, items=list(data["items"]))
        return cart

    """
    Updates a cart by adding new items to it.

    Parameters:
    cart (Cart): The cart to update.
    data (dict): The data for the new items.

    Returns:
    Cart: The updated cart.
    """

    @staticmethod
    def update_cart(cart: Cart, data: dict) -> Cart:
        # Add at the end of the chain
        CartServices.create_item(cart=cart, items=list(data["items"]))
        return cart
