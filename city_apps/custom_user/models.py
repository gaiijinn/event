from django.db import models
from django_use_email_as_username.models import BaseUser, BaseUserManager


class OrgType(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.name}"


class Organization(models.Model):
    address = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    type_id = models.ForeignKey(to=OrgType, on_delete=models.CASCADE)


class UserLevels(models.Model):
    name = models.CharField(max_length=128, default='idk')
    low_range = models.SmallIntegerField()
    top_range = models.SmallIntegerField()

    def __str__(self):
        return f"{self.name}"


class UserAchievement(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=256)
    final_value = models.SmallIntegerField()
    given_exp = models.SmallIntegerField()
    image = models.ImageField(upload_to='users/achievements', default='static/achievement/base.jpg')
    for_org = models.BooleanField(default=False)
    for_def_user = models.BooleanField(default=True)

    def __str__(self):
        return f'название - {self.name}, опыт - {self.given_exp}'


class User(BaseUser, models.Model):
    objects = BaseUserManager()
    picture_profile = models.ImageField(upload_to='users/users_picture_profile', null=True, blank=True,
                                        default='static/picture_profile/base.jpg')
    user_level = models.ForeignKey(to=UserLevels, on_delete=models.CASCADE, null=True, blank=True)
    user_rating = models.FloatField(null=True, blank=True, default=0)
    user_exp_right_now = models.SmallIntegerField(null=True, blank=True, default=0)
    achievements = models.ManyToManyField(UserAchievement, through='UserAchievementStatus', related_name='users')

    def check_level(self):
        user_achievement_statuses = UserAchievementStatus.objects.filter(user=self, is_achieved=True)
        total_exp = sum(status.achievement.given_exp for status in user_achievement_statuses)
        user_level = UserLevels.objects.filter(low_range__lte=total_exp, top_range__gte=total_exp).first()

        if not user_level:
            user_level = UserLevels.objects.last()
        else:
            user_level = user_level

        User.objects.filter(pk=self.pk).update(user_exp_right_now=total_exp, user_level=user_level)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(User, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        self.check_level()


class UserAchievementStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(UserAchievement, on_delete=models.CASCADE)
    progress_right_now = models.SmallIntegerField(default=0)
    is_achieved = models.BooleanField(default=False)

    def __str__(self):
        return f"Пользователь {self.user.email}: название - {self.achievement.name}, Достигнуто: {self.is_achieved}"

    def check_if_achieved(self):
        if self.achievement.final_value <= self.progress_right_now:
            self.is_achieved = True
            UserAchievementStatus.objects.filter(pk=self.pk).update(is_achieved=True)   # чтобы не было рекурсии



