from django.db.models.signals import post_save
from django.dispatch import receiver
from weather_app.models import WeatherRecords
from utils.stats_utils import StatsUtils


@receiver(post_save, sender=WeatherRecords)
def stats_populate(sender, instance, using, update_fields, **kwargs):
    date = instance.date
    station_id = instance.station_id
    update_existing = True if update_fields else False
    StatsUtils.create_weather_stats(
        station_id=station_id, year=date.year, update_existing=update_existing
    )
