# from django.apps import AppConfig


# class ClsbookConfig(AppConfig):
#     name = "clsbook"


from django.apps import AppConfig

class ClsbookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clsbook'

    def ready(self):
        from allauth.account import app_settings
        from allauth.account.adapter import get_adapter
        from .forms import TeacherSignupForm

        # Replace default signup form
        app_settings.FORMS['signup'] = TeacherSignupForm

        