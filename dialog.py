from userdata import read_user_data, dump_user_data
from getpass import getpass


main = """
1 - Сделать образ сети
2 - Построить топологию сети
3 - Запрос параметров устройства
4 - Настройки программы
0 - Выход из программы\n
"""

select_snapshot = """
1 - Создать новый образ сети 
2 - Использовать последний образ сети (по умолчанию)
3 - Выбрать образ сети из журнала\n
"""
csv_columns = "Device ID;IP address;Software;Version\n"
connections_columns = "Device A IP;Device A ID;Device A Port;Device B IP; Device B ID;Device B Port\n"


def net_access_user_data():
    user_data_ip, user_data_flag = read_user_data()
    if user_data_ip:
        use_old_data = input('Использовать последние данные для входа в сеть?(Д/н): ') != 'н'
    else:
        use_old_data = False

    if use_old_data:
        outer_ip, outer_login, outer_password, _ = user_data_flag['_outer']
        entry_ip, entry_login, entry_password, _ = user_data_flag['_entry']
        
    else:
        print('Данные входа во внешнюю машину')
        outer_ip = input('ip: ')
        outer_login = input('login: ')
        outer_password = getpass('password: ')
        print('Данные входа в машину в сети')
        entry_ip = input('ip: ')
        entry_login = input('login: ')
        entry_password = getpass('password: ')


        dump_data = {
            outer_ip: (outer_ip, outer_login, outer_password, '_outer'),
            entry_ip: (entry_ip, entry_login, entry_password, '_entry')
        }
        dump_user_data(dump_data)
        print('Данные для входа сохранены')

    return {
            'outer': (outer_ip, outer_login, outer_password),
            'entry': (entry_ip, entry_login, entry_password)
        }
