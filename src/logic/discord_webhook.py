"""

"""
# ------------------------------------------------------- #
#                     imports
# ------------------------------------------------------- #
import requests
from gutils.logging_handle import logger
from gutils.config_handle import config

from time import sleep

# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
MODULE_LOGGER_HEAD = "discord_webhook -> "
APP_VERSION = "v1.0.4"


# ------------------------------------------------------- #
#                   global variables
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #
def setup_logging(level):
    logger.set_logging_level(level)
    logger.set_cmd_line_logging_output()


def alert(host_name):
    logger.warning(MODULE_LOGGER_HEAD + "Alert! USV OFFLINE!")

    url = config.get_element("general", "discord_webhook")

    embed = {
        "description": "Host {} offline!".format(host_name),
        "title": "ALERT! USV offline!"
    }

    data = {
        "content": "Input for {} dropped under 200V!".format(host_name),
        "username": "GW-Uptime-USV",
        "embeds": [
            embed
        ],
    }

    result = requests.post(url, json=data)
    if 200 <= result.status_code < 300:
        logger.debug(MODULE_LOGGER_HEAD + f"Webhook sent {result.status_code}")
        sleep(10)
    else:
        logger.debug(MODULE_LOGGER_HEAD + f"Not sent with {result.status_code}, response:\n{result.json()}")
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

    alert("TEST-MESSAGE")
    exit()
