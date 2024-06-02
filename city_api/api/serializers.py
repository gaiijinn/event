from rest_framework import serializers

from city_apps.custom_user.models import (User, UserAchievement,
                                          UserAchievementStatus)

from city_apps.events.models import EventTypes, Events, EventGuests


class UserAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAchievement
        fields = ('id', 'name', 'description', 'final_value', 'given_exp', 'image', 'for_org', 'for_def_user')


class UserAchievementStatusSerializer(serializers.ModelSerializer):
    achievement = UserAchievementSerializer(read_only=True)

    class Meta:
        model = UserAchievementStatus
        fields = ('achievement', 'progress_right_now', 'is_achieved')


class UserSerializer(serializers.ModelSerializer):
    user_level = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    user_rating = serializers.FloatField(default=0)
    user_exp_right_now = serializers.IntegerField(default=0)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'picture_profile',
                  'user_level', 'user_rating', 'user_exp_right_now')


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTypes
        fields = ('id', 'event_type', )


class EventSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()
    event_type = serializers.SlugRelatedField(
        queryset=EventTypes.objects.all(),
        slug_field='event_type'
    )

    class Meta:
        model = Events
        fields = ('id', 'user_full_name', 'event_name', 'event_descr', 'event_type', 'event_address', 'date',
                  'begin_time', 'end_time', 'event_main_photo', 'additional_event_photo', 'price', 'coordinates')

    def get_user_full_name(self, obj):
        return obj.user.get_full_name()

    def validate(self, data):
        request = self.context.get('request')
        if request and 'event_main_photo' not in request.FILES:
            raise serializers.ValidationError(
                {"event_main_photo": "Key 'event_main_photo' not found in uploaded files."})
        return data


class EventGuestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = EventGuests
        fields = ('user', )