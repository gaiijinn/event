from city_apps.custom_user.models import User
from city_api.api.serializers import UserSerializer
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

# Create your views here.


class UserViewSet(ModelViewSet):
    queryset = User.objects.select_related('organization', 'user_level').prefetch_related('achievements')
    #queryset = User.objects.select_related('organization', 'user_level')
    #queryset = User.objects.all()
    serializer_class = UserSerializer