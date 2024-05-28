from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from city_api.api.filters import UserAchievementFilter
from city_api.api.serializers import UserAchievementSerializer
from city_apps.custom_user.models import UserAchievement

# Create your views here.


class UserAchievementViewSet(ModelViewSet):
    queryset = UserAchievement.objects.all().order_by('-id')
    serializer_class = UserAchievementSerializer
    pagination_class = None
    permission_classes = (IsAdminUser, )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserAchievementFilter

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
