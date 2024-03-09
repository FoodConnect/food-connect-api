from django.apps import AppConfig


class FoodConnectAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'food_connect_app'

    def ready(self):
        import food_connect_app.signals