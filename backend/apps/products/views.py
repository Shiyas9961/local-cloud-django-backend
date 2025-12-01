"""Product views."""
from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated

from backend.apps.products.models import Product
from backend.apps.products.serializers import ProductSerializer
from backend.apps.products.filters import ProductFilter


class ProductViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-created_at')
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["created_at"]