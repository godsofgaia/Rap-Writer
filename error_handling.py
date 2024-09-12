"""
Importing necessary libraries
"""
import logging
import os
import config  # Import the config module to access settings

# Setup logging configuration
if config.LOGGING_ENABLED:
    log_dir = os.path.join(os.path.expanduser("~"), "RapWriter", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, config.LOG_FILE)

    logging.basicConfig(
        filename=log_file_path,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def log_error(error_message):
    """Logs an error message to a file if logging is enabled."""
    if config.LOGGING_ENABLED:
        logging.error(error_message)
        print(f"Logged error: {error_message}")


def log_info(info_message):
    """Logs an informational message to a file if logging is enabled."""
    if config.LOGGING_ENABLED:
        logging.info(info_message)
        print(f"Logged info: {info_message}")


def log_warning(warning_message):
    """Logs a warning message to a file if logging is enabled."""
    if config.LOGGING_ENABLED:
        logging.warning(warning_message)
        print(f"Logged warning: {warning_message}")


def handle_exception(exception):
    """Handles an exception by logging it and providing user feedback."""
    error_message = f"An error occurred: {str(exception)}"
    log_error(error_message)
    print(f"An error occurred: {str(exception)}")


def setup_logging():
    """Sets up logging if not already configured."""
    if not config.LOGGING_ENABLED:
        return
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            filename=log_file_path,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    print("Logging setup complete.")
