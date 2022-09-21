from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class dbdata(models.Model):
    """
    SQL平台数据库管理模型
    """
    ENGINE_TYPE = [
        ("ibm_db_django", "DB2"),
        ("django.db.backends.oracle", "Oracle"),
        ("django.db.backends.mysql", "MySQL"),
        ("django.db.backends.postgresql", "PostgreSQL"),
        ("django.db.backends.sqlite3", "SQLite3"),
    ]
    # ID = models.CharField(max_length=100, default="", editable=False)
    DBID = models.CharField(max_length=100, help_text="可读名称", verbose_name="数据库标识")
    ENGINE = models.CharField(max_length=100, choices=ENGINE_TYPE, help_text="请选择", verbose_name="数据库类型")
    DBNAME = models.CharField(max_length=100, verbose_name="数据库名")
    USER = models.CharField(max_length=100, blank=True, verbose_name="用户名")
    PASSWORD = models.CharField(max_length=100, blank=True, verbose_name="密码")
    HOST = models.CharField(max_length=100, blank=True, verbose_name="连接地址")
    PORT = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(65535)], blank=True, verbose_name="连接端口")
    CREATE_AT = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    UPDATE_AT = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    def __str__(self):
      return self.DBID
    
    class Meta:
        verbose_name = '数据库列表'
        verbose_name_plural = '数据库列表'
