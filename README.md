# SNMP-Monitor-USV
USV Monitoring Utility which sends a Discord message if a USVs Input Voltage drops to low.
This Application Can for instance be deployed in a Docker container and monitor all USVs in a Organisation.
How to use:
* 1. Clone the Repo
* 2. Rename the config/snmp_example.yml to snmp.yml
* 3. Add all your SNMP Hosts. Imput the SNMP Password and webhook url aswell!
* 4. Install the Requirments. GUtils is something i wrote to make my life eayser. 

TO-DO:
* Add Influx DB Support to show Offline Status and Voltages.
* Add check to show if alert has already been sent for a Device so you wont get alerted multiple times.
