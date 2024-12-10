from django.apps import AppConfig


class AppNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'student_adms'  # Replace with your app's name

    def ready(self):
        import student_adms.signals  
