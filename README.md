# SNMP-Monitor-USV
USV Monitoring Utility which sends a Discord message if a USVs Input Voltage drops to low.
This Application Can for instance be deployed in a Docker container and monitor all USVs in a Organisation.
How to use:
* Clone the Repo
* Rename the config/snmp_example.yml to snmp.yml
* Add all your SNMP Hosts. Input the SNMP Password and webhook url aswell!
* Install the Requirments. 

TO-DO:
[] Add Influx DB Support to show Offline Status and Voltages.

[X] Add check to show if alert has already been sent for a Device so you wont get alerted multiple times.
