import logging
import socket
import time
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_file = 'application.log'
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def check_connectivity(host="google.com.au", port=80, timeout=10):
    """
    Check connectivity to a host on a given port.
    """
    try:
        socket.setdefaulttimeout(timeout)
        sock = socket.create_connection((host, port))
        sock.close()
        return True
    except socket.error:
        return False


def log_isp():
    """
    Get the current Internet Service Provider using an external API.
    """
    response = requests.get('https://ipinfo.io/json')
    data = response.json()
    logger.info("ISP info: %s", data)


if __name__ == "__main__":
    logger.info("Starting connectivity check...")
    log_isp()
    total_failed = 0
    total_count = 1
    while True:
        if check_connectivity():
            logger.info(f"Connectivity check passed. fail rate: {total_failed}/{total_count}")
        else:
            total_failed += 1
            logger.info(f"Connectivity check failed. fail rate: {total_failed}/{total_count}")
        time.sleep(30)
        total_count += 1
