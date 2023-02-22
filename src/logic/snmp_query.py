"""

"""
# ------------------------------------------------------- #
#                     imports
# ------------------------------------------------------- #
import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen
from zk_tools.logging_handle import logger

# ------------------------------------------------------- #
#                   definitions
# ------------------------------------------------------- #
MODULE_LOGGER_HEAD = "snmp_query -> "


# ------------------------------------------------------- #
#                   global variables
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                      functions
# ------------------------------------------------------- #
def snmp_input_state(host, community):
    logger.debug(MODULE_LOGGER_HEAD + "Entered snmp_input_state in snmp_query")
    oid = '1.3.6.1.2.1.33.1.3.3.1.3.1'
    error_indication, error_status, error_index, var_snmp = cmdgen.CommandGenerator().getCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget((host, 161)),
        cmdgen.MibVariable(oid),
        lookupMib=False,
    )
    if error_indication:
        logger.debug(MODULE_LOGGER_HEAD + "Entered Error indication. Val set to 1")
        logger.debug(MODULE_LOGGER_HEAD + "Returning Value for IP: {}".format(host))
        return int(1)
    for oid, val in var_snmp:
        return_value = int(val)
        return return_value


# ------------------------------------------------------- #
#                      classes
# ------------------------------------------------------- #


# ------------------------------------------------------- #
#                       main
# ------------------------------------------------------- #
if __name__ == "__main__":
    print(snmp_input_state("111.111.111.111", "public"))
