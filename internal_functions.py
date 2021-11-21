import logging
import http.client

def change_log_level(level):
    if level == "DEBUG":
        logging.basicConfig(level=logging.DEBUG)
    elif level == "INFO":
        logging.basicConfig(level=logging.INFO)
    elif level == "WARNING":
        logging.basicConfig(level=logging.WARNING)
    elif level == "ERROR":
        logging.basicConfig(level=logging.ERROR)
    elif level == "CRITICAL":
        logging.basicConfig(level=logging.CRITICAL)
    else:
        logging.basicConfig(level=logging.INFO)

def get_web_request(url, method, headers, data):
    conn = http.client.HTTPSConnection(url)
    conn.request(method, "/", data, headers)
    response = conn.getresponse()
    return response.read().decode()