import logging
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

from ..common import Common
from .controller import get_user_by_id, update_user, \
    get_user_settings_by_id

logger = logging.getLogger(__name__)
common_methods = Common()


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        user = get_user_by_id(request.user.id)
        user.theme = get_user_settings_by_id(
            request.user.id).theme

        return JsonResponse(_serialize_user(user))

    @staticmethod
    def put(request):
        user = get_user_by_id(request.user.id)

        data = common_methods.get_request_data(request)
        user.email = data['email']
        user.first_name = data['firstName']
        user.last_name = data['lastName']
        user.login = data['userName']
        user.age = data['age']
        user.street = data['address']['street']
        user.city = data['address']['city']
        user.zip = data['address']['zipCode']
        user.role = data['role']

        update_user(user)

        user.theme = get_user_settings_by_id(
            request.user.id).theme

        return JsonResponse(_serialize_user(user))


class UserSettings(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        user = get_user_settings_by_id(request.user.id)

        return JsonResponse({'themeName': user.theme})

    @staticmethod
    def put(request):
        user_settings = get_user_settings_by_id(request.user.id)

        user_settings.theme = common_methods.get_request_data(
            request)['themeName']
        user_settings.save()

        return JsonResponse({'message': 'User theme was updated'},
                            status=status.HTTP_200_OK)


def _serialize_user(user):
    return {
        'id': user.id,
        'email': user.email,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'userName': user.login,
        'age': user.age,
        'role': user.role,
        'settings': {
            'themeName': user.theme
        },
        'address': {
            'street': user.street,
            'city': user.city,
            'zipCode': user.zip,
        }
    }
