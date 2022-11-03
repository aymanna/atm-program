from customer import Customer
import dbMethod


class ATM(Customer):
    def __init__(self, id: str):
        user_id, name, pin, balance, type = dbMethod.get_user(id)
        super().__init__(user_id, name, pin, balance, type)

    @property
    def formatted_balance(self):
        return f"Saldo Anda adalah Rp {self.balance:,}"

    def withdraw(self, amount: int):
        if self.balance < amount:
            print("Saldo Anda tidak mencukupi untuk penarikan tunai.")
            return

        self.balance -= amount
        dbMethod.update_balance(self.balance, self.id)
        dbMethod.insert_transactions(self.id, amount, "withdraw")
        print(f"Penarikan uang sebesar Rp {amount:,} berhasil.")

    def deposit(self, amount: int):
        self.balance += amount
        dbMethod.update_balance(self.balance, self.id)
        dbMethod.insert_transactions(self.id, amount, "deposit")
        print(f"Setoran uang sebesar Rp {amount:,} berhasil.")

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

        target_name = dbMethod.get_user(target_id)[1]
        self.balance -= transfer_value
        balance_target = dbMethod.get_balance(target_id) + transfer_value

        dbMethod.update_balance(self.balance, self.id)
        dbMethod.update_balance(balance_target, target_id)
        dbMethod.insert_transactions(self.id, transfer_value,
                                     "transfer", target_id=target_id)
        dbMethod.insert_transactions(target_id, transfer_value,
                                     "recieve", target_id=self.id)

        print(f"Transfer uang ke {target_name} sebesar Rp {transfer_value:,} berhasil.")

    def transaction_history(self):
        transactions = dbMethod.get_transactions(self.id)
        
        if not bool(transactions):  # check if empty
            print("Tidak ada riwayat transaksi.")
            return

        columns = ["Jumlah", "Deskripsi", "Tanggal"]
        max_col_lengths = []
        sep = "+"

        for i in range(len(columns)):
            mx_transaction = max(transactions, key=lambda x: x[i])
            data_length = len(str(mx_transaction[i]))

            if data_length > len(columns[i]):
                max_col_length = data_length
            else:
                max_col_length = len(columns[i])

            max_col_lengths.append(max_col_length)
            sep += "-" * (max_col_length + 2) + "+"

        print(sep)

        for i, column in enumerate(columns):
            print(f"| {column.ljust(max_col_lengths[i])} ", end='')

        print('|')
        print(sep)

        for mx_transaction in transactions:
            for i, item in enumerate(mx_transaction):
                print(f"| {str(item).ljust(max_col_lengths[i])} ", end='')
            print('|')

        print(sep)
