"""Product views."""

from rest_framework import decorators, filters, mixins, response, viewsets
from rest_framework.permissions import IsAuthenticated

from backend.apps.products.filters import ProductFilter
from backend.apps.products.models import Product
from backend.apps.products.serializers import ProductSerializer
from backend.apps.products.services import ProductService


class ProductViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
):
    """ProductViewSet."""

    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by("-created_at")
    lookup_field = "id"
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["created_at"]

    @decorators.action(detail=False, methods=["get"], url_path="info")
    def info(self, request):
        """Return quota information."""
        info_res = ProductService.get_quota_info()
        return response.Response(info_res)

    @decorators.action(detail=False, methods=["get"], url_path="update-stats")
    def update_stats(self, request):
        """Force update stats."""
        ProductService.update_stats()
        return response.Response({"message": "update stats successfully"})
