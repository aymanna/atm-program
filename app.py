import dbMethod
from atm import ATM


def main():

    print("Selamat datang di ATM A. Silahkan masukkan ID Anda.\n")

    id_input = input("input ID: ")
    while not dbMethod.in_data(id_input):
        print("ID yang Anda masukkan tidak berlaku. Silahkan coba kembali.\n")
        id_input = input("input ID: ")

    pin_input = input("input PIN: ")
    while not dbMethod.true_user(id_input, pin_input):
        print("PIN yang Anda masukkan salah. Silahkan coba kembali.\n")
        pin_input = input("input PIN: ")

    user = ATM(id_input)

    menus = [
        "Cek Saldo",
        "Setor Tunai",
        "Tarik Tunai",
        "Transfer",
        "Riwayat Transaksi",
        "Keluar",
    ]

    print(f"\nSelamat datang, {user.name}.")

    while True:

        print("\nSilahkan pilih menu di bawah ini.")
        for i, menu in enumerate(menus):
            print("[%d] %s" % (i + 1, menu))
        print()

        menu_input = input("Pilihan menu: ")

        if menu_input == '1':
            print(user.formatted_balance)
            continue

        elif menu_input == '2':
            try:
                amount = int(input("\nMasukkan jumlah setoran: "))
            except:
                print("Setoran tunai gagal.")
            else:
                if amount <= 0:
                    print("Setoran tunai gagal.")
                    continue
                user.deposit(amount)
            continue

        elif menu_input == '3':
            try:
                amount = int(input("\nMasukkan jumlah penarikan: "))
            except:
                print("Penarikan tunai gagal.")
            else:
                if amount <= 0:
                    print("Penarikan tunai gagal.")
                    continue
                user.withdraw(amount)
            continue

        elif menu_input == '4':
            transfer_id = input("\nMasukkan ID yang ingin ditransfer: ")

            try:
                amount = int(input("Masukkan jumlah transfer: "))
            except:
                print("Transfer gagal.")
            else:
                if amount <= 0:
                    print("Transfer gagal.")
                    continue
                print()
                user.transfer(transfer_id, amount)
            continue

        elif menu_input == '5':
            print()
            print(user.transaction_history)
            continue

        elif menu_input == '6':
            print("\nTerima kasih telah menggunakan ATM A, %s." % user.name)
            print("Selamat Tinggal!")
            break

        else:
            print()
            continue


if __name__ == '__main__':
    main()
