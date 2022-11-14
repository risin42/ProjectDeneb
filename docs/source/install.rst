安装部署
========

一键脚本
---------

在项目根目录，执行 ``./install.sh`` 即可自动安装部署

在最小化安装的 CentOS 7 / RHEL 7 上测试通过，无需公网

.. important ::

    一键部署完成后，你需要更改一些配置文件，以适应你的实际环境

    见 配置文件_

.. _配置文件: #id7

准备编译环境
------------

.. note::

    以下手动安装步骤根据最小化安装 ``CentOS-7-x86_64-DVD-2009.iso`` 环境编写，如果确定你的环境没有问题可以跳过相应章节

项目已提供所需环境包，可以跳至上传步骤，如果需要重新打包请参考

- 下载机需安装前置软件包，否则 ``yumdownloader`` 无法解析到相关依赖

.. code-block:: console

    yum install -y epel-release yum-utils centos-release-scl

- 离线下载编译工具包及依赖

.. code-block:: console

    yumdownloader -x '*i686' --resolve --destdir=/opt/devtools/ \
    ake \
    bzip2-devel \
    centos-release-scl \
    centos-release-scl-rh \
    devtoolset-8 \
    gdbm-devel \
    glibc \
    libffi-devel \
    ncurses-devel \
    nspr \
    nss \
    openssl11 \
    openssl11-devel \
    pcre-devel \
    perl-core \
    readline-devel \
    sqlite-devel \
    tk-devel \
    uuid-devel \
    xz-devel \
    zlib-devel

- 打包

.. code-block:: console

    cd /opt; tar -zcf devtools.tgz /opt/devtools

- 下载 OpenSSL

.. code-block:: console

    wget https://www.openssl.org/source/openssl-1.1.1q.tar.gz

- 下载 Python3.10

.. code-block:: console

    wget https://www.python.org/ftp/python/3.10.5/Python-3.10.5.tgz

- 上传至服务器
  
上传 ``devtools.tgz``, ``openssl-1.1.1q.tar.gz``, ``Python-3.10.5.tgz`` 至服务器 ``/opt`` 目录

安装编译工具包
--------------

- 解压

.. code-block:: console

    cd /opt
    tar -zxf devtools.tgz && cd devtools; ls -lrth
    
- 使用 ``yum`` 离线安装

.. code-block:: console

    yum install -y --cacheonly --disablerepo=* *.rpm

