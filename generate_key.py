from cryptography.fernet import Fernet


def regenerate_key():
    with open('.secret_key', mode='wb') as key:
        key.write(Fernet.generate_key())


if __name__ == '__main__':

    sure = input('Вы уверены, что вы хотите перегенерировать ключ шифрации данных? (д/Н): ') == 'д'
    if sure:
        regenerate_key()
        print('Сгенерирован новый ключ')
