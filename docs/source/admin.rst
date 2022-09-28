管理工具
========

uWSGI
-----------

- 启动 uWSGI

.. code-block:: console

    systemctl start uwsgi

- 停止 uWSGI

.. code-block:: console

    systemctl stop uwsgi

- 重载 uWSGI

.. code-block:: console

    systemctl reload uwsgi

- 获取 uWSGI Master PID

.. code-block:: console

    cat /approot1/projectSQL/uwsgi/uwsgi_sql.pid

- 查看 uWSGI 日志

.. code-block:: console

    less /approot1/projectSQL/logs/uwsgi uwsgi_sql.log

- 配置日志滚动

使用 ``crontab`` 执行脚本，每日0点切割日志并归档，历史日志保存在 ``/approot1/projectSQL/logs/archived/``

.. code-block:: console

    cat << \EOF >> /var/spool/cron/root
    # uWSGI 日志滚动
    0 0 * * * bash /approot1/projectSQL/utils/uwsgi_logrotate.sh &>/dev/null
    EOF

- 查看 uWSGI 状态统计

默认未启用状态文件，如需要可以手动打开

定位到最后一行，去除注释并重载 ``uWSGI``

.. code-block:: console

    vi /approot1/projectSQL/uwsgi_sql.ini

    # status
    # stats           = /approot1/projectSQL/uwsgi/uwsgi_sql.stats

使用以下命令查看状态

.. code-block:: console

    uwsgi --connect-and-read /approot1/projectSQL/uwsgi/sql_platform.stats

Nginx
------

- 启动 Nginx
  
.. code-block:: console

    systemctl start nginx

- 停止 Nginx
  
.. code-block:: console

    systemctl stop nginx

- 重载 Nginx

.. code-block:: console

    systemctl reload nginx

- 查看 Nginx 日志
  
.. code-block:: console

    less /approot2/nginx/logs/error.log

- 配置日志滚动

