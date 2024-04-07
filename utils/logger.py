import logging
import datetime
import os


class Logger:
    """
    Logs information at configured level. Creates a new log file for each program execution.
    """
    def __init__(self, logging_level="info"):
        # Directory for logs
        base_dir = os.path.dirname(os.path.abspath(__file__))
        logs_dir = os.path.join(base_dir, "../logs")

        # Ensure logs directory exists
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
        log_filename = os.path.join(logs_dir, f"process_{timestamp}")

        # Setup logger
        self.logger = logging.getLogger(__name__)
        if logging_level == "error":
            self.logger.setLevel(logging.ERROR)
        else:
            self.logger.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(funcName)s: %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        # File handler
        fh = logging.FileHandler(log_filename)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        # Stream handler (to console)
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
