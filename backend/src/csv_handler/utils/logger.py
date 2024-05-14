import logging
from rich.console import Console
from rich.logging import RichHandler
from logging import StreamHandler
from central_config import LOGGER_LEVEL, LOGGER_MOD

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
