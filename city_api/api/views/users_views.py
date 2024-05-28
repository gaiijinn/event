from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from city_api.api.filters import UserAchievementStatusFilter
from city_api.api.serializers import (UserAchievementStatusSerializer,
                                      UserSerializer)
from city_apps.custom_user.models import User, UserAchievementStatus


# профиль юзера
class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return User.objects.select_related('user_level').prefetch_related('userachievementstatus_set__achievement')

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(pk=self.request.user.pk)
        return obj


class UserAchievementStatusListApiView(ListAPIView):
    serializer_class = UserAchievementStatusSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserAchievementStatusFilter

    def get_queryset(self):
        return UserAchievementStatus.objects.all()

    @method_decorator(cache_page(60))  # 2мин
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        filter_queryset = self.filter_queryset(queryset)
        serializer = self.serializer_class(filter_queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
