import logging

package_logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="last_run.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(levelname)s:%(message)s",
    filemode="w",
)

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("portfolio_optimizer")
except PackageNotFoundError:
    __version__ = "0.0"
