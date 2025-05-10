import json
import logging
import time
import httpx
from datetime import datetime


class LokiHandler(logging.Handler):
    """ Log handler for sending logs to Grafana Loki """

    def __init__(self, loki_host: str, loki_port: str | int, labels: dict):
        super().__init__()
        self.url = f"http://{loki_host}:{loki_port}/loki/api/v1/push"
        self.labels = {str(k): str(v) for k, v in labels.items()}
        self.labels["service_name"] = labels.get("app")
        self.client = httpx.Client(headers={"Content-Type": "application/json"})

    def emit(self, record: logging.LogRecord):
        """ Send log to Loki """
        log_message = self.format(record)
        log_entry = [{
            "stream": self.labels,
            "values": [[str(int(time.time() * 1e9)), f"{datetime.now()} | {log_message}"]],
        }]
        log_data = {"streams": log_entry}
        try:
            response = self.client.post(self.url, headers={"Content-Type": "application/json"},
                                        data=json.dumps(log_data))
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"Error sending log: {e.response.status_code} {e.response.text}")


def setup_logger(loki_host, loki_port, labels: dict, logging_level=logging.INFO):
    logger_name = f"loki_logger_{labels['app']}"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)

    loki_handler = LokiHandler(loki_host, loki_port, labels)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    loki_handler.setFormatter(formatter)
    logger.addHandler(loki_handler)
    return logger


def setup_console_logger(name="salesmanago_tools"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create a console handler that writes to stdout
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Set a simple log format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Prevent adding multiple handlers if setup_console_logger is called multiple times
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":
    logger = setup_logger("185.253.7.140", 3100, labels={"app": "salesmanago_tools"})
    logger.info("TEST")
