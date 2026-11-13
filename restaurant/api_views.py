from django.contrib.auth.models import User
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, MenuItem
from .serializers import BookingSerializer, MenuItemSerializer, RegistrationSerializer


class MenuPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [MenuPermission]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        requested_date = self.request.query_params.get("date")
        if requested_date:
            queryset = queryset.filter(reservation_date=requested_date)
        return queryset


class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"username": user.username, "token": token.key},
            status=status.HTTP_201_CREATED,
        )
