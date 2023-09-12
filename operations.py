from config import expect_lib

# from pexpect import popen_spawn
import re


class DeviceInfo:
    ip_address: str
    device_id: str
    interface: str
    port_id: str

    software: str
    version: str

def start_telnet(ip: str, port: str):
    print(f"Подключение к {ip} {port}...")
    pxp = expect_lib.spawn(f"telnet {ip} {port}")
    # pxp.expect("Escape")
    pxp.sendline("\n")
    result = pxp.expect([".*>", ".*#", expect_lib.TIMEOUT])
    if result == -1:
        print("TIMEOUT")
    else:
        print(f"Подключен к {ip} {port}")
    if result == 0:
        enter_privileged_mode(pxp)
    pxp.sendline("terminal length 0")
    pxp.expect([".*>", ".*#"])
    print("Включен режим полного вывода")
    return pxp


def enter_privileged_mode(pxp: expect_lib.spawn):
    print("Вход в привелигированный режим...")
    pxp.sendline("enable")
    result = pxp.expect([".*#", "Password"])
    match result:
        case 0:
            pass
        case 1:
            pxp.sendline("cisco")
            pxp.expect(".*#")

    print("Accesed")


def get_neig_data(pxp: expect_lib.spawn):
    print("Получение данныx с устройства...")
    pxp.sendline("show cdp neig det")
    pxp.expect("Total cdp entries displayed : ")
    data = pxp.before  # .decode("utf-8")
    # pxp.expect([".*>", ".*#"])
    print("Данные полученны")
    return data

def parse_neighbors(output: str):
    matches = []
    for block in output.split("-------------------------"):
        match = re.search(
            r"Device ID ?: ?(?P<device_id>\w+)"
            r".+IP address ?: ?(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            r".+Interface ?: ?(?P<interface>\S+)"
            r".+Port ID \(outgoing port\) ?: ?(?P<port_id>\S+)"
            r".+Software \((?P<software>\S+)\)"
            r".+Version (?P<version>.+?)(,\s|$)$",
            block,
            re.DOTALL | re.MULTILINE,
        )
        if match:
            matches.append(match.groupdict())
    return matches

def roam_net(pxp: expect_lib.spawn):
    enter_privileged_mode(pxp)
    stack = parse_neighbors(get_neig_data(pxp)) 
    while stack:
        pass





def match_neighbors(data):
    print("Поиск соседей...")
    neighbors = []
    return neighbors


def match_neighbours(data):
    return match_neighbors(data)

