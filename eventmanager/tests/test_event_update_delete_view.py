from .BaseTest import BaseTestCase
from ..models import Event


class EventUpdateDeleteTestClass(BaseTestCase):
    def setUp(self):
        super().setUp()

        # Create a couple of test events
        self.event1 = Event.objects.create(
            name="Test Event 1", description="This is a test event", user=self.user1
        )
        self.event2 = Event.objects.create(
            name="Test Event 2",
            description="This is another test event",
            user=self.user1,
        )
        self.event3 = Event.objects.create(
            name="Test Event 3", description="This is 3rd test event", user=self.user1
        )
        self.event4 = Event.objects.create(
            name="Test Event 4", description="This is created by 2nd", user=self.user2
        )
        self.event5 = Event.objects.create(
            name="Test Event 5",
            description="This is again created by 2nd",
            user=self.user2,
        )

    def test_delete_event(self):
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token1.key)

        response = self.client.delete(f"/api/events/{self.event1.id}")
        # Check that the event was deleted
        self.assertEqual(response.status_code, 204)
        self.assertEqual(4, Event.objects.all().count())

        # Check if a user cannot delete anothers event
        response = self.client.delete(f"/api/events/{self.event4.id}")
        self.assertEqual(response.status_code, 404)

    def test_update_event(self):
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token1.key)

        response = self.client.patch(
            f"/api/events/{self.event2.id}", data={"name": "New event name"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "New event name")
