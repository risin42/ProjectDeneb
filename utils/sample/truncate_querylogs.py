#!/usr/bin/env python3
import getopt
import logging
import os
import sys
from datetime import datetime, timedelta

from project_profile import *
# PROJECT_DIR = "PATH/TO/PROJECT"
# APP_NAME = "YOUR_APP_NAME"

sys.path.append(PROJECT_DIR)
os.environ["DJANGO_SETTINGS_MODULE"] = f"{APP_NAME}.settings"

import django

django.setup()

from explorer.models import QueryLog

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# get sys args, raise error if no args or invalid args
def get_args():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:")
    except getopt.GetoptError:
        logger.error("Usage: python3 truncate_querylogs.py -d <days>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-d":
            return int(arg)
    logger.error("Usage: python3 truncate_querylogs.py -d <days>")
    sys.exit(2)


# main
def main(days):
    qs = QueryLog.objects.filter(run_at__lt=datetime.now() - timedelta(days=days))
    # Using a variable to hold the count, do not direct formatting qs.count()
    qs_count = qs.count()
    if qs_count > 0:
        logger.info(f"Deleting {qs_count} QueryLogs older than {days} days.")
    else:
        logger.info(f"No QueryLog older than {days} days.")
    qs.delete()


# run
if __name__ == "__main__":
    logger.info("Starting...")
    days = get_args()
    main(days)
    logger.info("Done.")
    sys.exit(0)
