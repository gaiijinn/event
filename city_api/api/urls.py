from django.urls import include, path
from rest_framework.routers import DefaultRouter

from city_api.api.views.events_views import UserAchievementViewSet
from city_api.api.views.users_views import (UserAchievementStatusListApiView,
                                            UserRetrieveUpdateAPIView)

router = DefaultRouter()
router.register('achievements', UserAchievementViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),

    path('user_profile/', UserRetrieveUpdateAPIView.as_view(), name='user_profile'),
    path('get_user_achievements/', UserAchievementStatusListApiView.as_view(), name='get_user_achievements'),
]
