from datetime import datetime

from .BaseTest import BaseTestCase
from ..models import Event, EventLog


class EventTrendsTest(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.event1 = Event.objects.create(user=self.user1, name="event1")
        self.event2 = Event.objects.create(user=self.user1, name="event2")

        # Create some event logs
        EventLog.objects.create(
            creator=self.user1,
            event=self.event1,
            event_name=self.event1.name,
            timestamp=datetime(2023, 1, 1),
            data={},
        )
        EventLog.objects.create(
            creator=self.user1,
            event=self.event1,
            event_name=self.event1.name,
            timestamp=datetime(2023, 1, 2),
            data={},
        )
        EventLog.objects.create(
            creator=self.user1,
            event=self.event2,
            event_name=self.event2.name,
            timestamp=datetime(2023, 1, 1),
            data={},
        )

    def test_event_trends(self):
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token1.key)

        response = self.client.get("/api/stats/event_trend")
        print(response.content)
        self.assertEqual(response.status_code, 200)

        expected_data = {
            "2023-01-01": {"event1": 1, "event2": 1},
            "2023-01-02": {"event1": 1},
        }

        self.assertEqual(response.data, expected_data)
