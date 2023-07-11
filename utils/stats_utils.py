from weather_app.models import WeatherRecords, WeatherStationStats
from django.db.models import Avg, Sum, F


class StatsUtils:
    """Helper utilities for stats calculation"""

    def __init__(self) -> None:
        pass

    @staticmethod
    def create_weather_stats(
        station_id: str, year: int, update_existing: bool = False
    ) -> None:
        """
        Takes Station_id and year and create stats for the same
        """
        year = int(year)
        records = WeatherRecords.objects.filter(date__year=year, station_id=station_id)

        # Values converted to degree celsius
        avg_max_temp = (
            records.values("max_temp")
            .exclude(max_temp=-9999)
            .aggregate(Avg(F("max_temp")))
            .get("max_temp__avg", 0)
        )
        # None value can be returned if all records are -9999(unavailable)
        avg_max_temp = 0 if avg_max_temp is None else avg_max_temp / 10
        avg_min_temp = (
            records.values("min_temp")
            .exclude(max_temp=-9999)
            .aggregate(Avg(F("min_temp")))
            .get("min_temp__avg", 0)
        )
        avg_min_temp = 0 if avg_min_temp is None else avg_min_temp / 10
        # Value converted to centimeter from millimeter
        total_ppt = (
            records.values("ppt_amount")
            .exclude(ppt_amount=-9999)
            .aggregate(Sum(F("ppt_amount")))
            .get("ppt_amount__sum", 0)
        )
        total_ppt = 0 if total_ppt is None else total_ppt / 100
        if update_existing is False:
            WeatherStationStats(
                station_id=station_id,
                year=year,
                max_temp_avg=avg_max_temp,
                min_temp_avg=avg_min_temp,
                total_ppt=total_ppt,
            ).save()
        else:
            stats = WeatherStationStats.objects.get(station_id=station_id, year=year)
            stats.max_temp_avg = avg_max_temp
            stats.min_temp_avg = avg_min_temp
            stats.total_ppt = total_ppt
            stats.save()
