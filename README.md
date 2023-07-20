# event-tracker: flexible event tracking API

![Image Description](img/logo.png)

## ABOUT:

Welcome to EventTrackr, a robust and scalable event tracking system that caters to the unique requirements of you and your platform. Our application allows you to create & manage custom events, and then track those events on your websites. Using our API will enable you to gain insightful data and analytics about user behaviors, leading to more informed decision making and strategic planning.

## Table of Contents

- [ARCHITECTURE](#architecture)
- [INSTALLATION INSTRUCTIONS](#installation-instructions)
- [THIS SOLUTION SHOULD PROVIDE](#this-solution-should-provide)

## ARCHITECTURE


## INSTALLATION INSTRUCTIONS

**Prerequisites**

Ensure that you have the following installed:
- Python3
- pip
- virtualenv

**Step-by-step Guide**

1. Clone the repository:

```sh
git clone https://github.com/shahwaiz14/event-tracker.git
```

Navigate into the project directory:

```sh
cd event-tracker
```

2. Create a virtual environment:

```sh
python3 -m venv env
```

Activate the virtual environment (for MacBook):

```sh
source env/bin/activate
```

3. Install the required packages

```sh
pip install -r requirements.txt
```

4. Create a database from your terminal. Make sure you have postgres installed on your machine.

```sh
createdb -h localhost -p 5432 -U shahwaiz EventManager
```

5. Set up the database (I am using postgresql). Add this to your `DATABASES` setting in settings.py. Make sure to add the `USER` property.

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "EventManager",
        "USER": {USER},
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "",
    }
}
```

6. Run the following command to apply migrations:

```sh
python3 manage.py migrate
```

7. Run the server

```sh
python3 manage.py runserver
```

Visit http://localhost:8000 in your web browser to see your application running.

### Creating a new user and login ###
You will not be able to make any request until you create a new user and login. You can do this through Django Rest Framework's browsable API or through command line.

8. Register a new user
```sh
curl -X POST http://127.0.0.1:8088/auth/users/ --data 'username=djoser&password=alpine12'
```

9. Log in
```sh
curl -X POST http://127.0.0.1:8088/auth/token/login/ --data 'username=djoser&password=alpine12'
```

This will return a auth token, like this `{"auth_token": "b704c9fc3655635646356ac2950269f352ea1139"`. Store this token, as you will need it to communicate with EventTracker API.

10. Check if your token is working

```sh
curl -LX GET http://127.0.0.1:8088/auth/users/me/ -H 'Authorization: Token b704c9fc3655635646356ac2950269f352ea1139'
```

This will return something like this: `{"email": "", "username": "djoser", "id": 1}`


## THIS SOLUTION SHOULD PROVIDE:

_Django Rest Framework's Browsable API is more intuitive to interact and test this API. However, if you want to use Python or terminal, here is the code to interact with the Event-Tracker API:_

(Please ensure that you replace the port number in the URL with the appropriate port that your application is running on your local machine. Additionally, don't forget to add your authentication token in the Authorization header for all requests)

1. Users should be able to get a list of events they have created

Terminal:
```sh
curl http://127.0.0.1:8081/api/events/ -H 'Authorization: Token {your_token}'
```

Python:
```python
import requests

url = "http://127.0.0.1:8081/api/events/"
headers = {"Authorization": f"Token {token}"}

response = requests.get(url, headers=headers)

print(response.text)
```


2. Users should be able to create events. If you try to create a duplicate event, you will get an error.

Terminal:
```sh
curl -X POST http://127.0.0.1:8081/api/events/ \
-H "Authorization: Token {token}" \
-H "Content-Type: application/json" \
-d '{"name":"test","description":"testing event creation"}'

```

Python:
```python
import requests
token = 'your_token'
url = "http://127.0.0.1:8081/api/events/"
headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}
data = {
    "name": "test",
    "description": "testing event creation"
}

response = requests.post(url, headers=headers, json=data)
```


3. Users can search the events they created via the title and description

Terminal
```sh
curl 'http://127.0.0.1:8081/api/events/?search=test' -H "Authorization: Token {token}"
```

Python:
```python
import requests

url = "http://127.0.0.1:8081/api/events/"
headers = {"Authorization": f"Token {token}"}
params = {"search": "test"}

response = requests.get(url, headers=headers, params=params)

print(response.json()) 
```


4. The user can update an event if needed

Terminal:
```sh
curl -X PATCH http://127.0.0.1:8081/api/events/1 -H "Authorization: Token {token}" -H "Content-Type: application/json" --data '{"description":"modified description"}'
```

Python:
```python
import requests
import json

url = 'http://127.0.0.1:8081/api/events/1'
headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json'}
data = {'description': 'modified description'}

response = requests.patch(url, headers=headers, data=json.dumps(data))
```


5. The user can remove an event if needed by passing in event_id as a path parameter

Terminal:
```sh
curl -X DELETE http://127.0.0.1:8081/api/events/1 -H "Authorization: Token {token}"
```

Python:
```python
import requests

url = 'http://127.0.0.1:8081/api/events/1'
headers = {'Authorization': f'Token {token}'}

requests.delete(url, headers=headers)

```


7. Users can use this endpoint to implement in their frontend (or their platform) so that we can log event’s data on their customers events

Terminal:
```sh
curl -X POST http://127.0.0.1:8081/api/eventlogs/ \
-H "Authorization: Token {token}" \
-H "Content-Type: application/json" \
-d '{"event_name":"purchased","data":"{"amount":50, product_id=2}"}'
```

Python:
```python
import requests

url = 'http://127.0.0.1:8081/api/eventlogs/'
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}
data = {
    'event_name': 'purchased',
    'data': '{"amount": 50, "product_id": 2}'
}

response = requests.post(url, headers=headers, json=data)
```


8. The user can view events trend data for their website

Terminal:
```sh
curl http://127.0.0.1:8081/api/stats/event_trend -H "Authorization: Token {token}"
```

Python:
```python
import requests

url = 'http://127.0.0.1:8081/api/stats/event_trend'
headers = {'Authorization': f'Token {token}'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("Event trend:", data)
```


9. User can views events data, specifically the frequency at which events occur by optionally providing the event_name, start_date, end_date. 

Terminal
```sh
curl 'http://127.0.0.1:8081/api/stats/event_frequency?event_name=click&start_date=2021-01-01&end_date=2024-01-01' -H "Authorization: Token {token}"

```

Python
```python
import requests

url = 'http://127.0.0.1:8081/api/stats/event_frequency'
headers = {
    'Authorization': f'Token {token}'
}
# passing params is optional
params = {
    'event_name': 'click',
    'start_date': '2021-01-01',
    'end_date': '2024-01-01'
}

response = requests.get(url, headers=headers, params=params)
print(response.text)
```
