from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK

from .BaseTest import BaseTestCase
from ..models import Event


class EventLogDataTest(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_create_event_log_data(self):
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token1.key)
        # Make the request
        self.event = Event.objects.create(
            name="Event1", description="Test Event", user=self.user1
        )
        response = self.client.post(
            "/api/eventlogs/",
            {"event_name": "Event1", "data": {"key": "value"}},
            format="json",
        )
        # Check the response
        self.assertEqual(response.status_code, 201, response.content)
        self.assertEqual(response.data["event_name"], self.event.name)
        self.assertEqual(response.data["data"], {"key": "value"})

    def test_create_event_log_data_non_existent_event(self):
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token1.key)
        # Make the request
        response = self.client.post(
            "/api/eventlogs/",
            {"event_name": "NonExistentEvent", "data": {"key": "value"}},
            format="json",
        )
        # Check the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {
                "error": "The specified event does not exist. Please create the event first."
            },
        )
