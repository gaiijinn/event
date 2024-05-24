from rest_framework import serializers
from city_apps.custom_user.models import User, UserAchievement, UserAchievementStatus


class UserAchievementStatusSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='achievement.id')
    name = serializers.ReadOnlyField(source='achievement.name')
    description = serializers.ReadOnlyField(source='achievement.description')
    final_value = serializers.ReadOnlyField(source='achievement.final_value')
    given_exp = serializers.ReadOnlyField(source='achievement.given_exp')
    image = serializers.ReadOnlyField(source='achievement.image.url')


    class Meta:
        model = UserAchievementStatus
        fields = ('id', 'achievement', 'name', 'description', 'description', 'final_value', 'given_exp',
                  'progress_right_now', 'is_achieved', 'image')


class UserSerializer(serializers.ModelSerializer):
    user_level = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    achievements = UserAchievementStatusSerializer(source="userachievementstatus_set", many=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'organization',
                  'user_level', 'user_rating', 'user_exp_right_now', 'achievements')