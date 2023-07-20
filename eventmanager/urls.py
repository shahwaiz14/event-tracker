from django.urls import path
from . import views

urlpatterns = [
    path("events/", views.EventList.as_view()),
    path("events/<int:pk>", views.EventUpdateDelete.as_view()),
    path("eventlogs/", views.EventLogData.as_view()),
    path("stats/event_frequency", views.EventFrequency.as_view()),
    path("stats/event_trend", views.EventTrendsView.as_view()),
]