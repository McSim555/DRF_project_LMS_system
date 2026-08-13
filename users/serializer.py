from rest_framework.serializers import ModelSerializer

from materials.serializer import PaymentSerializer
from users.models import User


class UserSerializer(ModelSerializer):
    payment_date = PaymentSerializer(many=True, source="payment")

    class Meta:
        model = User
        fields = "__all__"
