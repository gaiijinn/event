import django.core.exceptions

from city_apps.custom_user.models import User, UserAchievement, UserAchievementStatus
from city_api.api.serializers import UserSerializer, UserAchievementSerializer, UserAchievementStatusSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
# Create your views here.


class UserAchievementViewSet(ModelViewSet):
    queryset = UserAchievement.objects.all().order_by('-id')
    serializer_class = UserAchievementSerializer
    permission_classes = (IsAdminUser, )


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

    def get_queryset(self):
        return UserAchievementStatus.objects.all()

    def check_param(self, param):
        try:
            if param == "True" or param == "False":
                param = param
            else:
                param = None
        except django.core.exceptions.ValidationError:
            param = None

        return param

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        param = self.request.query_params.get('is_achieved')

        param = self.check_param(param)
        if param is not None:
            queryset = self.get_queryset().filter(user=request.user, is_achieved=param)

        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)