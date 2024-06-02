from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from city_apps.events.models import EventGuests, Events, EventTypes
from city_api.api.serializers import EventTypeSerializer, EventSerializer, EventGuestSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data)



class EventGuestsListAPIView(ListAPIView):
    queryset = EventGuests.objects.all().prefetch_related('user')
    permission_classes = (IsAuthenticated, )
    pagination_class = None
    serializer_class = EventGuestSerializer

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        event = get_object_or_404(Events, pk=event_id)
        return self.queryset.filter(event=event).all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data)
