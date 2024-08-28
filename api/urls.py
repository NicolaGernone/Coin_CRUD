from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.infrastructure.views import CartViewSet

router = DefaultRouter()
router.register(r"carts", CartViewSet, basename="carts")

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
]
