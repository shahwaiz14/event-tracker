from rest_framework import serializers

from .models import Event, EventLog

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["name", "description"]


class EventDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLog
        fields = ["event_name", "data"]

