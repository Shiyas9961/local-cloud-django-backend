from rest_framework import viewsets, permissions, mixins
from .serializers import UserSerializer
from .models import User

class UserViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # change for update/list as needed
    lookup_field = "id"
    # you might want to override get_permissions to restrict list/update/delete to admins/self.