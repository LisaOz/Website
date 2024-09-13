from django.apps import AppConfig


class ImagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'images'

    """
    This function imports the signals for the application so that they are imported when the images applicaion is loaded
    """
    def ready(self):
        import images.signals # import signal handlers
