from typing import Optional
from colorama import Fore, Style, init
from datetime import datetime
from pvmlib.logs.models import Application, Measurement, DataLogger, ExceptionModel
from pvmlib.logs.utils import LogType
from pvmlib.context.request_context import RequestContext
from pvmlib.patterns.decorator import LogSanitizer
from google.cloud.logging_v2 import Client
from google.cloud.logging.handlers import CloudLoggingHandler
from google.cloud import logging_v2
from google.cloud.logging_v2.types import LogMetric
from time import time
import os
import logging
import socket
import sys
import inspect
import traceback
import uuid
import json

# Initialize colorama for cross-platform colored terminal output.
init(autoreset=True)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"  # Define a constant for the date format.

# Basic configuration for logging (handlers are added manually above).
logging.basicConfig(handlers=[])

class LogData:
    """
    A singleton class responsible for collecting and formatting log data.
    It gathers information about the application, environment, and the specific log event.
    """
    _instance = None  # Class variable to hold the single instance.

    def __new__(cls, *args, **kwargs):
        """
        Ensures only one instance of LogData exists (singleton pattern).
        Initializes the instance if it doesn't exist.
        """
        if cls._instance is None:
            cls._instance = super(LogData, cls).__new__(cls)  # Call the superclass's __new__ method.
            cls._instance.__initialize(*args, **kwargs)  # Initialize the instance.
        return cls._instance

    def __initialize(self, origin: str = "INTERNAL"):
        """
        Initializes the LogData instance with default values and environment information.

        Args:
            origin (str): The origin of the log event (e.g., "INTERNAL", "REQUEST"). Defaults to "INTERNAL".
        """
        self.schema_version = os.getenv("VERSION_LOG", "1.0.0")  # Get log schema version from the environment.
        self.log_origin = origin  # Store the origin of the log.
        self.tracing_id = "N/A"  # Default tracing ID.
        self.hostname = socket.gethostname()  # Get the hostname of the machine.
        self.appname = os.getenv("APP_NAME", "default_app")  # Get the application name from the environment.
        self.source_ip = socket.gethostbyname(self.hostname)  # Get the source IP address using hostname.
        self.destination_ip = "N/A"  # Default destination IP address.
        self.additional_info = {}  # Dictionary for storing extra information.
        self.app = Application(  # Create an Application model instance.
            name=os.getenv("APP_NAME", "default"),
            version=os.getenv("API_VERSION", "default"),
            env=os.getenv("ENV", "default"),
            kind=os.getenv("APP_KIND", "default"))
        self.console_formatter = logging.Formatter(
            '%(levelname)s: %(asctime)s - %(message)s',
            datefmt=DATE_FORMAT)  # Define the console log formatter.

        # Initialize the base logger.
        self.logger = logging.getLogger(self.appname)
        self.logger.setLevel(logging.DEBUG)

        root = logging.getLogger(self.appname)
        root.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(self.console_formatter)
        root.addHandler(handler)

        # Initialize Google Cloud Logging.
        try:
            self.gcp_client = Client()  # Create a Google Cloud Logging client.
            self.gcp_logger = self.gcp_client.logger(self.app.name)  # Get a logger for this application.
            self.gcp_handler = CloudLoggingHandler(self.gcp_client, name=self.app.name)  # Create a Cloud Logging handler.
            self.gcp_handler.setLevel(logging.DEBUG)  # Set the GCP handler level to DEBUG.
            self.logger.addHandler(self.gcp_handler)  # Add the GCP handler to the logger.

            # Create HTTP count metrics.
            self.create_http_metrics()

        except Exception as e:
            print(f"Error initializing GCP Logging: {e}. Logging to GCP will be disabled.")  # Print error message.
            self.gcp_client = None  # Disable GCP logging.
            self.gcp_logger = None  # Disable GCP logging.

        self.initialized = True  # Mark the instance as initialized.
        self.log_sanitizer = LogSanitizer()  # Initialize the log sanitizer.

    def create_http_metrics(self):
        """Creates count metrics for HTTP 200, 4xx, and 5xx errors in Google Cloud Logging."""
        try:
            client = logging_v2.Client()  # Create a logging v2 client.

            # Metric to count HTTP 200 responses.
            metric_200 = LogMetric(
                name=f"{self.app.name}_http_200_count",
                filter='resource.type="http_request" AND httpRequest.status=200',
                description=f"Counts HTTP 200 responses for {self.app.name}",
            )
            client.metric(metric_200.name).create(metric_200)  # Create the 200 metric.

            # Metric to count HTTP 4xx responses.
            metric_4xx = LogMetric(
                name=f"{self.app.name}_http_4xx_count",
                filter='resource.type="http_request" AND httpRequest.status >= 400 AND httpRequest.status < 500',
                description=f"Counts HTTP 4xx responses for {self.app.name}",
            )
            client.metric(metric_4xx.name).create(metric_4xx)  # Create the 4xx metric.

            # Metric to count HTTP 5xx responses.
            metric_5xx = LogMetric(
                name=f"{self.app.name}_http_5xx_count",
                filter='resource.type="http_request" AND httpRequest.status >= 500',
                description=f"Counts HTTP 5xx responses for {self.app.name}",
            )
            client.metric(metric_5xx.name).create(metric_5xx)  # Create the 5xx metric.

            print("HTTP error metrics created successfully.")  # Indicate success.

        except Exception as e:
            print(f"Error creating HTTP metrics: {e}")  # Print any errors during metric creation.

    def _format_exception_info(self) -> tuple[Optional[ExceptionModel], str]:
        """
        Formats exception information if an exception occurred.

        Returns:
            tuple[Optional[ExceptionModel], str]: A tuple containing the ExceptionModel (if an exception exists)
                                                and the source file where the exception occurred.
        """
        exception_model = None  # Initialize exception model.
        source_file = "N/A"  # Default source file.
        exc_type, exc_value, exc_traceback = sys.exc_info()  # Get current exception information.
        if exc_type and exc_value and exc_traceback:
            exception_model = ExceptionModel(  # Create an ExceptionModel instance.
                name=exc_type.__name__,
                message=str(exc_value),
                stackTrace=''.join(traceback.format_tb(exc_traceback))  # Format the stack trace.
            )
        tb = traceback.extract_tb(exc_traceback)  # Extract the traceback.
        if tb:
            source_file = tb[-1].filename  # Get the filename from the last frame of the traceback.
        return exception_model, source_file  # Return the exception model and source file.

    def _format_filename(self, full_path: str):
        """
        Extracts a cleaner, more readable filename from a full path.
        Tries to get the path relative to 'src' or 'site-packages' directories.

        Args:
            full_path (str): The full file path.

        Returns:
            str: A formatted filename.
        """
        parts = full_path.split(os.sep)  # Split the path by the OS separator.
        try:
            start_index = 0
            if 'src' in full_path:
                start_index = parts.index("src")  # Find the index of 'src'.
            if 'site-packages' in full_path:
                start_index = parts.index("site-packages")  # Find the index of 'site-packages'.
            filename_with_py = ".".join(parts[start_index:])  # Reconstruct filename.
            filename_without_ext, _ = os.path.splitext(filename_with_py)  # Remove extension.
            return filename_without_ext.replace(os.sep, ".") + ".py"  # Replace separators and add '.py'.
        except ValueError:
            return full_path  # Return the original path if 'src' or 'site-packages' are not found.

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
            log_type (str): The type of log (e.g., "INTERNAL", "REQUEST", "RESPONSE").
                          Defaults to "INTERNAL".
            event_type (str): A specific event type within the log type (e.g., "START", "END", "FAILURE").
                            Defaults to "EVENT".
            status (str): The status of the operation being logged (e.g., "INPROCESS", "SUCCESS", "FAILED").
                            Defaults to "INPROCESS".
            destination_ip (str, optional): The destination IP address if applicable. Defaults to None.
            additional_info (Optional[dict], optional): A dictionary containing extra information to include in the log.
                                                        Defaults to None.
        """
        context = RequestContext()  # Get the current request context.

        if destination_ip is not None:
            self.destination_ip = destination_ip  # Update the destination IP.

        # Get information about the caller function (filename and method name).
        frame_info = inspect.stack()[2]  # Index 2 to get the caller of this log method.
        filename = self._format_filename(frame_info.filename)  # Format the filename.
        method_name = frame_info.function  # Get the method name.

        # Format exception information if an exception is being handled.
        exception_model, source_file = self._format_exception_info()  # Get exception info.

        # Calculate elapsed time.
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
            timestamp=datetime.now().strftime(DATE_FORMAT),  # Use the correct format
            tracing_id=context.get_tracing_id(),  # Get tracing ID from request context.
            hostname=self.hostname,
            event_type=f"{log_type}_{event_type.upper()}",  # Combine log type and event type.
            application=self.app,
            measurement=Measurement(
                method=method_name,
                elapsed_time=f"{elapsed_time:.2f}"  # Format elapsed time to 2 decimal places.
            ),
            destination_ip=self.destination_ip,
            additional_info=additional_info or self.additional_info,
            exception=exception_model,
            source_file=source_file
        )
        console_log, gcp_log_payload = self._format_log(log_entry, filename, method_name,
                                                        context.get_tracing_id())  # Format log for console and GCP.
       
        self.logger.log(level, console_log)
        if self.gcp_client:
            self.gcp_logger.log_struct(gcp_log_payload, severity=level)  # Log to GCP.

    def _format_log(
            self,
            log_entry: DataLogger,
            filename: str,
            method_name: str,
            tracing_id: str
    ):
        """
        Formats the log message for console and GCP Logging.

        Args:
            log_entry (DataLogger): The structured log data.
            filename (str): The source filename of the log call.
            method_name (str): The source method name of the log call.
            tracing_id (str): The current tracing ID.

        Returns:
            tuple[str, dict]: A tuple containing the formatted log message for console output and the payload
                            for Google Cloud Logging.
        """
        name = f"{Fore.CYAN}{self.appname}{Style.RESET_ALL}"  # Colorize the app name.
        date_now = datetime.now().strftime("%H:%M")  # Format the current time.
        id_log_tracing = tracing_id.split('-')[-1] if tracing_id != "N/A" else "N/A"  # Extract last part of tracing ID.
        id_log_instance = LoggerSingleton._instance._id.split('-')[-1]  # Extract last part of logger instance ID.

        part_one_log = f'| {date_now} | {name} == '
        part_thow_log = f'[{id_log_instance},{id_log_tracing}] == '
        part_three_log = f'{filename}::{method_name} -> '

        @self.log_sanitizer.sanitize_decorator
        def format_log_message(log_data: DataLogger) -> str:
            """
            Formats the log message, potentially including the full DataLogger data.
            This function is decorated with the log sanitizer.

            Args:
                log_data: the log entry
            Returns:
                The formatted log message
            """
            return json.dumps(log_data.model_dump())  # Use model_dump() for Pydantic v2

        part_four_log = format_log_message(log_entry)
        console_log = f'{part_one_log}{part_thow_log}{part_three_log}{part_four_log}'  # Format for the console.

        # Create the payload for GCP Logging.  Adhere to the recommended structure.
        gcp_log_payload = {
            "severity": log_entry.level,  # Use 'severity'
            "message": log_entry.message,
            "timestamp": log_entry.timestamp,  # In RFC 3339 format
            "jsonPayload": log_entry.model_dump(),
            "labels": {
                "app_name": log_entry.application.name,
                "environment": log_entry.application.env,
            },
             "resource": {
                "labels": {
                "container_name": f"{log_entry.application.name}-pvm",
                "namespace_name": os.environ.get('KUBERNETES_NAMESPACE', ""),
                "pod_name": log_entry.hostname
                }
            }
        }
        return console_log, gcp_log_payload

    def info(self, *args, **kwargs):
        """Logs a message at the INFO level.

        Args:
            *args:  Positional arguments passed to the underlying log method.
            **kwargs: Keyword arguments passed to the underlying log method.
        """
        self.log(logging.INFO, *args, **kwargs)  # Call the log method with INFO level.

    def error(self, *args, **kwargs):
        """
        Logs a message at the ERROR level.

        Args:
            *args:  Positional arguments passed to the underlying log method.
            **kwargs: Keyword arguments passed to the underlying log method.
        """
        self.log(logging.ERROR, *args, **kwargs)  # Call the log method with ERROR level.

    def warning(self, *args, **kwargs):
        """
        Logs a message at the WARNING level.
        Args:
            *args:  Positional arguments passed to the underlying log method.
            **kwargs: Keyword arguments passed to the underlying log method.
        """
        self.log(logging.WARNING, *args, **kwargs)  # Call the log method with WARNING level.

    def debug(self, *args, **kwargs):
        """
        Logs a message at the DEBUG level.
        Args:
            *args:  Positional arguments passed to the underlying log method.
            **kwargs: Keyword arguments passed to the underlying log method.
        """
        self.log(logging.DEBUG, *args, **kwargs)  # Call the log method with DEBUG level.

    def critical(self, *args, **kwargs):
        """
        Logs a message at the CRITICAL level.
        Args:
            *args:  Positional arguments passed to the underlying log method.
            **kwargs: Keyword arguments passed to the underlying log method.
        """
        self.log(logging.CRITICAL, *args, **kwargs)  # Call the log method with CRITICAL level.


class LoggerSingleton:
    """
    A singleton class that provides a single instance of the LogData class.
    This ensures that all logging within the application uses the same configuration.
    """
    _instance = None  # Class variable to hold the single instance.

    def __new__(cls, *args, **kwargs):
        """
        Ensures only one instance of LoggerSingleton exists.
        Initializes the LogData instance within it if it doesn't exist.
        Assigns a unique ID to the logger instance.
        """
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)  # Call the superclass's __new__ method.
            cls._instance.__initialize(*args, **kwargs)  # Initialize the instance.
            cls._instance._id = str(uuid.uuid4())  # Generate a unique ID for the logger instance.
        return cls._instance

    def __initialize(self):
        """Initializes the LogData instance."""
        self.logger = LogData()  # Create an instance of LogData.

    def get_instance_id(self):
        """Returns the unique ID of this logger instance."""
        return self._id  # Return the unique ID.