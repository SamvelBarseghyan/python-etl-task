import logging
from .config import settings

logs_lvl = logging.DEBUG if settings.debug else logging.INFO
logging.basicConfig(
    level=logs_lvl,
    format=settings.log_format
)
