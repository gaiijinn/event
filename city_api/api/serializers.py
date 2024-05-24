from rest_framework import serializers
from city_apps.custom_user.models import User, UserAchievement, UserAchievementStatus


class UserAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAchievement
        fields = ('id', 'name', 'description', 'final_value', 'given_exp', 'image')


class UserAchievementStatusSerializer(serializers.ModelSerializer):
    achievement = UserAchievementSerializer(read_only=True)

    class Meta:
        model = UserAchievementStatus
        fields = ('achievement', 'progress_right_now', 'is_achieved')


class UserSerializer(serializers.ModelSerializer):
    achievements = UserAchievementStatusSerializer(source="userachievementstatus_set", many=True, required=False)
    user_level = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    user_rating = serializers.FloatField(default=0)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'user_level', 'user_rating', 'user_exp_right_now', 'achievements')