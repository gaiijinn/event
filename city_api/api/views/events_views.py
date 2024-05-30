from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from city_apps.events.models import EventGuests, Events, EventTypes
from city_api.api.serializers import EventTypeSerializer, EventSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters import rest_framework as filters

# Create your views here.


class EventTypesModelViewSet(ModelViewSet):
    serializer_class = EventTypeSerializer
    queryset = EventTypes.objects.all()
    permission_classes = (IsAdminUser, )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('event_type', )


class EventModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    pagination_class = None
    serializer_class = EventSerializer
    queryset = Events.objects.filter().order_by('-id')
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('event_name', 'event_type', 'date')

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).select_related('user', 'event_type')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
