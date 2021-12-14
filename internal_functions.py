import json
import configuration as conf
import logging
import http.client
import os

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

def update_thread_info_json(thread, message):
    if not os.path.isfile(conf.thread_info_json):
        with open(conf.thread_info_json, "w+") as thread_info_file:
            thread_info_file.write('{"threads": []}')

    with open(conf.thread_info_json, "r+") as thread_info_file:
        try:
            thread_info = json.loads(thread_info_file.read())
            # Append thread info to json root object
            thread_info["threads"].append({"thread_id": thread.id, "announce_message_id": message})
            # empt thread info file
            thread_info_file.seek(0) # sets read/write position to the beginning of the file
            # TODO set r/w position to the end of the last object in the root node
            json.dump(thread_info, thread_info_file)

        finally:
            thread_info_file.close()

def get_random_string():
    import string
    import random
    return ''.join(random.choice(string.ascii_letters) for i in range(16))