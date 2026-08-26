from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from materials.models import Course
from users.models import Payment, User
from users.permissions import IsOwnerUser
from users.serializer import PaymentSerializer, UserSerializer
from users.services import (create_stripe_price, create_stripe_product,
                            create_stripe_session)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsOwnerUser]
        elif self.action == "create":
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_fields = ("paid_course", "paid_lesson", "payment_type")
    ordering_fields = ("payment_date",)
    ordering = ("-payment_date",)

    def perform_create(self, serializer):
        payment = serializer.save(
            user=self.request.user,
            payment_date=timezone.now().date(),
        )
        course = Course.objects.get(id=payment.paid_course_id)

        product = create_stripe_product(course.name, f"Курс: {course.name}")
        price = create_stripe_price(product.id, course.price)

        session_id, session_url, amount_total = create_stripe_session(price)
        payment.paid_amount = amount_total / 100
        payment.session_id = session_id
        payment.link = session_url
        payment.save(update_fields=["session_id", "link", "paid_amount"])
