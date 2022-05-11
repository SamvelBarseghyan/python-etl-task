import os
import logging
from config import config_by_name

config_type = os.getenv("CONFIG_TYPE", "dev")
settings = config_by_name[config_type]()

logs_lvl = logging.DEBUG if settings.debug else logging.INFO
logging.basicConfig(
    filename=settings.log_filename,
    level=logs_lvl,
    format=settings.log_format
)
