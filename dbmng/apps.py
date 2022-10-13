from django.apps import AppConfig


class DbmngConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dbmng'

    verbose_name = '数据库管理'