.. code-block:: console

    cat << \EOF > /etc/logrotate.d/nginx
    /approot2/nginx/logs/*.log {
        daily
        rotate 30
        compress
        delaycompress
        dateext
        missingok
        notifempty
        create 0664 nginx nginx
        sharedscripts
        postrotate
            [ ! -f /approot2/nginx/nginx.pid ] || kill -USR1 `cat /approot2/nginx/nginx.pid`
        endscript
    }
    EOF

- 测试日志滚动配置
  
.. code-block:: console

    logrotate -d /etc/logrotate.d/nginx

Redis
------

- 启动 Redis
  
.. code-block:: console

    systemctl start redis

- 停止 Redis
  
.. code-block:: console

    systemctl stop redis

- 重启 Redis

.. code-block:: console

    systemctl restart redis

- 刷新缓存

.. code-block:: console

    redis-cli -n 1 flushdb

- 查看日志

.. code-block:: console

    less /approot3/redis/logs/redis_6379.log

- 配置日志滚动

.. code-block:: console

    cat << \EOF > /etc/logrotate.d/redis
    /approot3/redis/logs/*.log {
        daily
        rotate 30
        compress
        delaycompress
        dateext
        missingok
        notifempty
        create 0664 redis redis
    }
    EOF

- 测试日志滚动配置
  
.. code-block:: console

    logrotate -d /etc/logrotate.d/redis

Django
-------

部署和维护均不需要关注此部分，如果你需要在此基础上二次开发，以下内容可能有所帮助

- 收集静态文件

静态文件有变动时，需重新收集静态文件，请确保其他用户有读取权限

静态文件由 ``nginx`` 处理

.. code-block:: console

    echo yes|python3 manage.py collectstatic

- 编译消息文件

为了与项目所使用的开源组件代码风格保持一致，便于维护或合并更改，二次开发部分建议使用英语，部分字符串需要在消息文件中进行本地化，具体可参考 |docs.djangoproject.i18n|

.. |docs.djangoproject.i18n| raw:: html

   <a href="https://docs.djangoproject.com/zh-hans/4.1/topics/i18n" target="_blank">官方文档</a>

创建消息文件后，以及每次修改 ``.po`` 文件时，需要编译出 ``.mo`` 文件以供 ``gettext`` 使用

.. hint::

    说人话：
    不跑这一条翻译不生效

.. code-block:: console

    python3 manage.py compilemessages

- 显示现有迁移

不加参数默认显示所有应用，可指定 ``APP_NAME``

.. code-block:: console
    
    python3 manage.py showmigrations
    python3 manage.py showmigrations dbmng

- 撤销迁移

``python3 manage.py migrate [app_name] [migration_name]``

- 清理迁移文件

每当模型有改动时都需要执行 ``python3 manage.py makemigrations`` 生成迁移文件记录数据结构变化

开发过程中对模型不断更新，可能会留下一些反复改动导致的无意义迁移文件

虽然对小项目来说迁移文件的数量并没有什么影响，但你如果恰巧有点代码洁癖，以下操作可以对迁移文件进行合并

.. attention:: 

    谨慎操作

1. 初始化模型（仅标记）

.. code-block:: console

    python3 manage.py migrate --fake [app_name] zero

--fake            仅标记，不实际更改数据库，``zero`` 表示回溯所有的迁移

2. 删除 ``migrations`` 目录中不再需要的迁移文件

在项目根目录执行，删除 ``__init__.py`` 之外所有的迁移文件

.. code-block:: console

    find [app_name] -path "*/migrations/*.py" -not -name "__init__.py" -delete

3. 重新生成迁移文件

.. code-block:: console

    python3 manage.py makemigrations [app_name]

4. 执行迁移（仅标记）

.. code-block:: console

    python3 manage.py migrate --fake-initial [app_name]

管理后台
--------

- 后台基于 ``django-admin`` 和 ``SimpleUI`` 构建

数据库管理
^^^^^^^^^^

此页面可管理外部配置 ``projectSQL/conf/`` 中的数据库配置，不包含 ``settings.py`` 中的数据库，避免错误配置导致项目无法启动

功能包含：

- 新增/修改/删除数据库连接配置

  + 数据库支持列表

    + DB2
    + MySQL
    + Oracle
    + PostgreSQL
    + SQLite3

- 立即应用配置

- 按数据库名/连接地址搜索

- 按数据库类型筛选

功能说明
********

关于 ``应用到配置文件`` 按钮

受限于框架， ``应用到配置文件`` 至少需要勾选一个项目才允许使用，如果你打算清空外部数据库配置，将无法使用此按钮应用

并且，有些时候你可能并不需要立即重启服务端来应用配置更改

跳转到 ``功能脚本`` - sync_db.py_ 查看解决办法 

.. _sync_db.py: #utils-sync-db-py

.. important::

    热修改配置在 |docs.djangoproject.altering-settings-at-runtime| 中是明确不建议的操作
    
    应用配置需要重启服务端来生效，这意味着所有正在执行的 SQL 都将 **立即中断**

    SQL 平台的数据库连接基于 ``Django ORM`` 接口，且所有的数据库操作都使用了事务(``transaction``)来保证数据的安全性和一致性
    
    所以即使正在执行更改类 SQL 时被中断也是安全的

    影响仅限于正在等待 SQL 结果返回的用户会获得一个 ``502`` 错误

.. tip::

    但你也可以利用此按钮来立即中断意外进行的全表扫描

.. |docs.djangoproject.altering-settings-at-runtime| raw:: html

   <a href="https://docs.djangoproject.com/en/dev/topics/settings/#altering-settings-at-runtime" target="_blank">官方文档</a>

查询日志管理
^^^^^^^^^^^^

此页面可管理查看 SQL 平台产生的历史查询日志，用于审计

功能包含：

- 删除/搜索/筛选历史查询日志

  + 按 SQL 语句内容搜索
  + 按执行人筛选
  + 按数据库筛选
  + 时间段范围筛选

.. note::

    虽然有个 ``增加`` 按钮，但不要在此页面手动增加查询日志

查询语句管理
^^^^^^^^^^^^

此页面可管理 SQL 平台 - 新增查询 页面创建的 SQL 语句

功能包含：

- 新增/修改/删除保存的语句

- 直接在此页面执行并导出所选语句的结果为 CSV

- 按 SQL 语句内容搜索

- 按创建者/数据库筛选

用户管理
^^^^^^^^

- 后台用户及权限管理完全由 ``django-admin`` 框架实现，你可以使用正常的搜索引擎找到大量优秀文档


功能脚本
^^^^^^^^

``utils/sync_db.py``
*********************

此脚本可以在项目外部单独执行，以 SQL 平台数据库为目标单向同步本地配置

以下为使用管理后台删除了列表中最后一个配置 ``TEST_DB`` ，但无法使用 ``应用到配置文件`` 时的场景

执行脚本后将移除本地配置中的 ``TEST_DB``

.. code-block:: console

    [root@localhost utils]# python3 sync_db.py
    2022-08-31 16:21:47,333 - [INFO] - DB remote: []
    2022-08-31 16:21:47,333 - [INFO] - DB local before add: ['TEST_DB']
    2022-08-31 16:21:47,333 - [INFO] - Diff DB +: []
    2022-08-31 16:21:47,333 - [INFO] - DB local after add: ['TEST_DB']
    2022-08-31 16:21:47,333 - [INFO] - Phase 1 synchronization is completed
    2022-08-31 16:21:47,333 - [INFO] - DB remote: []
    2022-08-31 16:21:47,333 - [INFO] - DB local before remove: ['TEST_DB']
    2022-08-31 16:21:47,333 - [INFO] - Diff DB -: ['TEST_DB']
    2022-08-31 16:21:47,333 - [INFO] - Removing DB from local: TEST_DB
    2022-08-31 16:21:47,333 - [INFO] - DB local after remove: []
    2022-08-31 16:21:47,333 - [INFO] - Phase 2 synchronization is completed
    2022-08-31 16:21:47,340 - [INFO] - Backing up env.py to /approot1/projectSQL/conf/archived
    2022-08-31 16:21:47,341 - [INFO] - Writing DB connection string to env.py
    2022-08-31 16:21:47,348 - [INFO] - Backing up explorer.py to /approot1/projectSQL/conf/archived
    2022-08-31 16:21:47,349 - [INFO] - Writing EXPLORER_CONNECTIONS_EXTRA to explorer.py
    2022-08-31 16:21:47,349 - [INFO] - Phase 3 write to env.py and explorer.py is completed
    2022-08-31 16:21:47,358 - [INFO] - Reloading uWSGI
    2022-08-31 16:21:47,396 - [INFO] - Flushing Redis
    2022-08-31 16:21:47,397 - [INFO] - All done.

- 配置自动同步

使用 ``crontab`` 执行脚本，闲时自动同步数据库配置，历史日志保存在 ``/approot1/projectSQL/logs/``

.. code-block:: console

    cat << \EOF >> /var/spool/cron/root
    # SQL 平台 数据库配置同步
    0 1 * * * /usr/bin/env python3 /approot1/projectSQL/utils/sync_db.py &>/dev/null
    EOF

``utils/create_user.py``
*************************

此脚本可以在项目外部单独执行，用于快速创建用户

可以与其他脚本配合使用，批量创建用户

Usage: create_user.py -u <username> -p <password>

-u                      用户名
-p                      密码，可不填，将使用脚本中定义的默认密码

.. code-block:: console

    [root@localhost utils]# python3 create_user.py -u query -p password
    2022-08-31 17:20:12,080 - [INFO] - User query created
    [root@localhost utils]# python3 create_user.py -u DBA
    2022-08-31 17:20:18,648 - [INFO] - User DBA created

``utils/truncate_querylogs.py``
********************************

此脚本可以在项目外部单独执行，用于清理 SQL 平台的历史查询日志

Usage: python3 truncate_querylogs.py -d <days>

-d                      天数，大于此数的历史日志将被清理

.. code-block:: console

    [root@localhost utils]# python3 truncate_querylogs.py -d 30
    2022-08-31 17:28:52,369 - [INFO] - Starting...
    2022-08-31 17:28:52,376 - [INFO] - No QueryLog older than 30 days.
    2022-08-31 17:28:52,378 - [INFO] - Done.
    [root@localhost utils]# python3 truncate_querylogs.py -d 7
    2022-08-31 17:28:58,309 - [INFO] - Starting...
    2022-08-31 17:28:58,316 - [INFO] - Deleting 33 QueryLogs older than 7 days.
    2022-08-31 17:28:58,330 - [INFO] - Done.

- 配置自动清理

使用 ``crontab`` 执行脚本，闲时自动清理历史查询日志，历史日志保存在 ``/approot1/projectSQL/logs/``

.. code-block:: console

    cat << \EOF >> /var/spool/cron/root
    # SQL 平台 查询日志清理
    0 2 * * * /usr/bin/env python3 /approot1/projectSQL/utils/truncate_querylogs.py -d90 &>/dev/null
    EOF