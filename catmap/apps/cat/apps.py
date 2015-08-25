# myapp/apps.py
from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .handlers import add_log_for_cat


class CatConfig(AppConfig):
    name = 'catmap.apps.cat'

    def ready(self):
        pre_save.connect(add_log_for_cat, sender='eventlog.Log', dispatch_uid='eventlog.Log.add_log_for_cat')
