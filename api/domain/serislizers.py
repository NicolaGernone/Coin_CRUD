from rest_framework import serializers

from api.application.services import CartServices
from .entities import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "name", "quantity", "price", "previous_hash", "hash"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "hash", "items"]

    def create(self, validated_data):
        return CartServices.create_cart(data={**validated_data})

    def update(self, instance, validated_data):
        return CartServices.update_cart(cart=instance, data={**validated_data})
