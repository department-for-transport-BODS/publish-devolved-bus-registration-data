import logging
import os

from rich.console import Console

console = Console()

# from rich.logging import RichHandler
# logging.basicConfig(
#     level="NOTSET",
#     format="%(message)s",
#     datefmt="[%X]",
#     handlers=[RichHandler(rich_tracebacks=True)],
# )


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[38;5;202m",
    }
    RESET = "\033[0m"

    def msg_format(self, record):
        logger_mod = os.environ.get("LOGGER_MOD", "localdev")
        if logger_mod == "localdev":
            color = self.COLORS.get(record.levelname, self.RESET)
            logger_message = (
                f"{color}{record.levelname}{self.RESET}: {record.log_date}"
                f" {record.module}:{record.lineno} : {record.message}"
            )
        else:
            logger_message = f"{record.levelname}: {record.message}"
        return logger_message

    def format(self, record):
        super().format(record)
        record.log_date = f"{self.formatTime(record, '%Y-%m-%d %H:%M:%S')}"
        return self.msg_format(record)


log = logging.getLogger("backendLogger")
log_level = os.environ.get("LOGGER_LEVEL", "DEBUG")
log.setLevel(log_level)

# Console logger
console_handler = logging.StreamHandler()
# Apply formatting to the log message
formatter = ColoredFormatter()
# Apply format for the handler
console_handler.setFormatter(formatter)

# Attach handler to the logger
log.addHandler(console_handler)

