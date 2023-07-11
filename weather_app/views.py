from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from weather_app.models import WeatherRecords, WeatherStationStats

from .serializers import WeatherRecordSerializer, WeatherStatsSerializer


# Create your views here.
class WeatherDataViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """

    queryset = WeatherRecords.objects.all()
    serializer_class = WeatherRecordSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "station_id",
                openapi.IN_QUERY,
                description="Station ID",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "date",
                openapi.IN_QUERY,
                description="Date in yyyymmdd format",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        station_id = request.query_params.get("station_id", "")
        date = request.query_params.get("date", "")
        date = datetime.strptime(date, "%Y%m%d") if date else ""

        if date and not station_id:
            self.queryset = WeatherRecords.objects.filter(date=date)
        elif station_id and not date:
            self.queryset = WeatherRecords.objects.filter(station_id=station_id)
        elif station_id and date:
            self.queryset = WeatherRecords.objects.filter(
                station_id=station_id, date=date
            )
        page = self.paginate_queryset(self.queryset)
        searializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(searializer.data)


# Create your views here.
class WeatherStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """

    queryset = WeatherStationStats.objects.all()
    serializer_class = WeatherStatsSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "station_id",
                openapi.IN_QUERY,
                description="Station ID",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "year",
                openapi.IN_QUERY,
                description="Year in yyyy format",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        station_id = request.query_params.get("station_id", "")
        year = int(request.query_params.get("year", 0))
        if year and not station_id:
            self.queryset = WeatherStationStats.objects.filter(year__contains=year)
        elif station_id and not year:
            self.queryset = WeatherStationStats.objects.filter(station_id=station_id)
        elif station_id and year:
            self.queryset = WeatherStationStats.objects.filter(
                station_id=station_id, year__contains=year
            )
        page = self.paginate_queryset(self.queryset)
        searializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(searializer.data)
