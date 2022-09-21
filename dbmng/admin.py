import os

from django.contrib import admin, messages
from django.conf import settings

from .models import dbdata

BASE_DIR = settings.BASE_DIR
CONF_DIR = f"{BASE_DIR}/conf"
ENV_CONF = "env.py"
EXPLORER_CONF = "explorer.py"
ARCHIVED = f"{BASE_DIR}/conf/archived"
UWSGI_PID = f"{BASE_DIR}/uwsgi/uwsgi_sql.pid"


class dbdataAdmin(admin.ModelAdmin):
    # 搜索框
    search_fields = ("DBNAME", "HOST")
    # 显示的字段
    list_display = (
        "DBID",
        "ENGINE",
        "DBNAME",
        "USER",
        "HOST",
        "PORT",
        "CREATE_AT",
        "UPDATE_AT",
    )
    # 筛选框
    list_filter = ["ENGINE"]
    # 每页显示的数据条数
    list_per_page = 20
    list_max_show_all = 200
    # 自定义按钮
    actions = ["apply_to_settings"]

    def apply_to_settings(self, request, queryset):
        # queryset.values 是一个 QuerySet 对象，包含了所选择的数据
        dbdata = queryset.values(
            "DBID", "ENGINE", "DBNAME", "USER", "PASSWORD", "HOST", "PORT"
        )
        # 将 queryset 转换为列表
        dbdata_to_list = list(dbdata)
        # 将列表转换为 Django settings 格式的嵌套字典
        DATABASES_EXTRA = {
            db["DBID"]: {
                "ENGINE": db["ENGINE"],
                "NAME": db["DBNAME"],
                "USER": db["USER"],
                "PASSWORD": db["PASSWORD"],
                "HOST": db["HOST"],
                "PORT": db["PORT"],
            }
            for db in dbdata_to_list
        }
        # 备份外部 Django DATABASES 配置文件
        os.system(
            f"cp {CONF_DIR}/{ENV_CONF} {ARCHIVED}/{ENV_CONF}.$(date '+%Y%m%d_%H%M%S')"
        )
        # 将字典写入 ENV_CONF 文件
        with open(f"{CONF_DIR}/{ENV_CONF}", "w") as f:
            f.write(f"DATABASES_EXTRA = {DATABASES_EXTRA}")
        # 备份 explorer 连接列表文件
        os.system(
            f"cp {CONF_DIR}/{EXPLORER_CONF} {ARCHIVED}/{EXPLORER_CONF}.$(date '+%Y%m%d_%H%M%S')"
        )
        # 将 DBID 的 value 添加到 explorer 连接列表
        EXPLORER_CONNECTIONS_EXTRA = {db["DBID"]: db["DBID"] for db in dbdata_to_list}
        # 将连接列表写入 EXPLORER_CONF 文件
        with open(f"{CONF_DIR}/{EXPLORER_CONF}", "w") as f:
            f.write(f"EXPLORER_CONNECTIONS_EXTRA = {EXPLORER_CONNECTIONS_EXTRA}")

        messages.add_message(request, messages.SUCCESS, "操作成功")
        # reload django settings
        os.system(f"uwsgi --reload {UWSGI_PID}")
        # flush redis
        os.system("redis-cli flushall")


    # 按钮配置
    apply_to_settings.confirm = "确定要应用到配置文件吗？这将立即重启服务端"
    apply_to_settings.short_description = "应用到配置文件"
    apply_to_settings.type = "warning"
    apply_to_settings.icon = "el-icon-setting"


# 管理页面的配置
admin.site.site_header = "SQL平台管理"
admin.site.site_title = "SQL平台管理"
admin.site.index_title = "SQL平台管理"

# 注册模型
admin.site.register(dbdata, dbdataAdmin)
