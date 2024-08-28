import uuid
from django.db import models
from model_utils.models import TimeStampedModel


class Cart(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hash = models.CharField(max_length=64, blank=True, null=True, editable=False)

    def __str__(self):
        return str(self.id)


class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    id = models.UUIDField(primary_key=True, editable=True)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    previous_hash = models.CharField(
        max_length=64, blank=True, null=True, editable=False
    )
    hash = models.CharField(max_length=64, blank=True, null=True, editable=False)

    def __str__(self):
        return str(self.id)
