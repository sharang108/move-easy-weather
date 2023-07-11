from django.db import models


class WeatherRecords(models.Model):
    """
    Weather Records Database to be populated with the flat text files
    Note: station_id is assumed to be the name of the file
    """

    station_id = models.CharField(max_length=255)
    date = models.DateField()
    max_temp = models.IntegerField()
    min_temp = models.IntegerField()
    ppt_amount = models.IntegerField()

    class Meta:
        """
        Meta for weather records,
        Making station_id, date unique in order to identify unnique record for a given date/station
        """

        unique_together = ["station_id", "date"]


class WeatherStationStats(models.Model):
    """
    Stats for weather stations by station per year
    """

    station_id = models.CharField(max_length=255)
    year = models.IntegerField()
    max_temp_avg = models.FloatField()
    min_temp_avg = models.FloatField()
    total_ppt = models.IntegerField()

    class Meta:
        """
        Meta for weather records stats,
        Making station_id, date unique in order to identify unnique record for a given date/station
        """

        unique_together = ["station_id", "year"]
