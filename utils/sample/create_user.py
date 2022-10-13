#!/usr/bin/env python3
import getopt
import logging
import os
import sys

from project_profile import *
# DEFAULT_PASSWORD = "YOUR_PASSWORD"
# PROJECT_DIR = "PATH/TO/PROJECT"
# APP_NAME = "YOUR_APP_NAME"

sys.path.append(PROJECT_DIR)
os.environ["DJANGO_SETTINGS_MODULE"] = f"{APP_NAME}.settings"

import django

django.setup()

from django.contrib.auth.models import User

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# get options
def get_options():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:p:", ["username=", "password="])
    except getopt.GetoptError as err:
        logger.error(err)
        logger.error(f"Usage: {sys.argv[0]} -u <username> -p <password>")
        sys.exit(2)
    username = None
    password = None
    for opt, arg in opts:
        if opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
    if username is None:
        logger.error(f"Usage: {sys.argv[0]} -u <username> -p <password>")
        sys.exit(2)
    elif password is None:
        password = DEFAULT_PASSWORD
    return username, password


#  create user
def create_user(username, password):
    user = User.objects.create_user(username, password=password, is_staff=True)
    user.save()
    logger.info(f"User {username} created")


# main
def main():
    username, password = get_options()
    try:
        create_user(username, password)
    except Exception as err:
        logger.error(err)


# run
if __name__ == "__main__":
    main()
