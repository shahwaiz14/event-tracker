from .BaseTest import BaseTestCase
from ..models import Event, EventLog


class EventFrequencyTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.event1 = Event.objects.create(user=self.user1, name="event1")
        self.event2 = Event.objects.create(user=self.user1, name="event2")

        # Create event logs
        EventLog.objects.create(
            creator=self.user1, event=self.event1, event_name=self.event1.name, data={}
        )
        EventLog.objects.create(
            creator=self.user1, event=self.event1, event_name=self.event1.name, data={}
        )
        EventLog.objects.create(
            creator=self.user1, event=self.event2, event_name=self.event2.name, data={}
        )

    def test_frequency_of_specific_event(self):
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token1.key)

        response = self.client.get(
            "/api/stats/event_frequency", params={"event_name": "event1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0], {"event_name": "event1", "total": 2})

    def test_frequency_of_all_events(self):
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token1.key)

        response = self.client.get("/api/stats/event_frequency")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn({"event_name": "event1", "total": 2}, response.data)
        self.assertIn({"event_name": "event2", "total": 1}, response.data)
