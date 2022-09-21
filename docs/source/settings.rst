配置选项
========

SQL 平台
---------

``sql_platform/settings.py``

默认连接
^^^^^^^^^^^^

- EXPLORER_DEFAULT_CONNECTION

连接列表中默认选择的库

连接列表
^^^^^^^^

- EXPLORER_CONNECTIONS

选择连接数据库时的列表， ``dict`` 格式

``Key`` 为别名 (alias) ， 显示在 SQL 平台的连接选择列表

``value`` 为 ``DATABASES`` 中配置的数据库名，也就是 ``DATABASES`` 的 ``key``

.. code-block:: console

    EXPLORER_CONNECTIONS = {
        "Django": "default"
    }

用户白名单
^^^^^^^^^^

- EXPLORER_USER_WHITELIST

.. danger::

    用户白名单，有权限执行修改类 SQL（无视 SQL 黑名单），谨慎添加， ``tuple`` 格式

.. warning::

    superuser 同样可以无视 SQL 黑名单



.. code-block:: console

    EXPLORER_USER_WHITELIST = ("DBA","BOSS")
    
SQL 黑名单
^^^^^^^^^^^

- EXPLORER_SQL_BLACKLIST

禁止在 SQL 平台执行的 SQL 类型，默认配置了所有修改类 SQL， ``tuple`` 格式

建议首先为每个数据库配置只读用户，当无法修改数据库时，这个配置可以提供最后的权限保护

.. code-block:: console

    EXPLORER_SQL_BLACKLIST = (
        "ALTER",
        "RENAME ",
        "DROP",
        "TRUNCATE",
        "INSERT INTO",
        "UPDATE",
        "REPLACE",
        "DELETE",
        "CREATE TABLE",
        "GRANT",
        "OWNER TO",
        "SET",
    )

表结构排除前缀
^^^^^^^^^^^^^^^^^^^^^^^

- EXPLORER_SCHEMA_EXCLUDE_TABLE_PREFIXES

在表结构显示中隐藏的表前缀，仅隐藏，避免干扰，实际仍可操作， ``tuple`` 格式

.. code-block:: console

    EXPLORER_SCHEMA_EXCLUDE_TABLE_PREFIXES = (
        "auth_",
        "contenttypes_",
        "sessions_",
        "admin_",
    )

其他配置
^^^^^^^^

- 请参考 ``settings.py`` 中的注释

Nginx
------

``/approot2/nginx/conf/conf.d/sql.conf``

uWSGI 超时
^^^^^^^^^^

- uwsgi_read_timeout

- uwsgi_send_timeout

.. code-block:: console

    uwsgi_read_timeout 600;
    uwsgi_send_timeout 600;

连接数限制

- limit_conn perserver

视情况修改，当前并发连接总数超过指定数量，会返回 ``503`` 错误

.. code-block:: console

    limit_conn perserver 10;