#!/usr/bin/bash

BASE_DIR=${BASE_DIR:-"/approot1/projectSQL"}
BASE_NAME=${uwsgi_sql:-"uwsgi_sql"}
LOG_DIR=$BASE_DIR/logs
UWSGI_PID=$BASE_DIR/uwsgi/$BASE_NAME.pid

mv $LOG_DIR/$BASE_NAME.log $LOG_DIR/archived/$BASE_NAME."$(date '+%Y%m%d_%H%M')".log
uwsgi --reload "$UWSGI_PID"
