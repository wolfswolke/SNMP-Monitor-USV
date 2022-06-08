"""

"""
# ------------------------------------------------------- #
#                     imports
# ------------------------------------------------------- #

from gutils.config_handle import config
from gutils.logging_handle import logger
from logic.snmp_query import snmp_input_state
from logic.discord_webhook import alert as discord_alert

from time import sleep

# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
APP_VERSION = "v1.0.4"
MODULE_LOGGER_HEAD = "start_app -> "


# ------------------------------------------------------- #
#                   global variables
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #
def setup_logging(level):
    logger.set_logging_level(level)
    logger.set_cmd_line_logging_output()


# ------------------------------------------------------- #
#                      classes
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                       main
# ------------------------------------------------------- #

if __name__ == "__main__":
    try:
        config.load_config("../config/snmp.yml")
        config.set_element("general", "version", APP_VERSION)
        setup_logging(config.get_element("general", "debug_level"))

        logger.info("-----------------------------------------------------------")
        logger.info("            SNMP Monitor Started {}".format(APP_VERSION))
        logger.info("-----------------------------------------------------------")

        clients = config.get_element("clients")
        snmp_password = config.get_element("general", "snmp_password")
        timeout = config.get_element("general", "check_cycle_in_minutes")

        while True:
            for dict_key, dict_value in clients.items():
                ip = str(dict_key)
                hostname = str(dict_value["hostname"])
                snmp_result = snmp_input_state(ip, snmp_password)
                logger.debug(MODULE_LOGGER_HEAD + "Voltage: " f"{snmp_result}")

                if snmp_result < 200:
                    if bool(dict_value["offline"]) is False:
                        logger.debug(MODULE_LOGGER_HEAD + "Sending Alert and marking Device as Offline.")
                        discord_alert(hostname)
                        dict_value["offline"] = True
                    else:
                        logger.debug(MODULE_LOGGER_HEAD + "Device Still offline")

                else:
                    dict_value["offline"] = False
                    logger.debug(MODULE_LOGGER_HEAD + "Is back online!")

            logger.info("Finished Check. Going to Sleep...")
            sleep(timeout * 60)

    except KeyboardInterrupt:
        logger.info("-----------------------------------------------------------")
        logger.info("            SNMP Monitor Stopped.")
        logger.info("-----------------------------------------------------------")
