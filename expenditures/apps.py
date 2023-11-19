import os
from django.apps import AppConfig
from config import settings


class ExpendituresConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "expenditures"

    def ready(self): #앱 초기화 및 설정
        if os.environ.get('RUN_MAIN', None) is not None:
            if settings.SCHEDULER_DEFAULT:
                print("schedul once!!")
            
