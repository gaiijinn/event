import django_filters
from city_apps.custom_user.models import UserAchievementStatus, User, UserAchievement
from django_filters import rest_framework as filters


class UserAchievementFilter(filters.FilterSet):
    for_org = filters.BooleanFilter(field_name='for_org')
    for_def_user = filters.BooleanFilter(field_name='for_def_user')

    class Meta:
        model = UserAchievement
        fields = ('for_org', 'for_def_user')


class UserAchievementStatusFilter(filters.FilterSet):
    class Meta:
        model = UserAchievementStatus
        fields = ('is_achieved', 'achievement__name')
