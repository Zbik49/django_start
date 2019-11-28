from rest_framework.serializers import ModelSerializer

from .models import UserPaymentDetails


class UserPaymentDetailsSerializer(ModelSerializer):
    class Meta:
        model = UserPaymentDetails
        fields = ['__all__']
