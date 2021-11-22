import json

from python_json.json_reader import *
from snmp_functions import *
import graph_functions

from pysnmp.hlapi import *
from datetime import datetime

import time



def snmpget(ip, oid):
    iterator = nextCmd(
        SnmpEngine(),
        CommunityData('passprojet', mpModel = 0),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(errorIndication)
        snmp_result = errorIndication
        type = "error_indication"

    elif errorStatus:
        #print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        snmp_result = ('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        type = "error_status"

    else:
        for varBind in varBinds:
            #print(' = '.join([x.prettyPrint() for x in varBind]))
            #snmp_result = (' = '.join([x.prettyPrint() for x in varBind]))
            snmp_result = (varBind.__getitem__(1))
        type = "info"   
 
    now = datetime.now()
    current_date = now.strftime("%d/%m/%Y")
    current_time = now.strftime("%H:%M:%S")
    log_string = f"{current_date};{current_time};{type};{ip};{oid};{snmp_result}"
    #log_string=str(current_time+";" + type +" ; "+ "IP : "+ip+" ; "+"OID : "+oid+" ; "+"Request : "+str(snmp_result))
    print(log_string)
    log = open("./templates/module_logs/BitRateFile.txt", "a")
    log.write(log_string + "\n")
    log.close()

data_ip="192.168.176.2"
data_oid="1.3.6.1.2.1.2.2.1.10"
frequency=10


#schedule.every(2).seconds.do(snmpget(data_ip, data_oid))


while True:
    snmpget(data_ip, data_oid)
    time.sleep(frequency)

