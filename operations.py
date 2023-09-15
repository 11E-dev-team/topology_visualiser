from config import expect_lib

import re
import time
import settings
from prints import log_print


def start_ssh(ip: str, login: str, password: str, pxp: expect_lib.spawn | None = None, max_reconnections: int = 10) -> expect_lib.spawn:
    if pxp is None:
        pxp = expect_lib.spawn(f"ssh {login}@{ip}", timeout=10)
    else:
        pxp.expect("$")
        log_print("На базовом устройстве", level=1)
        log_print("Подключение по ssh внутрь сети", level=1)
        pxp.sendline(f"ssh {login}@{ip}")
    reconections = 0
    result = 2
    while (result == 2) or (reconections > max_reconnections):
        reconections += 1
        log_print(f"Попытка подключения {reconections}/{max_reconnections}", level=0)
        time.sleep(reconections * 5)
        result = pxp.expect(["password:", "(yes/no)", expect_lib.TIMEOUT])
    if reconections > max_reconnections:
        log_print("Попытка подключения не удалась", level=0)
    if result == 1:
        pxp.sendline("yes")
    pxp.sendline(f"{password}")
    pxp.sendline("terminal length 0")
    return pxp


def enter_privileged_mode(pxp: expect_lib.spawn):
    log_print("Вход в привелигированный режим...", level=0)
    pxp.sendline("enable")
    result = pxp.expect([".*#", "Password"])
    match result:
        case 0:
            pass
        case 1:
            pxp.sendline("cisco")
            pxp.expect(".*#")

    log_print("Допущен", level=0)


def get_neig_data(pxp: expect_lib.spawn, max_reconnections: int = 10) -> str:
    log_print("Получение данныx с устройства...", level=1)
    pxp.sendline("terminal length 0")
    pxp.sendline("show cdp neig det")
    result = pxp.expect(["--.+$", expect_lib.TIMEOUT], re.DOTALL)
    reconections = 2
    while (result == 1) or (reconections > max_reconnections):
        log_print(f"Попытка подключения {reconections}/{max_reconnections}", level=0)
        time.sleep(reconections)
        result = pxp.expect(["--.+$", expect_lib.TIMEOUT], re.DOTALL)
        reconections += 1
    if reconections > max_reconnections:
        log_print("Попытка подключения не удалась", level=0)
    if result == 0:
        data = pxp.after
        log_print("Данные полученны", level=1)
    return data


def parse_neighbors(output: str) -> dict:
    matches = []
    for block in output.split("-------------------------"):
        match = re.search(
            r"Device ID ?: ?(?P<device_id>\w+)"
            r".+IP address ?: ?(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            r".+Interface ?: ?(?P<interface>\S+),"
            r".+Port ID \(outgoing port\) ?: ?(?P<port_id>\S+)"
            r".+Software \((?P<software>\S+)\)"
            r".+Version (?P<version>.+?)(,\s|$)$",
            block,
            re.DOTALL | re.MULTILINE,
        )
        if match:
            matches.append(match.groupdict())
    return matches


def roam_net(pxp: expect_lib.spawn, entry_ip: str, username: str, password: str, send_connections=False, 
             connections_buffer: list=None, devices_buffer: list=None):
    log_print(f'Подключение к {username}@{entry_ip}', level=0)
    start_ssh(ip=entry_ip, login=username, password=password, pxp=pxp, 
              max_reconnections=int(settings.get_setting('reconnect')))
    stack = parse_neighbors(get_neig_data(pxp))
    visited = [entry_ip]
    log_print('Анализ сети', level=1)
    pxp.sendline('exit')
    has_added_entry_point = False
    while stack:
        device = stack.pop(0)
        if device["ip"] in visited:
            if device["ip"] == entry_ip:
                if not send_connections:
                    yield device
            continue
        log_print(f'Подключение к {username}@{device["ip"]}', level=0)
        start_ssh(ip=device['ip'], login=username, password=password, pxp=pxp,
                  max_reconnections=int(settings.get_setting('reconnect')))
        log_print('Подключено. Получение данных о соседях', level=1)
        neighs = parse_neighbors(get_neig_data(pxp))
        log_print('Обнаружено', len(neighs), 'соседей', level=1)
        for neigh in neighs:
            if neigh['ip'] == entry_ip and not has_added_entry_point:
                has_added_entry_point = True
                stack.append(neigh)
            elif neigh['ip'] not in visited:
                stack.append(neigh)

            if send_connections:
                yield ((device["ip"], device["device_id"], neigh["port_id"]), 
                        (neigh["ip"], neigh["device_id"], neigh["interface"]))
            if connections_buffer is not None:
                connections_buffer.append(
                    ((device["ip"], device["device_id"], neigh["port_id"]), 
                        (neigh["ip"], neigh["device_id"], neigh["interface"]))
                )
        visited.append(device['ip'])
        log_print('| stack:', [dev['ip'] for dev in stack], level=2)
        log_print('| visited:', visited, level=2)
        if not send_connections:
            yield device
        if devices_buffer is not None:
            devices_buffer.append(device)
        log_print('Возврат к внешней машине', level=1)
        pxp.sendline('exit')
