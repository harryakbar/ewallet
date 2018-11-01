import requests

URL = 'http://127.0.0.1:80'
def main():
    main_menu()
    while True:
        user_input = str(raw_input('Masukkan perintah (nomor saja, cth. 1): '))
        if user_input == '1':
            getSaldo()
        elif user_input == '2':
            getTotalSaldo()
        elif user_input == '3':
            transfer()
        elif user_input == '4':
            register()
        elif user_input == 'q':
            return
        else:
            print("Input tidak dikenal, masukkan input berikut:")
            main_menu()

def getSaldo():
    user_id = str(raw_input('Masukkan user_id (nomor saja, cth. 1506689080): '))
    try:
        r = requests.post('{}/ewallet/getSaldo'.format(URL), json={"user_id": user_id})
        if r.json()['saldo'] == -1:
            print("User belum terdaftar, register dulu")
            register()
        else:
            print(r.text)
    except Exception:
        print(Exception)

def getTotalSaldo():
    user_id = str(raw_input('Masukkan user_id (nomor saja, cth. 1506689080): '))
    try:
        r = requests.post('{}/ewallet/getTotalSaldo'.format(URL), json={"user_id": user_id})
        print(r.text)
    except Exception:
        print(Exception)

def transfer():
    user_id = str(raw_input('Masukkan user_id (nomor saja, cth. 1506689080): '))
    nilai = int(raw_input('Masukkan nilai yang ingin ditransfer (nomor saja, cth. 100): '))
    try:
        r = requests.post('{}/ewallet/transfer'.format(URL), json={"user_id": user_id, "nilai": nilai})
        print(r.text)
    except Exception:
        print(Exception)

def register():
    user_id = str(raw_input('Masukkan user_id (nomor saja, cth. 1506689080): '))
    nama = str(raw_input('Masukkan nama (nomor saja, cth. harry): '))
    try:
        r = requests.post('{}/ewallet/register'.format(URL), json={"user_id": user_id, "nama": nama})
        print(r.text)
    except Exception:
        print(Exception)

def main_menu():
    print("Menu:")
    print("[1] GetSaldo")
    print("[2] GetTotalSaldo")
    print("[3] Transfer")
    print("[4] Register")
    print(">>>>>>>>>>>>>>>>>>")

if __name__ == '__main__':
    main()