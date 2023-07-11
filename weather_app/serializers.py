from rest_framework import serializers
from weather_app.models import WeatherRecords, WeatherStationStats


class WeatherRecordSerializer(serializers.ModelSerializer):
    """Weather Records Serialization"""

    class Meta:
        model = WeatherRecords
        exclude = ["id"]


class WeatherStatsSerializer(serializers.ModelSerializer):
    """Weather Records Statistics Serialization"""

    class Meta:
        model = WeatherStationStats
        exclude = ["id"]
