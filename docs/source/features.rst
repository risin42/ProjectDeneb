功能提示
========

预览界面
--------

- 点击执行耗时前的 ``#`` 可显示行号
- 点击字段名可以排序
- 可全屏查看结果

数据透视表
----------

- 在查询结果的 TAB 处可查看数据透视表

参数化查询
----------

- 支持图形化界面的参数化查询

用法： 

 使用双 ``$$`` 包裹参数名， ``$$foo$$``

 加上冒号为参数提供默认值 ``$$foo:bar$$``

 建议在保存语句时添加默认值，否则会因为参数为空导致数据库返回语法错误提示（不影响保存）

例：

1. 新增查询

.. code-block:: console

  SELECT *
  FROM explorer_querylog
  WHERE run_by_user_id=$$id:1$$

2. 保存

3. 在查询列表中打开刚刚保存的语句

4. SQL 输入区域下方会生成参数输入框，输入新数值即可复用查询语句

.. tip::

  可以使用多个参数，当查询语句较长又仅需要更改其中部分字段时，可以避免改动原语句实现复用

  .. code-block:: console

    SELECT *
    FROM $$table:explorer_querylog$$
    WHERE id=$$id:1$$
  
.. note::

  从查询列表复用查询时，需输入原查询描述，否则会保存为新查询

使用 API
---------

- 可通过 API 调用已保存的查询语句

在 ``settings.py`` 中配置 ``EXPLORER_TOKEN_AUTH_ENABLED = True`` 以及 ``EXPLORER_TOKEN``

例：

.. code-block:: console

  curl -H "X-API-TOKEN <YOUR_TOKEN>" http://example.com/<query_id>/stream?format=csv

或者将 token 作为参数传入

.. code-block:: console

  curl http://example.com/<query_id>/stream?format=csv\&token=${YOUR_TOKEN}\&params=field:run_by_user_id\|table:explorer_querylog

导出
----

- 支持将 SQL 结果导出为以下格式

  + csv
  + xlsx
  + json

显示表结构
----------

- 点击后会在右侧显示当前选择数据库的 Schema

.. note::

    此操作使用 ``Django DB introspection`` 生成 Schema，效率并不高，生成后会缓存，并不会实时刷新

格式化语句
----------

- 点击后会将 SQL 输入框中的语句格式化显示（仅格式化，不判断语句本身是否正确）

页面指引
--------

快速查询
^^^^^^^^

- 在此页面输入 SQL 即可执行查询，无需填写查询描述，也不会记录在查询列表的最近查询中

.. hint::

    在 SQL 输入框按下 ``CRTL+ENTER`` 可以快速执行查询

查询列表
^^^^^^^^

- 此页面列出所有在 ``新增查询`` 页面添加的 SQL 语句，可以快速进行提交，导出，编辑等操作

新增查询
^^^^^^^^

- 此页面可以添加常用 SQL 语句，在 ``查询列表`` 页面方便地复用
- 可用于在任何需要具体留档的 SQL 语句执行前补充描述信息以便审计，创建者和创建时间会永久记录
- 每条语句会有一个独立的查询 ``ID`` ，体现在 URL 中

查询日志
^^^^^^^^

- 此页面可以查看历史查询日志，包括快速查询在内的所有 SQL 语句执行都将记录

- 会记录以下信息

  + 执行时间
  + 执行人
  + 执行耗时
  + SQL 语句
  + 查询 ID

其他特性
--------

请参考 ``配置选项`` 页面