"""ssh2net network ssh client library"""
import logging
from logging import NullHandler

from ssh2net.base import SSH2NetBase
from ssh2net.channel import SSH2NetChannel
from ssh2net.core.driver import BaseNetworkDriver
from ssh2net.netmiko_compatibility import connect_handler as ConnectHandler
from ssh2net.session import SSH2NetSession
from ssh2net.socket import SSH2NetSocket
from ssh2net.ssh_config import SSH2NetSSHConfig

__version__ = "2020.01.10"
__all__ = (
    "SSH2NetSocket",
    "SSH2NetBase",
    "SSH2NetSession",
    "SSH2NetChannel",
    "SSH2NetSSHConfig",
    "ConnectHandler",
    "BaseNetworkDriver",
)


# Class to filter duplicate log entries for the channel logger
# Stolen from: https://stackoverflow.com/questions/44691558/ \
# suppress-multiple-messages-with-same-content-in-python-logging-module-aka-log-co
class DuplicateFilter(logging.Filter):
    """Remove duplicates from log"""

    def filter(self, record):
        # Fields to compare to previous log entry if these fields match; skip log entry
        current_log = (record.module, record.levelno, record.msg)
        if current_log != getattr(self, "last_log", None):
            self.last_log = current_log
            return True
        return False


# Setup socket logger
logging.getLogger(f"{__name__}_socket").addHandler(NullHandler())

# Setup session logger; for session setup/teardown and what we
logging.getLogger(f"{__name__}_session").addHandler(NullHandler())

# Setup channel logger
CHANNEL_ADMIN_LOG = logging.getLogger(f"{__name__}_channel_admin")
# Add duplicate filter to channel log
CHANNEL_ADMIN_LOG.addFilter(DuplicateFilter())
logging.getLogger(f"{__name__}_channel").addHandler(NullHandler())

# Setup channel_raw logger
CHANNEL_RAW_LOG = logging.getLogger(f"{__name__}_channel_raw")
# Add duplicate filter to channel log
CHANNEL_RAW_LOG.addFilter(DuplicateFilter())
logging.getLogger(f"{__name__}_channel_raw").addHandler(NullHandler())
