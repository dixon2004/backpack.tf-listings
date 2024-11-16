from aiologger.handlers.streams import AsyncStreamHandler
from aiologger.handlers.files import AsyncFileHandler
from aiologger.formatters.base import Formatter
from aiologger import Logger
import logging.handlers
import logging
import sys
import os


class AsyncLogger:

    def __init__(self, folder_name: str, log_level: str = "INFO"):
        """
        Initialize the AsyncLogger class and set up loggers.

        Args:
            folder_name (str): The name of the folder where log files will be stored.
            log_level (str): The logging level (default is "INFO").
        """
        self.folder_name = folder_name
        self.log_path = os.path.join("./logs", folder_name)
        os.makedirs(self.log_path, exist_ok=True)

        # Ensure the log level is a valid string
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self.logger_info = None
        self.logger_error = None

        # Setup loggers
        self._setup_loggers()


    def _setup_loggers(self):
        """
        Set up loggers for info and error levels.
        """
        # Create a basic formatter
        formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Configure the info logger
        self.logger_info = Logger(name="infoLog", level=self.log_level)
        info_console_handler = AsyncStreamHandler(stream=sys.stdout)
        info_console_handler.formatter = formatter
        self.logger_info.add_handler(info_console_handler)

        info_file_handler = AsyncFileHandler(filename=os.path.join(self.log_path, "info.log"))
        info_file_handler.formatter = formatter
        self.logger_info.add_handler(info_file_handler)

        # Configure the error logger
        self.logger_error = Logger(name="errorLog", level=logging.ERROR)
        error_console_handler = AsyncStreamHandler(stream=sys.stderr)
        error_console_handler.formatter = formatter
        self.logger_error.add_handler(error_console_handler)

        error_file_handler = AsyncFileHandler(filename=os.path.join(self.log_path, "error.log"))
        error_file_handler.formatter = formatter
        self.logger_error.add_handler(error_file_handler)


    async def write_log(self, log_type: str, message: str) -> None:
        """
        Asynchronously log a message based on the log type provided.

        Args:
            log_type (str): The type of log message (e.g., "info", "error").
            message (str): The message to be logged.
        """
        try:
            log_type = log_type.lower()
            if log_type == "debug":
                await self.logger_info.debug(f"[{self.folder_name}] {message}")
            elif log_type == "info":
                await self.logger_info.info(f"[{self.folder_name}] {message}")
            elif log_type == "warning":
                await self.logger_error.warning(f"[{self.folder_name}] {message}")
            elif log_type == "error":
                await self.logger_error.error(f"[{self.folder_name}] {message}")
            elif log_type == "critical":
                await self.logger_error.critical(f"[{self.folder_name}] {message}")
            else:
                await self.logger_error.error("[Logging] Unknown log type specified")
        except Exception as e:
            if self.logger_error:
                await self.logger_error.error(f"[Logging] Exception while logging message: {e}")


class SyncLogger:

    def __init__(self, folder_name: str, log_level: str = "INFO", backup_count: int = 7):
        """
        Initialize the SyncLogger class and set up loggers.

        Args:
            folder_name (str): The name of the folder where log files will be stored.
            log_level (str): The logging level (default is "INFO").
            backup_count (int): Number of backup logs to keep.
        """
        self.folder_name = folder_name
        self.log_path = os.path.join("./logs", folder_name)
        os.makedirs(self.log_path, exist_ok=True)

        # Ensure the log level is a valid string
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)

        # Setup loggers
        self.logger_info = self._setup_logger("infoLog", "info.log", self.log_level)
        self.logger_error = self._setup_logger("errorLog", "error.log", logging.ERROR, backup_count)


    def _setup_logger(self, name: str, log_file: str, log_level: int, backup_count: int = 7) -> logging.Logger:
        """
        Set up a logger with both console and timed file handlers.

        Args:
            name (str): The name of the logger.
            log_file (str): The name of the log file.
            log_level (int): The logging level.
            backup_count (int): Number of backup logs to keep.

        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger(name)
        logger.setLevel(log_level)

        # Check if handlers are already added to avoid duplicate logs
        if not logger.hasHandlers():
            # Create a basic formatter
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            # File handler with daily rotation
            file_path = os.path.join(self.log_path, log_file)
            file_handler = logging.handlers.TimedRotatingFileHandler(
                file_path, when="D", backupCount=backup_count
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger


    def write_log(self, log_type: str, message: str) -> None:
        """
        Write a log message to the appropriate logger.

        Args:
            log_type (str): The type of log message (e.g., "debug", "info", "warning", "error", "critical").
            message (str): The message to be logged.
        """
        try:
            log_type = log_type.lower()
            if log_type == "debug":
                self.logger_info.debug(f"[{self.folder_name}] {message}")
            elif log_type == "info":
                self.logger_info.info(f"[{self.folder_name}] {message}")
            elif log_type == "warning":
                self.logger_error.warning(f"[{self.folder_name}] {message}")
            elif log_type == "error":
                self.logger_error.error(f"[{self.folder_name}] {message}")
            elif log_type == "critical":
                self.logger_error.critical(f"[{self.folder_name}] {message}")
            else:
                self.logger_error.error(f"[{self.folder_name}] [Logging] Unknown log type specified")
        except Exception as e:
            self.logger_error.error(f"[{self.folder_name}] [Logging] Exception while logging message: {e}")
            