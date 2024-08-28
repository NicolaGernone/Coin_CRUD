from api.application.domain.serislizers import CartSerializer
from rest_framework import viewsets
from .models import Cart


"""
API endpoint for interacting with Cart objects.

Use the following endpoints to interact with this view:

GET /api/carts/ :
    Retrieves a list of all Cart objects.

POST /api/carts/ :
    Creates a new Cart object. The request body should contain a JSON representation of the Cart.
    For example:
        {
            "items": [
                {
                    "id": "<item_id>",
                    "name": "<item_name>",
                    "quantity": <quantity>,
                    "price": <price>
                },
                ...
            ]
        }

GET /api/carts/<cart_id>/ :
    Retrieves a detailed view of a specific Cart object by ID.
    
PATCH /api/carts/<cart_id>/ :
    Partially updates a specific Cart object by ID. The request body should contain a JSON representation of the state changes to apply to the Cart.
    The request body should contain a JSON representation of the Cart.
    For example:
        {
            "items": [
                {
                    "id": "<item_id>",
                    "name": "<item_name>",
                    "quantity": <quantity>,
                    "price": <price>
                },
                ...
            ]
        }


DELETE /api/carts/<cart_id>/ :
    Deletes a specific Cart object by ID.

"""


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
