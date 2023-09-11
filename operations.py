import pexpect
import re

def start_telnet (ip:str, port:str):
    print (f"Подключение к {ip} {port}...")
    pxp = pexpect.spawn (f"telnet {ip} {port}")
    pxp.expect("Escape")
    pxp.sendline("\n")
    result = pxp.expect([".*>", ".*#", pexpect.TIMEOUT])
    if result == -1:
        print ("TIMEOUT")
    else:
        print (f"Подключен к {ip} {port}")
    if result == 0:
        enter_privileged_mode(pxp)
    pxp.sendline("terminal length 0")
    pxp.expect([".*>", ".*#"])
    print ("Включен режим полного вывода")
    return pxp
    
def enter_privileged_mode(pxp:pexpect.spawn):
    print ("Вход в привелигированный режим...")
    pxp.sendline("enable")
    result = pxp.expect([".*#", "Password"])
    match result:
        case 0:
            pass
        case 1:
            pxp.sendline("cisco")
            pxp.expect(".*#")

    print ("Accesed")

def get_neig_data(pxp:pexpect.spawn):
    print ("Получение данныx с устройства...")
    pxp.sendline("show cdp neig det")
    pxp.expect("Total cdp entries displayed : ")
    data = pxp.before.decode("utf-8")
    print ("Данные полученны")
    return data

class DeviceInfo:
    ip_address: str
    device_id: str
    interface: str
    port_id: str

    software: str
    version: str

def match_neighbors (data):
    print ("Поиск соседей...")
    neighbors = []
    return neighbors