import logging
import logging.handlers
import os
import time
from pathlib import Path
import threading

logging_initialized: bool = False

logger: logging.Logger = logging.getLogger('')

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, _NOTHING, DEFAULT = range(10)
#The background is set with 40 plus the number of the color, and the foreground with 30
#These are the sequences needed to get colored output
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
COLOR_PATTERN = "%s%s%%s%s" % (COLOR_SEQ, COLOR_SEQ, RESET_SEQ)
LEVEL_COLOR_MAPPING = {
    logging.DEBUG: (BLUE, DEFAULT),
    logging.INFO: (GREEN, DEFAULT),
    logging.WARNING: (YELLOW, DEFAULT),
    logging.ERROR: (RED, DEFAULT),
    logging.CRITICAL: (WHITE, RED),
}

class PerfFilter(logging.Filter):
    def format_perf(self, query_count, query_time, remaining_time):
        return ("%d" % query_count, "%.3f" % query_time, "%.3f" % remaining_time)

    def filter(self, record):
        if hasattr(threading.current_thread(), "query_count"):
            query_count = threading.current_thread().query_count
            query_time = threading.current_thread().query_time
            perf_t0 = threading.current_thread().perf_t0
            remaining_time = time.time() - perf_t0 - query_time
            record.perf_info = '%s %s %s' % self.format_perf(query_count, query_time, remaining_time)
            delattr(threading.current_thread(), "query_count")
        else:
            record.perf_info = "- - -"
        return True
    
class ColoredPerfFilter(PerfFilter):
    def format_perf(self, query_count, query_time, remaining_time):
        def colorize_time(time, format, low=1, high=5):
            if time > high:
                return COLOR_PATTERN % (30 + RED, 40 + DEFAULT, format % time)
            if time > low:
                return COLOR_PATTERN % (30 + YELLOW, 40 + DEFAULT, format % time)
            return format % time
        return (
            colorize_time(query_count, "%d", 100, 1000),
            colorize_time(query_time, "%.3f", 0.1, 3),
            colorize_time(remaining_time, "%.3f", 1, 5)
            )

class DBFormatter(logging.Formatter):
    def format(self, record):
        record.pid = os.getpid()
        return logging.Formatter.format(self, record)

class ColoredFormatter(DBFormatter):
    def format(self, record):
        fg_color, bg_color = LEVEL_COLOR_MAPPING.get(record.levelno, (GREEN, DEFAULT))
        record.levelname = COLOR_PATTERN % (30 + fg_color, 40 + bg_color, record.levelname)
        return DBFormatter.format(self, record)

# LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FORMAT: str = '%(asctime)s %(pid)s %(levelname)s %(name)s: %(message)s'

perf_filter = logging.Filter = PerfFilter()

def init_logger(level: int):
    global logging_initialized
    if not logging_initialized:
        logging.basicConfig(level=level, format=LOG_FORMAT, handlers=[])
        logging_initialized = True
    logger.addFilter(perf_filter)

def enable_stdout_logging():
    logger.debug('Enabling logging to stdout')
    formatter: logging.Formatter = ColoredFormatter(LOG_FORMAT)
    console: logging.StreamHandler = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

def enable_logfile(filename: Path):
    log_file: Path = filename
    logger.debug('Enabling logging to file: %s' % (log_file,))
    if not filename.parent.exists():
        logger.debug('Path for log folder %s does not exist. Creating...' % (log_file.parent,))
        filename.parent.mkdir(parents=True, exist_ok=True)
    formatter: logging.Formatter = DBFormatter(LOG_FORMAT)
    filehandler: logging.handlers.TimedRotatingFileHandler = logging.handlers.TimedRotatingFileHandler(filename=log_file, when="midnight", backupCount=30)
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

def customize_fastapi_logger():
    fastapi_logger = logging.getLogger('fastapi')
    uvicorn = logging.getLogger("uvicorn")
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_error = logging.getLogger("uvicorn.error")
    formatter: logging.Formatter = ColoredFormatter(LOG_FORMAT)
    console: logging.StreamHandler = logging.StreamHandler()
    console.setFormatter(formatter)
    fastapi_logger.handlers = []
    fastapi_logger.addHandler(console)
    uvicorn.handlers = []
    uvicorn.addHandler(console)
    uvicorn_access.handlers = []
    uvicorn_access.addHandler(console)
    uvicorn_error.handlers = []
    uvicorn_error.addHandler(console)

# class LoggerSetup:
#     def __init__(self) -> None:
#         self.logger = logging.getLogger('')
#         self.setup_logging()

#     def setup_logging(self):
#         logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

#         formatter = logging.Formatter(LOG_FORMAT)

#         console = logging.StreamHandler()
#         console.setFormatter(formatter)
