"""Product urls."""

from rest_framework import routers

from backend.apps.users.views import UserViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"users", UserViewSet, basename="user")

urlpatterns = router.urls
