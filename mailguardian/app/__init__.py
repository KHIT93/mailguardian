from mailguardian.config.app import settings
from mailguardian.config.logging import setup_logging

# Configure logging
logger = setup_logging(log_level=settings.APP_LOGLEVEL, log_output='default', log_dir=settings.APP_LOGDIR if settings.APP_LOG_TO_FILE else None)
