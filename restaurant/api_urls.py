from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .api_views import BookingViewSet, MenuItemViewSet, RegistrationView


router = DefaultRouter()
router.register("menu-items", MenuItemViewSet, basename="menu-item")
router.register("bookings", BookingViewSet, basename="api-booking")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegistrationView.as_view(), name="api-register"),
    path("token/", obtain_auth_token, name="api-token"),
]
