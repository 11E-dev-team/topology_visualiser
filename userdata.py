USERS_FILE = 'users.csv'

def add_user_data(ip: str, login: str, password: str, flag: str = '-'):
    with open(USERS_FILE, mode='a') as uf:
        uf.write(f'{ip};{login};{password};{flag}'+'\n')

def read_user_data():
    data_by_ip, data_by_flag = {}, {}
    header = True
    with open(USERS_FILE, mode='r') as uf:
        for line in uf.readlines():
            if header: 
                header = False
                continue
            line = line.strip('\n')
            ip, login, password, flag = line.split(';')
            data_by_ip[ip] = data_by_flag[flag] = [ip, login, password, flag]
    return data_by_ip, data_by_flag

def dump_user_data(data):
    with open(USERS_FILE, mode='w') as uf:
        uf.write('ip;login;password;flag\n')
        for ip, userdata in data.items():
            _, login, password, flag = userdata
            uf.write(f'{ip};{login};{password};{flag}')