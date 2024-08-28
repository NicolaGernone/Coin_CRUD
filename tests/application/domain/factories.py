import factory
from factory import Faker
from api.infrastructure.models import Cart, CartItem


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    hash = Faker("pystr", min_chars=64, max_chars=64)


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    id = factory.Faker("uuid4")
    name = factory.Faker("word")
    quantity = factory.Faker("pyint")
    price = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    previous_hash = Faker("pystr", min_chars=64, max_chars=64)
    hash = Faker("pystr", min_chars=64, max_chars=64)
