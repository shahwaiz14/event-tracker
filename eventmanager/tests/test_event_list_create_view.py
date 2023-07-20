from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK

from .BaseTest import BaseTestCase
from ..models import Event

class EventListCreateTestClass(BaseTestCase):
    def setUp(self):
        super().setUp()

        # Create a couple of test events
        Event.objects.create(name='Test Event 1', description='This is a test event', user=self.user1)
        Event.objects.create(name='Test Event 2', description='This is another test event', user=self.user1)
        Event.objects.create(name='Test Event 3', description='This is 3rd test event', user=self.user1)
        Event.objects.create(name='Test Event 4', description='This is created by 2nd', user=self.user2)
        Event.objects.create(name='Test Event 5', description='This is again created by 2nd', user=self.user2)


    def test_get_event_list(self):
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)

        # Send a GET request to the EventList view
        response = self.client.get('/api/events/')

        # Check that the response has status code 200
        self.assertEqual(response.status_code, 200)

        # Check that the response data contains our events' names
        self.assertIn('Test Event 1', response.data)
        self.assertIn('Test Event 2', response.data)

        # Ensure the response data is a list
        self.assertIsInstance(response.data, list, "Response data should be a list.")

        # Ensure we don't get user 2's events
        expected_data = ['Test Event 3', 'Test Event 2', 'Test Event 1']
        self.assertEqual(expected_data, response.data, "Response data did not match expected data.")
       

    def test_unauthorized_event_list(self):
        # Send a GET request without a token
        response = self.client.get('/api/events/')

        # Check that the response has status code 401 (unauthorized)
        self.assertEqual(response.status_code, 401)

    def test_post_events(self):
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)

        # Send a post request to the EventList view
        response = self.client.post('/api/events/', {"name":"click","description":"clicked"}, format='json')
        # Check to see if created correctly
        self.assertIn('click', response.data["name"])
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Send a faulty post request to the EventList view
        response = self.client.post('/api/events/', {"one":"click","two":"clicked"}, format='json')
        # Check to see if it gives the correct error 
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_search_event(self):
        """
        Ensure we can search an event by name.
        """
        #Authenticate
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)

        # Create an event for the test
        Event.objects.create(name='Test Event', description='This is a test event.', user=self.user1)

        # Use the search feature
        response = self.client.get('/api/events/', {'search': 'Test Event'}, format='json') 

        # Check that the response status code is 200
        self.assertEqual(response.status_code, HTTP_200_OK)
    
        # Check that the returned data contains the event's name
        self.assertEqual(response.data[0], 'Test Event')
        