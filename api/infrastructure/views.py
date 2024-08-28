from api.application.domain.serislizers import CartSerializer
from api.application.services import CartServices
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import cart



class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
    @action(detail=True, methods=["post"])
    def delete_item(self, request, pk=None):
        try:
            item_id = request.data.get("item_id")
            quantity = request.data.get("quantity", 1)

            if not item_id or int(quantity) <= 0:
                raise ValidationError("Item ID and a valid quantity are required.")

            cart = Cart.objects.get(pk=pk)
            updated_cart = CartServices.delete_cart_item(cart=cart, item_id=item_id, quantity=int(quantity))

            return Response(CartSerializer(updated_cart).data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)