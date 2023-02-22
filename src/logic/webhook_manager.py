"""

"""
# ------------------------------------------------------- #
#                     imports
# ------------------------------------------------------- #
import requests
from zk_tools.logging_handle import logger
from zk_tools.config_handle import config

from time import sleep

# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
MODULE_LOGGER_HEAD = "webhook_manager -> "
APP_VERSION = "v1.0.5"


# ------------------------------------------------------- #
#                   global variables
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #
def setup_logging(level):
    logger.set_logging_level(level)
    logger.set_cmd_line_logging_output()


def discord_alert(host_name):
    logger.warning(MODULE_LOGGER_HEAD + "Alert! USV OFFLINE!")

    url = config.get_element("general", "discord_webhook")

    embed = {
        "description": "Host {} offline!".format(host_name),
        "title": "ALERT! USV offline!"
    }

    data = {
        "content": "Input for {} dropped under 200V!".format(host_name),
        "username": "{}".format(config.get_element("general", "discord_username")),
        "embeds": [
            embed
        ],
    }

    response = requests.post(url, json=data)
    if 200 <= response.status_code < 300:
        logger.debug(MODULE_LOGGER_HEAD + f"Webhook sent {response.status_code}")
        sleep(10)
    else:
        logger.debug(MODULE_LOGGER_HEAD + f"Not sent with {response.status_code}, response:\n{response.json()}")
        sleep(10)


def gotify_alert(host_name):
    api_token = config.get_element("general", "gotify_token")
    gotify_url = config.get_element("general", "gotify_url")
    gotify_port = config.get_element("general", "gotify_port")

    response = requests.post('{}:{}/message?token={}'.format(gotify_url, gotify_port, api_token), json={
        "message": "USV {} OFFLINE.".format(host_name),
        "priority": 2,
        "title": "USV OFFLINE"
    })
    if 200 <= response.status_code < 300:
        logger.debug(MODULE_LOGGER_HEAD + f"Alert sent {response.status_code}")
        sleep(10)
    else:
        logger.debug(MODULE_LOGGER_HEAD + f"Not sent with {response.status_code}, response:\n{response.json()}")
        sleep(10)

# ------------------------------------------------------- #
#                      classes
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                       main
# ------------------------------------------------------- #
if __name__ == "__main__":
    config.load_config("../../config/snmp.yml")
    config.set_element("general", "version", APP_VERSION)
    setup_logging(config.get_element("general", "debug_level"))

    logger.debug("Sending Discord Alert...")
    discord_alert("TEST-MESSAGE")
    logger.debug("Sending Gotify Alert...")
    gotify_alert("Test-MSG")
    exit()
