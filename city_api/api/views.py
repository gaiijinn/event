from city_apps.custom_user.models import User
from city_api.api.serializers import UserSerializer
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

# Create your views here.


class UserViewSet(ModelViewSet):
    queryset = (User.objects.select_related('user_level')
                .prefetch_related('userachievementstatus_set__achievement'))
    serializer_class = UserSerializer