"""

"""
# ------------------------------------------------------- #
#                     imports
# ------------------------------------------------------- #

from gutils.config_handle import config
from gutils.logging_handle import logger
from logic.snmp_query import snmp_input_state, snmp_hostname
from logic.discord_webhook import alert as discord_alert

from time import sleep

# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
APP_VERSION = "v1.0.0"
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

        clients = dict(config.get_element("clients")).items()
        snmp_password = config.get_element("general", "snmp_password")
        timeout = config.get_element("general", "check_cycle_in_minutes")

        while True:
            for client in clients:
                ip, hostname = client
                snmp_result = snmp_input_state(ip, snmp_password)
                logger.debug(MODULE_LOGGER_HEAD + "Voltage: " f"{snmp_result}")
                if snmp_result < 200:
                    discord_alert(hostname)
            logger.info("Finished Check. Going to Sleep...")
            sleep(timeout*60)

    except KeyboardInterrupt:
        logger.info("-----------------------------------------------------------")
        logger.info("            SNMP Monitor Stopped.")
        logger.info("-----------------------------------------------------------")
