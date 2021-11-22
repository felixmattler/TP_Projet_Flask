from pysnmp.hlapi import *
from datetime import datetime


def snmpget(ip, oid_list):
    result_list=[]
    # oid_list=oid_chain.split(',')
    for oid in oid_list:

        iterator = nextCmd(
            SnmpEngine(),
            CommunityData('passprojet', mpModel=0),
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
        log = open("./templates/module_logs/logfile.txt", "a")
        log.write(log_string + "\n")
        log.close()
        
        result_list.append(snmp_result)

    return result_list
