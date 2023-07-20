# event-tracker: flexible event tracking API

![Image Description](img/logo.png)

## ABOUT:

Welcome to EventTrackr, a robust and scalable event tracking system that caters to the unique requirements of you and your platform. Our application allows you to create & manage custom events, and then track those events on your websites. Using our API will enable you to gain insightful data and analytics about user behaviors, leading to more informed decision making and strategic planning.

## Table of Contents

- [Architecture](#architecture)
- [Installation Instructions for your Device](#installation-instructions)

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

5. Set up the database (I am using postgresql). Add this to your `DATABASES` setting in settings.py:

6. Run the following command to apply migrations:

```sh
python3 manage.py migrate
```

7. Run the server

```sh
python manage.py runserver
```

Visit http://localhost:8000 in your web browser to see your application running.

