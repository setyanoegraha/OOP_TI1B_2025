# File: modul.py
class HP:
    def __init__(self, merk, model, harga, stok):
        self.merk = merk
        self.model = model
        self.harga = harga
        self.stok = stok

    def tampilkan_info(self):
        """Menampilkan informasi HP."""
        return f"{self.merk} {self.model} - Rp {self.harga} (Stok: {self.stok})"

    def kurangi_stok(self, jumlah):
        """Mengurangi stok HP jika stok mencukupi."""
        if self.stok >= jumlah:
            self.stok -= jumlah
            return True
        return False


class Transaksi:
    def __init__(self):
        self.keranjang = []

    def tambah_ke_keranjang(self, hp, jumlah):
        """Menambahkan HP ke keranjang belanja."""
        if hp.kurangi_stok(jumlah):
            self.keranjang.append((hp, jumlah))
            print(f"{jumlah} {hp.merk} {hp.model} ditambahkan ke keranjang.")
        else:
            print("Stok tidak mencukupi!")

    def hitung_total(self):
        """Menghitung total harga belanja."""
        return sum(hp.harga * jumlah for hp, jumlah in self.keranjang)

    def checkout(self):
        """Menyelesaikan transaksi."""
        if not self.keranjang:
            print("Keranjang kosong. Tidak ada transaksi.")
            return

        total = self.hitung_total()
        print("\n--- Detail Pembelian ---")
        for hp, jumlah in self.keranjang:
            print(f"{hp.merk} {hp.model} - {jumlah} unit - Rp {hp.harga * jumlah}")
        print(f"Total pembayaran: Rp {total}")
        print("Terima kasih telah berbelanja!")
        self.keranjang.clear()

