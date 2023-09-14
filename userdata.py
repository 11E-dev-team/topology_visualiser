from cryptography.fernet import Fernet
from os.path import isfile


def get_key():
    from generate_key import regenerate_key
    if not isfile('.secret_key'):
        regenerate_key()
    with open('.secret_key', mode='rb') as key:
        return key.read()

USERS_FILE = 'users.csv'


def add_user_data(ip: str, login: str, password: str, flag: str = '-'):
    with open(USERS_FILE, mode='a') as uf:
        data = f'{ip};{login};{password};{flag}'
        uf.write(Fernet(get_key()).encrypt(data.encode()).decode()+'\n')


def read_user_data():
    data_by_ip, data_by_flag = {}, {}
    header = True
    fn = Fernet(get_key())
    if not isfile(USERS_FILE):
        with open(USERS_FILE, mode='w') as uf:
            uf.write('ip;login;password;flag\n')
    with open(USERS_FILE, mode='r') as uf:
        for line in uf.readlines():
            if header: 
                header = False
                continue
            line = fn.decrypt(line.encode()).decode()
            line = line.strip('\n')
            ip, login, password, flag = line.split(';')
            data_by_ip[ip] = data_by_flag[flag] = [ip, login, password, flag]
    print(data_by_flag)
    return data_by_ip, data_by_flag


def dump_user_data(data):
    with open(USERS_FILE, mode='w') as uf:
        uf.write('ip;login;password;flag\n')
        for ip, userdata in data.items():
            _, login, password, flag = userdata
            data = f'{ip};{login};{password};{flag}'
            uf.write(Fernet(get_key()).encrypt(data.encode()).decode()+'\n')
