# Seyahat Planlama Uygulaması
# Seyahat rotalarının oluşturulması, konaklama seçeneklerinin yönetilmesi ve seyahat planlarının düzenlenmesi
# gibi temel işlevleri içeren bir seyahat planlama sistemidir. Kullanıcılar seyahat rotalarını oluşturabilir, 
# konaklama seçeneklerini seçebilir ve seyahat planlarını düzenleyebilir.



import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QLineEdit, QHBoxLayout, QMessageBox


class Konaklama:
    def __init__(self, ad, fiyat):
        self.ad = ad
        self.fiyat = fiyat
    def __str__(self):
        return f"{self.ad} - {self.fiyat} TL"

class Rota:
    def __init__(self, detay):
        self.detay = detay
        self.konaklamalar = []
    def konaklama_ekle(self, konaklama):
        self.konaklamalar.append(konaklama)
    def __str__(self):
        return self.detay

class Seyahat:
    def __init__(self):
        self.rotalar = []
    def rota_ekle(self, rota):
        self.rotalar.append(rota)
    def rota_sil(self, index):
        if 0 <= index < len(self.rotalar):
            del self.rotalar[index]

# --- PyQt5 Arayüzü ---
class SeyahatUygulamasi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seyahat Planlama Uygulaması")
        self.seyahat = Seyahat()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.rota_list = QListWidget()
        layout.addWidget(QLabel("Rotalar:"))
        layout.addWidget(self.rota_list)

        
        rota_ekle_layout = QHBoxLayout()
        self.rota_input = QLineEdit()
        self.rota_input.setPlaceholderText("Rota detayı girin")
        rota_ekle_btn = QPushButton("Rota Ekle")
        rota_ekle_btn.clicked.connect(self.rota_ekle)
        rota_ekle_layout.addWidget(self.rota_input)
        rota_ekle_layout.addWidget(rota_ekle_btn)
        layout.addLayout(rota_ekle_layout)

        
        rota_sil_btn = QPushButton("Seçili Rotayı Sil")
        rota_sil_btn.clicked.connect(self.rota_sil)
        layout.addWidget(rota_sil_btn)

        
        konaklama_layout = QHBoxLayout()
        self.konaklama_ad_input = QLineEdit()
        self.konaklama_ad_input.setPlaceholderText("Konaklama adı")
        self.konaklama_fiyat_input = QLineEdit()
        self.konaklama_fiyat_input.setPlaceholderText("Fiyat")
        konaklama_ekle_btn = QPushButton("Konaklama Ekle (Seçili Rota)")
        konaklama_ekle_btn.clicked.connect(self.konaklama_ekle)
        konaklama_layout.addWidget(self.konaklama_ad_input)
        konaklama_layout.addWidget(self.konaklama_fiyat_input)
        konaklama_layout.addWidget(konaklama_ekle_btn)
        layout.addLayout(konaklama_layout)

        
        self.konaklama_list = QListWidget()
        layout.addWidget(QLabel("Seçili Rotanın Konaklamaları:"))
        layout.addWidget(self.konaklama_list)
        self.rota_list.currentRowChanged.connect(self.konaklamalari_goster)

        self.setLayout(layout)

    def rota_ekle(self):
        detay = self.rota_input.text().strip()
        if detay:
            rota = Rota(detay)
            self.seyahat.rota_ekle(rota)
            self.rota_list.addItem(str(rota))
            self.rota_input.clear()
        else:
            QMessageBox.warning(self, "Uyarı", "Rota detayı girin!")

    def rota_sil(self):
        index = self.rota_list.currentRow()
        if index >= 0:
            self.seyahat.rota_sil(index)
            self.rota_list.takeItem(index)
            self.konaklama_list.clear()
        else:
            QMessageBox.warning(self, "Uyarı", "Silmek için bir rota seçin!")

    def konaklama_ekle(self):
        index = self.rota_list.currentRow()
        if index < 0:
            QMessageBox.warning(self, "Uyarı", "Önce bir rota seçin!")
            return
        ad = self.konaklama_ad_input.text().strip()
        fiyat = self.konaklama_fiyat_input.text().strip()
        if ad and fiyat.isdigit():
            konaklama = Konaklama(ad, int(fiyat))
            self.seyahat.rotalar[index].konaklama_ekle(konaklama)
            self.konaklamalari_goster(index)
            self.konaklama_ad_input.clear()
            self.konaklama_fiyat_input.clear()
        else:
            QMessageBox.warning(self, "Uyarı", "Geçerli konaklama adı ve fiyat girin!")

    def konaklamalari_goster(self, index):
        self.konaklama_list.clear()
        if 0 <= index < len(self.seyahat.rotalar):
            for k in self.seyahat.rotalar[index].konaklamalar:
                self.konaklama_list.addItem(str(k))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = SeyahatUygulamasi()
    pencere.show()
    sys.exit(app.exec_())
