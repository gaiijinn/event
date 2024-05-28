from django.contrib import admin

from .models import (Organization, OrgType, User, UserAchievement,
                     UserAchievementStatus, UserLevels)

# Register your models here.

admin.site.register(User)
admin.site.register(Organization)
admin.site.register(OrgType)
admin.site.register(UserLevels)
admin.site.register(UserAchievement)
admin.site.register(UserAchievementStatus)
