from django.apps import AppConfig


class WeatherAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "weather_app"

    def ready(self) -> None:
        import weather_app.signals

        return None
