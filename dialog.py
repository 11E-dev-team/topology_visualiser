from userdata import read_user_data, add_user_data
from getpass import getpass


main = """
1 - Инициализировать сеть
2 - Построить топологию сети
3 - Запрос параметров устройства
4 - Выполнить команды в 
конфигурационном устройстве
5 - Выполнить команды и заисать их вывод
0 - Выход из программы\n
"""

init = """
1 - инициализировать сеть 
2 - Использовать последний снапшот
3 - Выбрать снапшот\n
"""
csv_columns = "Device ID,IP address,Platform,Capabilities,Interface,Port ID,Version,Technicalsupport,Advertisment version,IP address"


def net_access_user_data():
    user_data_ip, user_data_flag = read_user_data()
    if user_data_ip:
        use_old_data = input('Использовать последние данные для входа в сеть?(Д/н): ') != 'н'
    else:
        use_old_data = False
    
   # print(user_data_flag)
   # print(user_data_ip)

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

        add_user_data(outer_ip, outer_login, outer_password, '_outer')
        add_user_data(entry_ip, entry_login, entry_password, '_entry')
        print('Данные для входа сохранены')

    return {
            'outer': (outer_ip, outer_login, outer_password),
            'entry': (entry_ip, entry_login, entry_password)
        }