.. note::

   确定所有依赖包都存在的情况下，也可以考虑使用 ``rpm -Uvh ./*.rpm --nodeps --force`` 强制安装

安装 OpenSSL
------------

- 启用 GCC 8

.. code-block:: console

    source scl_source enable devtoolset-8

可选 - 设置默认启用 GCC 8

 ``echo 'source scl_source enable devtoolset-8' >> ~/.bashrc && source ~/.bash_profile``

- 解压

.. code-block:: console
    
    cd /opt
    tar -zxf openssl-1.1.1q.tar.gz && cd openssl-1.1.1q; ls -lrth

- 编译安装

.. code-block:: console

    ./config --prefix=/usr --openssldir=/etc/ssl --libdir=lib zlib-dynamic
    make -j$(nproc) && make install

-j            使用并发， ``$(nproc)`` 表示 CPU 核心数

- 验证安装

.. code-block:: console

    find /usr -name "libcrypto.so.1.1*"
    find /usr -name "openssl" -type f
    whereis openssl
    openssl version

- 配置环境变量

.. code-block:: console

    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib:/usr/local/lib64

安装 Python3
------------

- 启用 GCC 8

.. code-block:: console

    source scl_source enable devtoolset-8

可选 - 设置默认启用 GCC 8

 ``echo 'source scl_source enable devtoolset-8' >> ~/.bashrc && source ~/.bash_profile``

- 解压

.. code-block:: console

    cd /opt
    tar -zxf Python-3.10.5.tgz && cd Python-3.10.5; ls -lrth

- 编译安装
  
.. code-block:: console

    ./configure --enable-optimizations --with-lto
    make -j$(nproc) && make install

.. caution:: 

    如果已有低版本 Python3，使用 ``make altinstall`` 安装

--enable-optimizations                      性能选项，启用以配置文件主导的优化（PGO），会增加编译时间带来永久性能提升
--with-lto                                  性能选项，启用链接时间优化（LTO），会增加编译时间带来永久性能提升
--enable-loadable-sqlite-extensions         可选，如果需要新版本 SQLite3，先编译安装 SQLite3 再重新编译 Python3
-j                                          使用并发， ``$(nproc)`` 表示 CPU 核心数

- 验证安装

.. code-block:: console

    whereis python3
    python3 --version
    pip3 --version
    python3 -c 'import ssl;print(ssl.OPENSSL_VERSION)'

如果使用 ``make altinstall`` 安装，手动创建软链接

.. code-block:: console

    mv /usr/bin/python3 /usr/bin/python3.bak
    mv /usr/bin/pip3 /usr/bin/pip3.bak
    ln -sf /usr/local/bin/python3.10 /usr/bin/python3
    ln -sf /usr/local/bin/pip3.10  /usr/bin/pip3

安装数据库驱动
--------------

- 上传驱动包
  
上传 ``instantclient-basic-linux.x64-21.7.0.0.0dbru.tgz``, ``linuxx64_odbc_cli.tar.gz`` 至服务器 ``/opt`` 目录

- 解压

.. code-block:: console
    
    cd /opt
    tar -zxf instantclient-basic-linux.x64-21.7.0.0.0dbru.tgz
    tar -zxf linuxx64_odbc_cli.tar.gz

- 配置环境变量 - IBM 驱动
  
写入 ``/etc/profile``

.. code-block:: console

    cat << \EOF >> /etc/profile
    # IBM 驱动
    export IBM_DB_HOME=/opt/clidriver
    export LD_LIBRARY_PATH=$IBM_DB_HOME/lib:/usr/local/lib:/usr/local/lib64:/usr/lib:/usr/lib64
    EOF
    source /etc/profile

.. important:: 

    安装 ``ibm-db-django`` 前必须先配置好 IBM 驱动环境变量，否则依赖包 ``ibm-db`` 安装时将会尝试下载驱动并卡住

    python3 -m pip install --user --verbose ibm-db-django

    ...

    Running command Getting requirements to build wheel

    Detected 64-bit Python

    Detected platform = linux, uname = x86_64

    Downloading https://public.dhe.ibm.com/ibmdl/export/pub/software/data/db2/drivers/odbc_cli/linuxx64_odbc_cli.tar.gz

- 配置环境变量 - Oracle 驱动

.. code-block:: console

    sh -c "echo /opt/instantclient_21_7 > /etc/ld.so.conf.d/oracle-instantclient.conf"
    ldconfig

- 其他

其他数据库无需外部驱动支持。

.. note:: 

    可选，关于 MySQL 驱动
  
    Python 的 ``mysqlclient`` 是 C 实现，高性能，但不兼容 ``caching_sha2_password``，需要更改验证方式为 ``mysql_native_password``，且依赖 ``mysql-devel``

    本项目默认使用纯 Python 实现的 ``pymysql``，会比 ``mysqlclient`` 稍慢，但是原生支持 ``caching_sha2_password``

安装 Python 软件包
-------------------

- 创建虚拟环境

此目录将作为项目主目录

.. code-block:: console

    mkdir /approot1
    cd /approot1
    python3 -m venv venv

- 激活虚拟环境

.. code-block:: console

    source /approot1/venv/bin/activate

.. tip:: 

    激活虚拟环境后，在任何位置都可以使用 ``deactivate`` 关闭虚拟环境

- 上传软件包

上传 ``pypi.tgz`` 至服务器 ``/opt`` 目录

- 解压

.. code-block:: console

    cd /opt
    tar -zxf pypi.tgz && cd pypi; ls -lrth

- 使用 ``pip`` 离线安装

请确保当前在虚拟环境下，终端前有 ``(venv)`` 标记

.. code-block:: console

    python3 -m pip install --no-index --find-links=/opt/pypi -r requirements.txt

.. note:: 

    ``ibm-db`` 安装报错：

        ERROR: Could not find a version that satisfies the requirement setuptools (from versions: none)

        ERROR: No matching distribution found for setuptools

    ``ibm-db`` 安装时将从 ``tar.gz`` 执行构建 ``whl``

    此时依赖 ``setuptools`` 版本需 >=65， ``wheel`` 版本需 >=0.37

    请检查当前目录内是否有以上组件


.. note:: 

    ``uWSGI`` 安装报错：

        ssl.c:(.text+0xe26): undefined reference to 'SSL_set_options'

        collect2: error: ld returned 1 exit status

    移除低版本 ``openssl-devel`` 即可

    ``yum remove openssl-devel``

安装 Nginx
-----------

- 创建 nginx 用户/组

.. code-block:: console

    groupadd -g 1110 nginx
    useradd -u 1110 -g 1110 -r -s /sbin/nologin nginx

- 上传软件包及配置

上传 ``nginx-1.22.0.tar.gz`` , ``nginx-conf.tgz`` 至服务器 ``/opt`` 目录

- 解压

.. code-block:: console

    cd /opt
    tar -zxf nginx-1.22.0.tar.gz && cd nginx-1.22.0; ls -lrth

- 编译安装

.. code-block:: console

    mkdir /approot2
    ./configure --prefix=/approot2/nginx \
    --sbin-path=/usr/sbin/nginx \
    --with-stream \
    --with-threads \
    --with-http_ssl_module \
    --with-http_v2_module \
    --with-http_gzip_static_module \
    --with-http_gunzip_module \
    --with-http_stub_status_module
    make -j$(nproc) && make install

- 应用项目配置文件

.. code-block:: console

    cd /opt
    tar -zxf nginx-conf.tgz --directory /approot2/nginx/conf

- 赋权
  
.. code-block:: console

    chown -R nginx:nginx /approot2

- 创建 systemd 服务
  
.. code-block:: console

    cat << \EOF > /etc/systemd/system/nginx.service
    [Unit]
    Description=The NGINX HTTP and reverse proxy server
    After=syslog.target network-online.target remote-fs.target nss-lookup.target
    Wants=network-online.target uwsgi.service

    [Service]
    Type=forking
    PIDFile=/approot2/nginx/nginx.pid
    ExecStartPost=/bin/sleep 0.1
    ExecStartPre=/usr/bin/rm -f /approot2/nginx/nginx.pid
    ExecStartPre=/usr/sbin/nginx -t
    ExecStart=/usr/sbin/nginx
    ExecReload=/usr/sbin/nginx -s reload
    ExecStop=/bin/kill -s QUIT $MAINPID
    KillSignal=SIGQUIT
    TimeoutStopSec=5
    KillMode=process
    PrivateTmp=true
    Restart=always

    [Install]
    WantedBy=multi-user.target
    EOF

- 重载 systemd 配置
  
.. code-block:: console

    systemctl daemon-reload

- 开启服务自启

.. code-block:: console

    systemctl enable nginx

- 启动服务

.. code-block:: console

    systemctl start nginx
    systemctl status nginx

安装 Redis
-----------

- 创建 redis 用户/组

.. code-block:: console

    groupadd -g 1220 redis
    useradd -u 1220 -g 1220 -r -s /sbin/nologin redis

- 上传软件包与配置

上传 ``redis-7.0.4.tar.gz`` , ``redis-conf.tgz`` 至服务器 ``/opt`` 目录

- 解压

.. code-block:: console

    cd /opt
    tar -zxf redis-7.0.4.tar.gz && cd redis-7.0.4; ls -lrth

- 编译安装
  
.. code-block:: console

    mkdir -p /approot3/redis/conf
    mkdir -p /approot3/redis/logs
    make -j$(nproc) && make install PREFIX=/approot3/redis
    cp utils/redis_init_script /etc/init.d/redis_6379
    ln -s /approot3/redis/bin/redis-cli /usr/sbin/
    ln -s /approot3/redis/bin/redis-server /usr/sbin/

- 应用项目配置文件

.. code-block:: console

    cd /opt
    tar -zxf redis-conf.tgz --directory /approot3/redis/conf

- 赋权
  
.. code-block:: console

    chown -R redis:redis /approot3

- 创建 systemd 服务

.. code-block:: console

    cat << \EOF > /etc/systemd/system/redis.service
    [Unit]
    Description=redis-server
    After=network.target

    [Service]
    User=redis
    Group=redis
    Type=forking
    PIDFile=/approot3/redis/redis_6379.pid
    ExecStartPost=/bin/sleep 0.1
    ExecStartPre=/usr/bin/rm -f /approot3/redis/redis_6379.pid
    ExecStart=/usr/sbin/redis-server /approot3/redis/conf/6379.conf
    ExecStop=/usr/sbin/redis-cli shutdown
    ExecReload=/bin/kill -s HUP $MAINPID

    [Install]
    WantedBy=multi-user.target
    EOF

- 重载 systemd 配置
  
.. code-block:: console

    systemctl daemon-reload

- 开启服务自启

.. code-block:: console

    systemctl enable redis

- 启动服务

.. code-block:: console

    systemctl start redis
    systemctl status redis

安装 MySQL
-----------

- 创建 mysql 用户/组

.. code-block:: console

    groupadd -g 1210 mysql
    useradd -u 1210 -g 1210 -r -s /sbin/nologin mysql

- 检查内置 mariadb-libs
  
.. code-block:: console

    rpm -qa|grep mariadb

若存在 ``mariadb-libs-x.x.xx-x.el7.x86_64`` ，先移除

.. code-block:: console

    rpm -e "mariadb-libs-*" --nodeps

- 上传软件包

上传 ``mysql8.tgz`` 至服务器 ``/opt`` 目录

- 解压

.. code-block:: console

    cd /opt
    tar -zxf mysql8.tgz && cd mysql; ls -lrth

- 使用 ``yum`` 离线安装

.. code-block:: console

    yum install -y --cacheonly --disablerepo=* *.rpm

.. note:: 

    安装时，因为移除了 ``mariadb-libs`` ，会提示内置邮件服务器 ``postfix`` 缺少依赖， ``MySQL`` 安装后即可自动恢复，可忽略

    Warning: RPMDB altered outside of yum.

    ** Found 2 pre-existing rpmdb problem(s), 'yum check' output follows:

    2:postfix-2.10.1-9.el7.x86_64 has missing requires of libmysqlclient.so.18()(64bit)

    2:postfix-2.10.1-9.el7.x86_64 has missing requires of libmysqlclient.so.18(libmysqlclient_18)(64bit)

- 初始化

.. code-block:: console

    mysqld --initialize --console

- 赋权

使用 ``root`` 用户初始化后， ``/var/lib/mysql`` 文件所有者为 ``root``，需重新赋权给 ``mysql``

.. code-block:: console

    chown -R mysql:mysql /var/lib/mysql

- 启动

.. code-block:: console

    systemctl start mysqld

- 检查状态

.. code-block:: console

    systemctl status mysqld

- 获取临时密码

.. code-block:: console

    grep 'temporary password' /var/log/mysqld.log

- 登录并修改密码

.. code-block:: console

    mysql -uroot -p

    ALTER USER 'root'@'localhost' IDENTIFIED BY 'PASSWORD'; 

- 为 SQL 平台建创建用户
  
.. code-block:: console

    CREATE USER 'projectSQL'@localhost IDENTIFIED BY 'PASSWORD';

- 为 SQL 平台创建数据库

.. code-block:: console

    CREATE DATABASE django;

- 赋权

可选 如果需要执行自动测试，额外赋予 ``test_DBNAME`` 权限

.. code-block:: console
    :emphasize-lines: 2

    GRANT ALL ON django.* TO 'projectSQL'@localhost;
    GRANT ALL ON test_django.* TO 'projectSQL'@localhost;

.. hint:: 

    ``CREATE USER``, ``GRANT``, ``REVOKE``, 不需要 ``FLUSH PRIVILEGES``

    ``DROP USER``, ``DELETE form mysql.user`` 等直接修改授权表时才需要 ``FLUSH PRIVILEGES``


- 可选 检查字符集设置

.. code-block:: console

    SHOW VARIABLES LIKE "chara%";

    +--------------------------+--------------------------------+
    | Variable_name            | Value                          |
    +--------------------------+--------------------------------+
    | character_set_client     | utf8mb4                        |
    | character_set_connection | utf8mb4                        |
    | character_set_database   | utf8mb4                        |
    | character_set_filesystem | binary                         |
    | character_set_results    | utf8mb4                        |
    | character_set_server     | utf8mb4                        |
    | character_set_system     | utf8mb3                        |
    | character_sets_dir       | /usr/share/mysql-8.0/charsets/ |
    +--------------------------+--------------------------------+


- 可选 检查数据库字符集和排序规则

.. code-block:: console

    use django
    SELECT @@character_set_database, @@collation_database;

    +--------------------------+----------------------+
    | @@character_set_database | @@collation_database |
    +--------------------------+----------------------+
    | utf8mb4                  | utf8mb4_0900_ai_ci   |
    +--------------------------+----------------------+


- 可选 查看密码验证方式
  
.. code-block:: console

    SELECT user, host, plugin FROM mysql.user;

- 可选 修改密码验证方式

使用 ``pymysql`` 时不需要修改

.. code-block:: console

    ALTER USER 'username'@'ip_address' IDENTIFIED WITH mysql_native_password BY 'PASSWORD';

- 其他 错误排查

数据库名称带有 ``-`` 时，需要加上 ``````

.. code-block:: console

    mysql> CREATE DATABASE django-vue-admin;

	ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '-vue-admin' at line 1

    mysql> CREATE DATABASE `django-vue-admin`

部署 SQL 平台
-------------

- 激活虚拟环境

.. code-block:: console

    source /approot1/venv/bin/activate

- 创建 uwsgi 用户/组

.. code-block:: console

    groupadd -g 1190 uwsgi
    useradd -u 1190 -g 1190 -r -s /sbin/nologin uwsgi

- 上传项目源代码包

上传 ``projectSQL.tgz`` 至服务器 ``/opt`` 目录

- 解压

.. code-block:: console
    
    cd /opt
    tar -zxf projectSQL.tgz --directory /approot1

- 配置环境变量

集中 ``__pychace__`` 缓存目录，保持项目文件夹干净

.. code-block:: console

    cat << \EOF >> /etc/profile
    # 集中 "__pychace__" 缓存目录
    export PYTHONPYCACHEPREFIX="/tmp/.cache/pycache/"
    EOF
    source /etc/profile

- 禁止其他用户访问关键配置文件

配置文件包含数据库密码，必须控制权限

.. code-block:: console

    cd /approot1/projectSQL
    chmod 750 conf sql_platform
    chmod 744 manage.py

- 修复 SimpleUI 列表选择 Bug
  
.. code-block:: console

    cp /approot1/projectSQL/templates/admin/actions.html /approot1/projectSQL/templates/admin/actions.html.bak
    sed -i '$d' /approot1/projectSQL/templates/admin/actions.html
    cat << \EOF >> /approot1/projectSQL/templates/admin/actions.html
        setInterval(function() {
            if ($("#action-toggle").is(":checked")){
                if (_action.select_across){
                    $(".question").hide();
                    $(".all").show();
                    $(".clear").show();
                }
                else{
                    $(".question").show();
                }
            }
            else{
                $(".clear").hide();
                $(".all").hide();
                $(".question").hide();
            }

        }, 100);
    </script>
    EOF

- 生成 SECRET_KEY

.. code-block:: console

    python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

复制生成的 KEY

- 修改 SECRET_KEY

.. code-block:: console

    cd /approot1/projectSQL/sql_platform/
    cp settings.py.sample settings.py
    vi settings.py

    SECRET_KEY = "YOUR_SECRET_KEY"

- 配置项目数据库

修改 ``settings.py`` 中的 ``DATABASES`` 配置，填入安装 ``MySQL`` 时设置的数据库名，用户，密码

.. code-block:: console

    vi settings.py

    DATABASES = {
        "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "django",
        "HOST": "127.0.0.1",
        "USER": "projectSQL",
        "PASSWORD": "PASSWORD",
        "PORT": 3306,
        },
    } 

- 执行迁移

在项目根目录 ``/approot1/projectSQL`` 执行迁移 ``python3 manage.py migrate``，如果数据库连接正常会有如下输出

.. code-block:: console

    (venv) [root@localhost projectSQL]# python3 manage.py migrate
    Operations to perform:
    Apply all migrations: admin, auth, contenttypes, dbmng, explorer, sessions
    Running migrations:
    Applying contenttypes.0001_initial... OK
    Applying auth.0001_initial... OK
    Applying admin.0001_initial... OK
    Applying admin.0002_logentry_remove_auto_add... OK
    Applying admin.0003_logentry_add_action_flag_choices... OK
    Applying contenttypes.0002_remove_content_type_name... OK
    Applying auth.0002_alter_permission_name_max_length... OK
    Applying auth.0003_alter_user_email_max_length... OK
    Applying auth.0004_alter_user_username_opts... OK
    Applying auth.0005_alter_user_last_login_null... OK
    Applying auth.0006_require_contenttypes_0002... OK
    Applying auth.0007_alter_validators_add_error_messages... OK
    Applying auth.0008_alter_user_username_max_length... OK
    Applying auth.0009_alter_user_last_name_max_length... OK
    Applying auth.0010_alter_group_name_max_length... OK
    Applying auth.0011_update_proxy_permissions... OK
    Applying auth.0012_alter_user_first_name_max_length... OK
    Applying dbmng.0001_initial... OK
    Applying explorer.0001_initial... OK
    Applying sessions.0001_initial... OK

- 创建 superuser
  
创建管理员用户 ``python3 manage.py createsuperuser``

.. code-block:: console

    (venv) [root@localhost projectSQL]# python3 manage.py createsuperuser
    用户名 (leave blank to use 'root'):
    电子邮件地址:
    Password:
    Password (again):
    Superuser created successfully.

- 赋权

.. code-block:: console

    chown -R uwsgi:uwsgi /approot1

- 启动服务端
  
手动启动服务端进行测试

.. code-block:: console

    nohup uwsgi --ini /approot1/projectSQL/uwsgi/uwsgi_sql.ini &>/dev/null &

使用 ``jobs`` 命令查看后台任务

.. code-block:: console

    (venv) [root@localhost projectSQL]# nohup uwsgi --ini /approot1/projectSQL/uwsgi/uwsgi_sql.ini &>/dev/null &
    [1] 98421
    (venv) [root@localhost projectSQL]# jobs
    [1]+  Running                 nohup uwsgi --ini /approot1/projectSQL/uwsgi/uwsgi_sql.ini &>/dev/null &

- 查看日志

启动成功将会有如下输出

.. code-block:: console

    less /approot1/projectSQL/logs/uwsgi_sql.log 

    ...
    lock engine: pthread robust mutexes
    thunder lock: enabled
    uwsgi socket 0 bound to UNIX address /approot1/projectSQL/uwsgi/uwsgi_sql.sock fd 3
    Python version: 3.10.5 (main, Jul 24 2022, 15:09:52) [GCC 8.3.1 20190311 (Red Hat 8.3.1-3)]
    Python main interpreter initialized at 0x2a31b10
    python threads support enabled
    your server socket listen backlog is limited to 100 connections
    your mercy for graceful operations on workers is 60 seconds
    mapped 1313856 bytes (1283 KB) for 64 cores
    *** Operational MODE: preforking+threaded ***
    WSGI app 0 (mountpoint='') ready in 0 seconds on interpreter 0x2a31b10 pid: 8534 (default app)
    *** uWSGI is running in multiple interpreter mode ***
    spawned uWSGI master process (pid: 8534)
    spawned uWSGI worker 1 (pid: 8560, cores: 8)
    spawned uWSGI worker 2 (pid: 8561, cores: 8)
    spawned uWSGI worker 3 (pid: 8566, cores: 8)
    spawned uWSGI worker 4 (pid: 8571, cores: 8)
    spawned uWSGI worker 5 (pid: 8580, cores: 8)
    spawned uWSGI worker 6 (pid: 8587, cores: 8)
    spawned uWSGI worker 7 (pid: 8594, cores: 8)
    spawned uWSGI worker 8 (pid: 8601, cores: 8)

.. tip::

    在 ``less`` 中，按 ``SHIFT + F`` 进入自动刷新，使用 ``CRTL + C`` 退出自动刷新，再按 ``Q`` 退出 ``less``

- 访问页面

打开浏览访问服务器 IP 即可看到登录页面，使用之前创建的 ``superuser`` 登录

``http://server_ip``

如果一切正常，使用 ``fg`` 命令调出后台任务，使用 ``CRTL + C`` 结束任务

.. code-block:: console

    (venv) [root@localhost projectSQL]# fg
    nohup uwsgi --ini /approot1/projectSQL/uwsgi/uwsgi_sql.ini &>/dev/null
    ^C(venv) [root@localhost projectSQL]#

.. note:: 

    遇到 ``500`` 错误，首先检查 ``uWSGI`` 目录所有者及权限是否正确

    ``chmod -R uwsgi:uwsgi /approot1``

- 创建 systemd 服务

.. code-block:: console

    cat << \EOF > /etc/systemd/system/uwsgi.service
    [Unit]
    Description=uWSGI Emperor
    After=syslog.target
    Wants=mysqld.service redis.service

    [Service]
    PIDFile=/approot1/projectSQL/uwsgi/uwsgi_sql.pid
    ExecStartPre=/bin/bash -c 'chown -R uwsgi:uwsgi /approot1; /usr/bin/rm -f /approot1/projectSQL/uwsgi/uwsgi_sql.pid'
    ExecStart=/bin/bash -c 'source /approot1/venv/bin/activate; source /etc/profile; uwsgi --ini /approot1/projectSQL/uwsgi/uwsgi_sql.ini'
    ExecReload=/bin/kill -HUP $MAINPID
    ExecStop=/bin/kill -INT $MAINPID
    TimeoutStopSec=5
    KillSignal=SIGQUIT
    Type=notify
    Restart=always
    StandardError=syslog
    NotifyAccess=all

    [Install]
    WantedBy=multi-user.target
    EOF

- 重载 systemd 配置
  
.. code-block:: console

    systemctl daemon-reload

- 开启服务自启

.. code-block:: console

    systemctl enable uwsgi

- 启动服务

.. code-block:: console

    systemctl start uwsgi
    systemctl status uwsgi

至此部署已全部完成，更多管理命令和可选配置请参考 ``管理工具`` 页面

配置文件
--------

- ``sql_platform/settings.py``

项目配置文件，包含数据库、缓存、日志、静态文件、中间件等配置

- ``uwsgi/uwsgi_sql.ini``

uWSGI 配置文件，包含进程数、线程数、日志、socket 等配置，如果你更改了安装目录，必须修改此文件

- ``utils/project_profile.py``

项目环境变量配置文件，包含项目路径、应用名称等配置，如果你更改了安装目录，必须修改此文件

- ``utils/logger.py``

日志记录器配置文件，包含日志格式、日志等级、日志文件路径等配置
