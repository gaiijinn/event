from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from city_api.api.filters import UserAchievementFilter

from city_api.api.filters import UserAchievementStatusFilter
from city_api.api.serializers import (UserAchievementStatusSerializer,
                                      UserSerializer, UserAchievementSerializer)
from city_apps.custom_user.models import User, UserAchievementStatus, UserAchievement
from rest_framework.parsers import MultiPartParser, FormParser
from django.core import cache


# профиль юзера
class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, )
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return User.objects.select_related('user_level')

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(id=self.request.user.id)
        return obj


class UserAchievementStatusListApiView(ListAPIView):
    serializer_class = UserAchievementStatusSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserAchievementStatusFilter

    def get_queryset(self):
        return UserAchievementStatus.objects.all()

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        filter_queryset = self.filter_queryset(queryset)
        serializer = self.serializer_class(filter_queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


#######

class UserAchievementViewSet(ModelViewSet):
    queryset = UserAchievement.objects.all().order_by('-id')
    serializer_class = UserAchievementSerializer
    pagination_class = None
    permission_classes = (IsAdminUser, )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserAchievementFilter

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
