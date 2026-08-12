from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import UserViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register("users", UserViewSet, basename="user")

urlpatterns = []

urlpatterns += router.urls
