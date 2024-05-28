from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, UserAchievement, UserAchievementStatus


@receiver(post_save, sender=User)
def create_user_achievements(sender, instance, created, **kwargs):
    if created:
        all_achievements = UserAchievement.objects.all()
        for achievement in all_achievements:
            UserAchievementStatus.objects.create(
                user=instance,
                achievement=achievement,
                is_achieved=False,
                progress_right_now=0,
            )


@receiver(post_save, sender=UserAchievement)
def create_user_achievement_statuses(sender, instance, created, **kwargs):
    if created:
        users = User.objects.all()
        for user in users:
            UserAchievementStatus.objects.create(
                user=user,
                achievement=instance,
                is_achieved=False,
                progress_right_now=0,
            )


@receiver(post_save, sender=UserAchievementStatus)
def update_user_info(sender, instance, created, **kwargs):
    if not created:
        instance.check_if_achieved()

        user = instance.user
        user.check_level()
