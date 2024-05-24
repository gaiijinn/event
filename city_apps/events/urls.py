from django.urls import path
from .views import event_index

app_name = 'events'

urlpatterns = [
    path('', event_index, name='event_index')
]