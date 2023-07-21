from datetime import datetime, date

from django.db.models import Count, functions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError

from .models import Event, EventLog
from .serializers import EventSerializer, EventDataSerializer

class EventList(ListCreateAPIView):
    """
    API for listing and creating events for authenticated users.
    Utilizes the search filter to allow searching for events by name or description.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["name", "description"]

    def get_queryset(self):
        """
        Returns a queryset that only includes events that belong to the authenticated user.

        The `get_queryset` method is used to restrict the list of events that the 
        authenticated user can see and delete. Only events that belong to the user 
        (where `user.id` matches `self.request.user.id`) will be returned.

        Returns:
            A queryset of Event instances.
        """
        return Event.objects.filter(user__id=self.request.user.id)

    def list(self, request):
        """
        Handle GET request for listing events.
        Returns a list of event names in descending order of creation.
        """
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset.order_by('-created_at').values_list('name', flat=True)
        return Response(list(data))

    def perform_create(self, serializer):
        """
        Perform creation of a new event.
        Sets the user_id field of the event to the current user.
        """
        serializer.save(user=self.request.user)

    def post(self, request):
        """
        Handle POST request for creating a new event.

        Validates the request data using the serializer.
        If the data is valid, creates a new event associated with the current user and
        returns a success response with status 201.
        If the data is invalid, returns a response with the validation errors and status 400.
        """
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the event already exists for the current user
            user = self.request.user
            name = serializer.validated_data['name']
            if Event.objects.filter(user=user, name=name).exists():
                raise ValidationError("Event with this name already exists.")

            self.perform_create(serializer)
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class EventUpdateDelete(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete an event.

    A user must be authenticated  to retrieve, update or delete their events. 
    The view only returns the events that belong  to the authenticated user and allows 
    them to delete their own events.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'  # Specifies the model field used for object lookup, 'pk' stands for primary key.

    def get_queryset(self):
        """
        Returns a queryset that only includes events that belong to the authenticated user.

        The `get_queryset` method is used to restrict the list of events that the 
        authenticated user can see, update and delete. Only events that belong to the user 
        (where `user.id` matches `self.request.user.id`) will be returned.

        Returns:
            A queryset of Event instances.
        """
        return Event.objects.filter(user__id=self.request.user.id)
    
class EventLogData(CreateAPIView):
    """
    API endpoint that allows authenticated users to create event log data.

    The endpoint expects a payload containing the event name and any relevant event data. The creator field is 
    automatically set to the current user making the request. If the provided event name does not correspond to 
    an existing event, the request will fail with an appropriate error message.

    """
    
    serializer_class = EventDataSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Overridden method from CreateAPIView to customize the process of saving the instance.
        This method sets the creator field of the event log data to the current authenticated user.

        Args:
            serializer (EventDataSerializer): A serializer instance.
        """
        serializer.save(creator_id=self.request.user.id)

    def create(self, request):
        """
        Handle POST request for creating a new event log data.

        This method validates the incoming data using the serializer, checks if the event exists, and if the event 
        exists, it saves the data and sets the creator to the current authenticated user and the event to the 
        corresponding event instance. If the event does not exist, it returns a response with an error message.

        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        event = Event.objects.filter(name=request.data.get("event_name")).first()
        # If user tries to capture an event that they have not created
        if event is None:
            return Response(
                {
                    "error": "The specified event does not exist. Please create the event first."
                },
                status=HTTP_400_BAD_REQUEST,
            )
        
        serializer.save(creator=request.user, event=event)
        return Response(serializer.data, status=HTTP_201_CREATED)


class EventFrequency(ListAPIView):
    """
    API endpoint that provides event frequency data for authenticated users.

    The endpoint provides the total number of times a specified event has occurred within a given date range.
    If no event name is specified, it returns the count for all events created by the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns a queryset that only includes events that belong to the authenticated user.
        """
        return EventLog.objects.filter(creator_id=self.request.user.id)

    def get(self, request):
        """
        Handle GET request for event frequency data.

        This method retrieves the 'event_name', 'start_date' and 'end_date' parameters from the request.
        If 'event_name' is specified, it returns the count of event logs with that name within the specified date range.
        If 'event_name' is not specified, it returns a count of all events created by the authenticated user.

        Args:
            request (HttpRequest): The request that has triggered this method.

        Returns:
            Response: HttpResponse containing the event frequency data.
        """
        # Assuming we start collecting data from this date, so if no start time is specified,
        # we get everything from the beginning
        app_start_date = datetime(2020, 1, 1)
        event_name = request.query_params.get('event_name')
        start_date = request.query_params.get('start_date') or app_start_date
        end_date = request.query_params.get('end_date') or date.today()

        if event_name:
            count = (
                self.get_queryset()
                .filter(
                    event_name=event_name,
                    timestamp__date__gt=start_date,
                    timestamp__date__lt=end_date,
                )
                .count()
            )
            return Response({"event_name": event_name, "total": count})
        else:
            event_count = (
                self.get_queryset().values("event_name").annotate(total=Count("event_name"))
            )
            return Response(event_count)


class EventTrendsView(ListAPIView):
    """
    API endpoint that provides event trends data for authenticated users.

    The endpoint returns a count of each event logged by the authenticated user per day. 
    The count is grouped by event names.

    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns a queryset that only includes events that belong to the authenticated user.
        """
        return EventLog.objects.filter(creator_id=self.request.user.id)

    @staticmethod
    def format_data(query_set):
        """
        Formats the data received from the queryset into a dictionary.

        The keys of the dictionary are the dates of the events. The values are dictionaries,
        where the keys are the event names and the values are the count of events on that date.

        Args:
            query_set (QuerySet): A QuerySet containing the data to be formatted.

        Returns:
            dict: The formatted data.
        """
        formatted_data = {}
        for item in query_set:
            date_str = item['date'].isoformat()
            if date_str not in formatted_data:
                formatted_data[date_str] = {}
            formatted_data[date_str][item['event_name']] = item['count']

        return formatted_data

    def get(self, request):
        """
        Handle GET request for event trends data.

        This method groups the event logs by date and event name and gets the count of event logs for each group.
        """
        query_set = (
            self.get_queryset().annotate(date=functions.TruncDate("timestamp"))
            .values("date", "event_name")
            .annotate(count=Count("id"))
            .order_by("date", "event_name")
        )

        data = self.format_data(query_set)
        return Response(data)


class LandingPageView(APIView):
    """
    Basic Landing Page View
    """
    def get(self, request):
        return Response({"Welcome to Event Tracker"})
        
