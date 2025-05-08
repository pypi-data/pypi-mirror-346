import rich
import rich.pretty
import rich.traceback
from loguru import logger
from rich.logging import RichHandler

rich.pretty.install(
    max_string=1_000,
    overflow="ellipsis",
    crop=True,
    # max_length=80,
)
rich.traceback.install(show_locals=True)
logger.configure(handlers=[{"sink": RichHandler(rich_tracebacks=False), "format": "{message}"}])
