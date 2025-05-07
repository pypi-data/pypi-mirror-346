from typing import Optional, Union
from colorama import Fore, Style, init
from datetime import datetime
from pvmlib.logs.models import Application, Measurement, DataLogger, ExceptionModel
from pvmlib.logs.utils import LogType
from pvmlib.context.request_context import RequestContext
from pvmlib.patterns.decorator import LogSanitizer
from time import time
import os
import logging
import socket
import sys
import inspect
import traceback
import uuid
import json

# Define a standard date format for log timestamps.
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Initialize colorama for cross-platform colored terminal output.
init(autoreset=True)

# Get the root logger named 'uvicorn' (often used by ASGI servers).
logger = logging.getLogger("uvicorn")
# Set the logging level for this logger to DEBUG, meaning all levels will be considered.
logger.setLevel(logging.DEBUG)

# Create a formatter for console output.
console_formatter = logging.Formatter(
    '%(levelname)s: %(asctime)s - %(message)s',
    datefmt=DATE_FORMAT
)

# Create a handler for standard output (console).
stdout_handler = logging.StreamHandler(sys.stdout)
# Set the logging level for this handler to INFO, so only INFO and higher levels are displayed.
stdout_handler.setLevel(logging.INFO)
# Apply the formatter to the stdout handler.
stdout_handler.setFormatter(console_formatter)
# Add the stdout handler to the logger.
logger.addHandler(stdout_handler)

# Create a handler for standard error (console).
stderr_handler = logging.StreamHandler(sys.stderr)
# Set the logging level for this handler to ERROR, so only ERROR and higher levels are displayed.
stderr_handler.setLevel(logging.ERROR)
# Apply the formatter to the stderr handler.
stderr_handler.setFormatter(console_formatter)
# Add the stderr handler to the logger.
logger.addHandler(stderr_handler)

# Basic configuration for logging (though handlers are added manually above).
logging.basicConfig(handlers=[])

