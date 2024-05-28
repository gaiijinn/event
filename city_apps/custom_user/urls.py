from django.urls import path

from .views import user_index

app_name = 'custom_user'

urlpatterns = [
    path('', user_index, name='user_index')
]
