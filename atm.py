from customer import Customer
import dbMethod


class ATM(Customer):
    def __init__(self, id: str):
        user_id, name, pin, balance, type = dbMethod.get_user(id)
        super().__init__(user_id, name, pin, balance, type)

    @property
    def formatted_balance(self):
        return "Saldo Anda adalah Rp {:,}".format(self.balance)

    def withdraw(self, amount: int):
        if self.balance < amount:
            print("Saldo Anda tidak mencukupi untuk penarikan tunai.")
            return

        self.balance -= amount
        dbMethod.update_balance(self.balance, self.id)
        dbMethod.insert_transactions(self.id, amount, "withdraw")
        print("Penarikan uang sebesar Rp {:,} berhasil.".format(amount))

    def deposit(self, amount: int):
        self.balance += amount
        dbMethod.update_balance(self.balance, self.id)
        dbMethod.insert_transactions(self.id, amount, "deposit")
        print("Setoran uang sebesar Rp {:,} berhasil.".format(amount))

    def change_pin(self, new_pin: str):
        if len(new_pin) != 6:
            print("PIN harus berjumlah 6-digit.")
            return

        self.pin = new_pin
        dbMethod.update_pin(new_pin, self.id)
        print("Penggantian PIN berhasil.")

    def transfer(self, target_id: str, transfer_value: int):
        if not dbMethod.in_data(target_id):
            print("ID yang ingin di transfer tidak dapat ditemukan.")
            return

        if self.id == target_id:
            print("Tidak dapat transfer ke diri sendiri.")
            return

        if self.balance < transfer_value:
            print("Saldo Anda tidak mencukupi untuk transfer.")
            return

        self.balance -= transfer_value
        balance_target = dbMethod.get_balance(target_id) + transfer_value

        dbMethod.update_balance(self.balance, self.id)
        dbMethod.update_balance(balance_target, target_id)
        dbMethod.insert_transactions(self.id, transfer_value,
                                     "transfer", target_id=target_id)
        print("Transfer uang sebesar Rp {:,} berhasil.".format(transfer_value))

    def transaction_history(self):
        transactions = dbMethod.get_transactions(self.id)
        
        if not bool(transactions):  # check if empty
            print("Tidak ada riwayat transaksi.")
            return

        columns = ["Jumlah", "Deskripsi", "Tanggal"]
        mxLengths = []
        sep = "+"

        for i in range(len(columns)):
            transaction = max(transactions, key=lambda x: x[i])
            dataLength = len(str(transaction[i]))

            if dataLength > len(columns[i]):
                maxLength = dataLength
            else:
                maxLength = len(columns[i])

            mxLengths.append(maxLength)
            sep += "-" * (maxLength + 2) + "+"

        print(sep)

        for i, column in enumerate(columns):
            print(f"| {column.ljust(mxLengths[i])} ", end='')

        print('|')
        print(sep)

        for transaction in transactions:
            for i, item in enumerate(transaction):
                print(f"| {str(item).ljust(mxLengths[i])} ", end='')
            print('|')

        print(sep)


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

    print("\nSelamat datang, %s." % user.name)

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
            user.transaction_history()
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