class LogData:
    """
    A singleton class responsible for collecting and formatting log data.
    It gathers information about the application, environment, and the specific log event.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Ensures only one instance of LogData exists (singleton pattern).
        Initializes the instance if it doesn't exist.
        """
        if cls._instance is None:
            cls._instance = super(LogData, cls).__new__(cls)
            cls._instance.__initialize(*args, **kwargs)
        return cls._instance

    def __initialize(self, origin: str = "INTERNAL"):
        """
        Initializes the LogData instance with default values and environment information.

        Args:
            origin (str): The origin of the log event (e.g., "INTERNAL", "REQUEST"). Defaults to "INTERNAL".
        """
        self.logger = logger  # Use the configured logger.
        self.schema_version = os.getenv("VERSION_LOG", "1.0.0")  # Get log schema version from environment.
        self.log_origin = origin
        self.tracing_id = "N/A"  # Default tracing ID.
        self.hostname = socket.gethostname()  # Get the hostname of the machine.
        self.appname = os.getenv("APP_NAME", )  # Get the application name from environment.
        self.source_ip = socket.gethostbyname(socket.gethostname())  # Get the source IP address.
        self.destination_ip = "N/A"  # Default destination IP address.
        self.additional_info = {}  # Dictionary for storing extra information.
        self.app = Application(  # Create an Application model instance.
            name = os.getenv("APP_NAME", "default"),
            version = os.getenv("API_VERSION", "default"),
            env = os.getenv("ENV", "default"),
            kind = os.getenv("APP_KIND", "default"))
        self.initialized = True
        self.log_sanitizer = LogSanitizer()

    def _format_exception_info(self) -> tuple[Optional[ExceptionModel], str]:
        """
        Formats exception information if an exception occurred.

        Returns:
            tuple[Optional[ExceptionModel], str]: A tuple containing the ExceptionModel (if an exception exists)
                                                 and the source file where the exception occurred.
        """
        exception_model = None
        source_file = "N/A"
        exc_type, exc_value, exc_traceback = sys.exc_info()  # Get current exception information.
        if exc_type and exc_value and exc_traceback:
            exception_model = ExceptionModel(
                name=exc_type.__name__,
                message=str(exc_value),
                stackTrace=''.join(traceback.format_tb(exc_traceback))  # Format the stack trace.
            )
        tb = traceback.extract_tb(exc_traceback)
        if tb:
            source_file = tb[-1].filename  # Get the filename from the last frame of the traceback.
        return exception_model, source_file
    
    def _format_exception_info2(self, exc_info_passed: Union[None, Exception, bool] = None) -> tuple[Optional[ExceptionModel], str]:
        """
        Formats exception information if an exception occurred.

        Returns:
            tuple[Optional[ExceptionModel], str]: A tuple containing the ExceptionModel (if an exception exists)
                                                and the source file where the exception occurred.
        """
        exception_model = None
        source_file = "N/A"
        exc_type, exc_value, exc_traceback = (None, None, None)

        if isinstance(exc_info_passed, BaseException):
            exc_type = type(exc_info_passed)
            exc_value = exc_info_passed
            exc_traceback = exc_info_passed.__traceback__
        elif exc_info_passed is True:
            exc_type, exc_value, exc_traceback = sys.exc_info()

        if exc_type and exc_value and exc_traceback:
            exception_model = ExceptionModel(
                name=exc_type.__name__,
                message=str(exc_value),
                stackTrace=''.join(traceback.format_tb(exc_traceback))
            )
            tb = traceback.extract_tb(exc_traceback)
            if tb:
                source_file = tb[-1].filename  # Get the filename from the last frame of the traceback.
        return exception_model, source_file

    def _format_filename(self, full_path):
        """
        Extracts a cleaner, more readable filename from a full path.
        Tries to get the path relative to 'src' or 'site-packages' directories.

        Args:
            full_path (str): The full file path.

        Returns:
            str: A formatted filename.
        """
        parts = full_path.split(os.sep)
        start_index = ""
        try:
            if 'src' in full_path:
                start_index = parts.index("src")
            if 'site-packages' in full_path:
                start_index = parts.index("site-packages")
            filename_with_py = ".".join(parts[start_index:])
            filename_without_ext, _ = os.path.splitext(filename_with_py)
            return filename_without_ext.replace(os.sep, ".") + ".py"
        except ValueError:
            return full_path  # Return the full path if 'src' or 'site-packages' are not found.

    def log(
        self,
        level: int,
        message: str,
        log_type: str = LogType.INTERNAL,
        event_type: str = "EVENT",
        status: str = "INPROCESS",
        destination_ip: str = None,
        additional_info: Optional[dict] = None
        ) -> None:
        """
        Logs a message with the specified level and additional information.

        Args:
            level (int): The logging level (e.g., logging.INFO, logging.ERROR).
            message (str): The log message.
            log_type (str): The type of log (e.g., "INTERNAL", "REQUEST", "RESPONSE"). Defaults to LogType.INTERNAL.
            event_type (str): A specific event type within the log type (e.g., "START", "END", "FAILURE"). Defaults to "EVENT".
            status (str): The status of the operation being logged (e.g., "INPROCESS", "SUCCESS", "FAILED"). Defaults to "INPROCESS".
            destination_ip (str, optional): The destination IP address if applicable. Defaults to None.
            additional_info (Optional[dict], optional): A dictionary containing extra information to include in the log. Defaults to None.
        """
        context = RequestContext()  # Get the current request context.

        if destination_ip is not None:
            self.destination_ip = destination_ip

        # Get information about the caller function (filename and method name).
        frame_info = inspect.stack()[2]  # Index 2 to get the caller of this log method.
        filename = self._format_filename(frame_info.filename)
        method_name = frame_info.function

        # Format exception information if an exception is being handled.
        exception_model, source_file = self._format_exception_info()

        # Time elapsed
        elapsed_time = time() - context.get_start_time() if context.get_start_time() else 0.00
        # Create a DataLogger model instance to structure the log data.
        log_entry = DataLogger(
            level=logging.getLevelName(level),  # Convert level integer to name (e.g., INFO).
            schema_version=self.schema_version,
            log_type=log_type,
            source_ip=self.source_ip,
            status=status,
            message=message,
            log_origin=self.log_origin,
            timestamp=datetime.now().strftime(DATE_FORMAT),
            tracing_id=context.get_tracing_id(),  # Get tracing ID from request context.
            hostname=self.hostname,
            event_type=f"{log_type}_{event_type.upper()}",  # Combine log type and event type.
            application=self.app,
            measurement=Measurement(
                method=method_name,
                elapsed_time=f"{elapsed_time:.2f}"
            ),
            destination_ip=self.destination_ip,
            additional_info=additional_info or self.additional_info,
            exception=exception_model,
            source_file=source_file
        )
        # Log the formatted message using the standard logger.
        self.logger.log(level, self._format_log(level, log_entry, filename, method_name, message, context.get_tracing_id()))

    def _format_log(
        self,
        level: int,
        log_entry: DataLogger,
        filename: str,
        method_name: str,
        message: str,
        tracing_id: str
    ):
        """
        Formats the log message for console output.

        Args:
            level (int): The logging level.
            log_entry (DataLogger): The structured log data.
            filename (str): The source filename of the log call.
            method_name (str): The source method name of the log call.
            message (str): The original log message.
            tracing_id (str): The current tracing ID.

        Returns:
            str: The formatted log message for console output.
        """
        name = f"{Fore.CYAN}{self.appname}{Style.RESET_ALL}"  # Colorize the app name.
        date_now = datetime.now().strftime("%H:%M")  # Format the current time.
        id_log_tracing = tracing_id.split('-')[-1] if tracing_id != "N/A" else "N/A"  # Extract last part of tracing ID.
        id_log_instance = LoggerSingleton._instance._id.split('-')[-1]  # Extract last part of logger instance ID.

        part_one_log = f'| {date_now} | {name} == '
        part_thow_log= f'[{id_log_instance},{id_log_tracing}] == '
        part_three_log = f'{filename}::{method_name} -> '
    
        @self.log_sanitizer.sanitize_decorator
        def format_log_message(log_data: DataLogger, msg: str, lvl: int) -> str:
                """
                Formats the log message, potentially including the full DataLogger data.  This function is decorated.

                Args:
                    log_data: the log entry
                    msg: the message
                    lvl: the log level
                Returns:
                    The formatted log message
                """
                #if lvl != logging.INFO:
                return json.dumps(log_data.model_dump())  # Return the whole structure as JSON (string)
                #else:
                #return f'{msg} ==> {log_data.additional_info}' if log_data.additional_info else msg  # Return just the message
        part_four_log = format_log_message(log_entry, message, level)
        return f'{part_one_log}{part_thow_log}{part_three_log}{part_four_log}'

    def info(self, *args, **kwargs):
        """Logs a message at the INFO level.
           message: Message informativo.
           additional_info: Info additional (Optional)
        """
        self.log(logging.INFO, *args, **kwargs)

    def error(self, *args, **kwargs):
        """
        Logs a message at the ERROR level.

        Args:
            *args: Positional arguments passed to the `log` method (typically the message).
            **kwargs: Keyword arguments passed to the `log` method, such as `log_type`, `event_type`,
                      `status`, `destination_ip`, and `additional_info`.
        """
        self.log(logging.ERROR, *args, **kwargs)

    def warning(self, *args, **kwargs):
        """
        Logs a message at the WARNING level.

        Args:
            *args: Positional arguments passed to the `log` method (typically the message).
            **kwargs: Keyword arguments passed to the `log` method, such as `log_type`, `event_type`,
                      `status`, `destination_ip`, and `additional_info`.
        """
        self.log(logging.WARNING, *args, **kwargs)

    def debug(self, *args, **kwargs):
        """
        Logs a message at the DEBUG level.

        Args:
            *args: Positional arguments passed to the `log` method (typically the message).
            **kwargs: Keyword arguments passed to the `log` method, such as `log_type`, `event_type`,
                      `status`, `destination_ip`, and `additional_info`.
        """
        self.log(logging.DEBUG, *args, **kwargs)

    def critical(self, *args, **kwargs):
        """
        Logs a message at the CRITICAL level.

        Args:
            *args: Positional arguments passed to the `log` method (typically the message).
            **kwargs: Keyword arguments passed to the `log` method, such as `log_type`, `event_type`,
                      `status`, `destination_ip`, and `additional_info`.
        """
        self.log(logging.CRITICAL, *args, **kwargs)

class LoggerSingleton:
    """
    A singleton class that provides a single instance of the LogData class.
    This ensures that all logging within the application uses the same configuration.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Ensures only one instance of LoggerSingleton exists.
        Initializes the LogData instance within it if it doesn't exist.
        Assigns a unique ID to the logger instance.
        """
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)
            cls._instance.__initialize(*args, **kwargs)
            cls._instance._id = str(uuid.uuid4())  # Generate a unique ID for the logger instance.
        return cls._instance

    def __initialize(self):
        """Initializes the LogData instance."""
        self.logger = LogData()

    def get_instance_id(self):
        """Returns the unique ID of this logger instance."""
        return self._id