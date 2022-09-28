#!/usr/bin/env python3
import logging
import os
import sys

from project_profile import *
# PROJECT_DIR = "PATH/TO/PROJECT"
# APP_NAME = "YOUR_APP_NAME"

sys.path.append(PROJECT_DIR)
os.environ["DJANGO_SETTINGS_MODULE"] = f"{APP_NAME}.settings"

import django

django.setup()

from conf.env import DATABASES_EXTRA
from dbmng.models import dbdata
from django.conf import settings

BASE_DIR = settings.BASE_DIR
CONF_DIR = f"{BASE_DIR}/conf"
ENV_CONF = "env.py"
EXPLORER_CONF = "explorer.py"
ARCHIVED = f"{BASE_DIR}/conf/archived"
UWSGI_PID = f"{BASE_DIR}/uwsgi/uwsgi_sql.pid"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# get db data from dbdata model
db_remote = dbdata.objects.values(
    "DBID", "ENGINE", "DBNAME", "USER", "PASSWORD", "HOST", "PORT"
)
# logger.debug(f"db_remote: {db_remote}")

# convert dbdata to list
db_remote_to_list = list(db_remote)
# logger.debug(f"db_remote_to_list: {db_remote_to_list}")

# format dbdata to django dict
db_remote_f = {
    db["DBID"]: {
        "ENGINE": db["ENGINE"],
        "NAME": db["DBNAME"],
        "USER": db["USER"],
        "PASSWORD": db["PASSWORD"],
        "HOST": db["HOST"],
        "PORT": db["PORT"],
    }
    for db in db_remote_to_list
}
# logger.debug(f"db_remote_f: {db_remote_f}")

db_remote_f_list = [db["DBID"] for db in db_remote_to_list]
logger.info(f"DB remote: {db_remote_f_list}")

# get local dbdata from env.py
db_local = DATABASES_EXTRA
# logger.debug(f"db_local: {db_local}")

db_local_list = list(db_local)
logger.info(f"DB local before add: {db_local_list}")

diff_db = [x for x in db_remote_f if x not in db_local]
logger.info(f"Diff DB +: {diff_db}")

# if some db in db_remote not in db_local, then add to db_local
for db in db_remote_f:
    if db not in db_local:
        db_local[db] = db_remote_f[db]
        logger.info(f"Adding DB to local: {db}")
    else:
        logger.info(f"DB: {db} is exists")

db_local_after_add = list(db_local)
logger.info(f"DB local after add: {db_local_after_add}")

# Phase One synchronization is completed
logger.info("Phase 1 synchronization is completed")

db_remote_f_list = db_remote_f_list
logger.info(f"DB remote: {db_remote_f_list}")

db_local_before_remove = list(db_local)
logger.info(f"DB local before remove: {db_local_before_remove}")

diff_db = [x for x in db_local if x not in db_remote_f]
logger.info(f"Diff DB -: {diff_db}")

# if some db in db_local not in db_remote, then remove from db_local
for db in db_local.copy():
    if db not in db_remote_f:
        del db_local[db]
        logger.info(f"Removing DB from local: {db}")
    else:
        logger.info(f"DB: {db} is exists")

db_local_after_remove = list(db_local)
logger.info(f"DB local after remove: {db_local_after_remove}")

logger.info("Phase 2 synchronization is completed")

# backup env.py
os.system(
    f"cp {CONF_DIR}/{ENV_CONF} {ARCHIVED}/{ENV_CONF}.$(date '+%Y%m%d_%H%M%S')"
)
logger.info(f"Backing up {ENV_CONF} to {ARCHIVED}")

# write db_local back to env.py
# logger.debug(f"DATABASES_EXTRA = {db_local}")
with open(f"{CONF_DIR}/{ENV_CONF}", "w") as f:
    f.write(f"DATABASES_EXTRA = {db_local}")
logger.info(f"Writing DB connection string to {ENV_CONF}")

# backup explorer.py
os.system(
    f"cp {CONF_DIR}/{EXPLORER_CONF} {ARCHIVED}/{EXPLORER_CONF}.$(date '+%Y%m%d_%H%M%S')"
)
logger.info(f"Backing up {EXPLORER_CONF} to {ARCHIVED}")

# add db_local keys to explorer connection list
EXPLORER_CONNECTIONS_EXTRA = { db: db for db in db_local }
# logger.debug(f"EXPLORER_CONNECTIONS_EXTRA: {EXPLORER_CONNECTIONS_EXTRA}")

# sort explorer_connection_extra by keys
EXPLORER_CONNECTIONS_EXTRA_sorted = dict(sorted(EXPLORER_CONNECTIONS_EXTRA.items()))
# logger.debug(f"EXPLORER_CONNECTIONS_EXTRA_sorted = {EXPLORER_CONNECTIONS_EXTRA_sorted}")

# write to explorer.py
with open(f"{CONF_DIR}/{EXPLORER_CONF}", "w") as f:
    f.write(f"EXPLORER_CONNECTIONS_EXTRA = {EXPLORER_CONNECTIONS_EXTRA_sorted}")
logger.info(f"Writing EXPLORER_CONNECTIONS_EXTRA to {EXPLORER_CONF}")

logger.info("Phase 3 write to env.py and explorer.py is completed")

# reload uwsgi
os.system(f"uwsgi --reload {UWSGI_PID}")
logger.info("Reloading uWSGI")

# flush redis
os.system("redis-cli -n 1 flushdb &> /dev/null")
logger.info("Flushing Redis")

logger.info("All done.")
