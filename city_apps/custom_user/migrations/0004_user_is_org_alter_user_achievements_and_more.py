# Generated by Django 5.0.6 on 2024-05-25 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0003_remove_user_organization_alter_user_achievements'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_org',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='achievements',
            field=models.ManyToManyField(related_name='users', through='custom_user.UserAchievementStatus', to='custom_user.userachievement'),
        ),
        migrations.AlterField(
            model_name='user',
            name='picture_profile',
            field=models.ImageField(blank=True, default='static/picture_profile/base.jpg', null=True, upload_to='users/users_picture_profile'),
        ),
        migrations.AlterField(
            model_name='userachievement',
            name='image',
            field=models.ImageField(default='static/achievement/base.jpg', upload_to='users/achievements'),
        ),
    ]