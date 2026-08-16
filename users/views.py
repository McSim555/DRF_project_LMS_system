from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User, Payment
from users.serializer import UserSerializer, PaymentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_fields = ("paid_course", "paid_lesson", "payment_type")
    ordering_fields = ("payment_date",)
    ordering = ("-payment_date",)
