from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserAchievementViewSet, UserRetrieveUpdateAPIView, UserAchievementStatusListApiView

router = DefaultRouter()
router.register('achievements', UserAchievementViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('user_profile/', UserRetrieveUpdateAPIView.as_view(), name='user_profile'),
    path('get_user_achievements/', UserAchievementStatusListApiView.as_view(), name='get_user_achievements'),
]
