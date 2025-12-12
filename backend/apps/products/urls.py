"""Product urls."""

from rest_framework import routers

from backend.apps.products.views import ProductViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = router.urls
