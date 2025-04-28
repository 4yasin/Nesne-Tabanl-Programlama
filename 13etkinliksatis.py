import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget,
    QLineEdit, QHBoxLayout, QMessageBox, QInputDialog
)


class Bilet:
    bilet_sayac = 1
    def __init__(self, etkinlik, kullanici):
        self.bilet_no = Bilet.bilet_sayac
        Bilet.bilet_sayac += 1
        self.etkinlik = etkinlik
        self.kullanici = kullanici
    def __str__(self):
        return f"Bilet #{self.bilet_no} - {self.etkinlik.ad} ({self.etkinlik.tarih})"

class Etkinlik:
    def __init__(self, ad, tarih, mekan, kontenjan):
        self.ad = ad
        self.tarih = tarih
        self.mekan = mekan
        self.kontenjan = kontenjan
        self.satilan_biletler = []
    def bilet_sat(self, kullanici):
        if len(self.satilan_biletler) < self.kontenjan:
            bilet = Bilet(self, kullanici)
            self.satilan_biletler.append(bilet)
            kullanici.bilet_al(bilet)
            return bilet
        else:
            return None
    def __str__(self):
        return f"{self.ad} - {self.tarih} - {self.mekan} (Kalan: {self.kontenjan - len(self.satilan_biletler)})"

class Kullanici:
    def __init__(self, ad):
        self.ad = ad
        self.biletler = []
    def bilet_al(self, bilet):
        self.biletler.append(bilet)
    def __str__(self):
        return self.ad

# --- PyQt5 Arayüzü ---
class EtkinlikBiletUygulamasi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Etkinlik ve Bilet Satış Platformu")
        self.etkinlikler = []
        self.kullanici = Kullanici("Kullanıcı1")  # Basitlik için tek kullanıcı
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Etkinlikler:"))
        self.etkinlik_list = QListWidget()
        layout.addWidget(self.etkinlik_list)

        
        etkinlik_ekle_layout = QHBoxLayout()
        self.etkinlik_ad_input = QLineEdit()
        self.etkinlik_ad_input.setPlaceholderText("Etkinlik adı")
        self.etkinlik_tarih_input = QLineEdit()
        self.etkinlik_tarih_input.setPlaceholderText("Tarih (GG/AA/YYYY)")
        self.etkinlik_mekan_input = QLineEdit()
        self.etkinlik_mekan_input.setPlaceholderText("Mekan")
        self.etkinlik_kontenjan_input = QLineEdit()
        self.etkinlik_kontenjan_input.setPlaceholderText("Kontenjan")
        etkinlik_ekle_btn = QPushButton("Etkinlik Ekle")
        etkinlik_ekle_btn.clicked.connect(self.etkinlik_ekle)
        etkinlik_ekle_layout.addWidget(self.etkinlik_ad_input)
        etkinlik_ekle_layout.addWidget(self.etkinlik_tarih_input)
        etkinlik_ekle_layout.addWidget(self.etkinlik_mekan_input)
        etkinlik_ekle_layout.addWidget(self.etkinlik_kontenjan_input)
        etkinlik_ekle_layout.addWidget(etkinlik_ekle_btn)
        layout.addLayout(etkinlik_ekle_layout)

      
        bilet_al_btn = QPushButton("Seçili Etkinliğe Bilet Al")
        bilet_al_btn.clicked.connect(self.bilet_al)
        layout.addWidget(bilet_al_btn)

        
        layout.addWidget(QLabel("Aldığım Biletler:"))
        self.bilet_list = QListWidget()
        layout.addWidget(self.bilet_list)

        self.setLayout(layout)

    def etkinlik_ekle(self):
        ad = self.etkinlik_ad_input.text().strip()
        tarih = self.etkinlik_tarih_input.text().strip()
        mekan = self.etkinlik_mekan_input.text().strip()
        kontenjan = self.etkinlik_kontenjan_input.text().strip()
        if ad and tarih and mekan and kontenjan.isdigit():
            etkinlik = Etkinlik(ad, tarih, mekan, int(kontenjan))
            self.etkinlikler.append(etkinlik)
            self.etkinlik_list.addItem(str(etkinlik))
            self.etkinlik_ad_input.clear()
            self.etkinlik_tarih_input.clear()
            self.etkinlik_mekan_input.clear()
            self.etkinlik_kontenjan_input.clear()
        else:
            QMessageBox.warning(self, "Uyarı", "Tüm alanları doldurun ve kontenjanı sayı olarak girin!")

    def bilet_al(self):
        index = self.etkinlik_list.currentRow()
        if index < 0:
            QMessageBox.warning(self, "Uyarı", "Önce bir etkinlik seçin!")
            return
        etkinlik = self.etkinlikler[index]
        bilet = etkinlik.bilet_sat(self.kullanici)
        if bilet:
            self.bilet_list.addItem(str(bilet))
            self.etkinlik_list.item(index).setText(str(etkinlik))  
        else:
            QMessageBox.warning(self, "Uyarı", "Bu etkinlikte bilet kalmadı!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = EtkinlikBiletUygulamasi()
    pencere.show()
    sys.exit(app.exec_())