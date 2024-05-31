from django.urls import include, path
from rest_framework.routers import DefaultRouter

from city_api.api.views.users_views import (UserAchievementStatusListApiView, UserAchievementViewSet,
                                            UserRetrieveUpdateDestroyAPIView)
from city_api.api.views.events_views import EventTypesModelViewSet, EventModelViewSet, EventGuestsListAPIView

router = DefaultRouter()
router.register('achievements', UserAchievementViewSet)
router.register('event_types', EventTypesModelViewSet)
router.register('events', EventModelViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('user_profile/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user_profile'),
    path('get_user_achievements/', UserAchievementStatusListApiView.as_view(), name='get_user_achievements'),
    path('events/<int:event_id>/guests/', EventGuestsListAPIView.as_view(), name='event-guests'),
]
