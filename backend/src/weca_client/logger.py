import logging
from rich.console import Console
from rich.logging import RichHandler
from logging import StreamHandler
LOGGER_LEVEL = "DEBUG"
LOGGER_MOD = "local"

console = Console()


if LOGGER_MOD == "local":
    logging.basicConfig(
        level=LOGGER_LEVEL,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
else:
    print("Appling else condition")
    logging.basicConfig(
        level=LOGGER_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        # datefmt="[%X]",
        handlers=[StreamHandler()],
    )

log = logging.getLogger("csv_handler")
# Usage:
# log.debug({"key": "value", "key2": "value2"})
# log.info("this is info message")
# log.warning("this is warning message")
# log.error("this is error message")
# log.critical("this is critical message")
