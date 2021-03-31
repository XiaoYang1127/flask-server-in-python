import datetime
import os.path
import re
import sys
import logging
from logging.handlers import TimedRotatingFileHandler

from backend.settings import LOG_PATH


def setup_logging(
    logName=None,
    fmt="[%(asctime)s][PID:%(process)d][%(levelname)s][%(name)s] %(message)s",
    level="INFO",
    when="MIDNIGHT",
    backCount=30,
):
    formatter = logging.Formatter(fmt)

    # write log to file
    if logName:
        file_handler = TimedRotatingFileHandler(
            filename="%s/%s" % (LOG_PATH, logName),
            when=when,
            interval=1,
            backupCount=backCount
        )
        file_handler.suffix = "%Y-%m-%d"
        file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        file_handler.setFormatter(formatter)
        logging.getLogger().addHandler(file_handler)

    # output log to stdout
    std_handler = logging.StreamHandler(sys.stdout)
    std_handler.setFormatter(formatter)
    logging.getLogger().addHandler(std_handler)

    logging.getLogger().setLevel(level)

    # Make noisy libraries less noisy
    if level != "DEBUG":
        for name in [
            "passlib",
            "requests.packages.urllib3",
            "snowflake.connector",
            "apiclient",
        ]:
            logging.getLogger(name).setLevel("ERROR")


app_log = logging.getLogger("my_log")
