from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from explorer.actions import generate_report_action
from explorer.models import Query, QueryLog


class QueryAdmin(admin.ModelAdmin):
    # list_per_page = 20
    # list_max_show_all = 200
    list_display = ('title', 'connection', 'sql', 'created_by_user', 'created_at', 'last_run_date')
    list_filter = ('created_by_user', 'connection',)
    search_fields = ('sql',)
    raw_id_fields = ('created_by_user',)
    actions = [generate_report_action()]

class QueryLogAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('run_at', 'run_by_user', 'connection', 'sql', 'query', 'duration',)
    list_filter = ('run_by_user', 'connection', ('run_at', DateFieldListFilter))
    search_fields = ('sql',)


admin.site.register(Query, QueryAdmin)
admin.site.register(QueryLog, QueryLogAdmin)
