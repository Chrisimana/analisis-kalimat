import json
import os
from datetime import datetime

class HistoryManager:
    def __init__(self, filename="history.json"):
        self.filename = filename
        self.history = []
        self.load_history()
    
    # Memuat riwayat dari file
    def load_history(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.history = json.load(file)
            except (json.JSONDecodeError, IOError):
                self.history = []
    
    # Menyimpan riwayat ke file
    def save_history(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.history, file, indent=2)
        except IOError:
            pass  # Gagal menyimpan, tapi program tetap berjalan
    
    # Menambahkan entri baru ke riwayat
    def add_entry(self, kalimat_asli, kalimat_dibalik, jumlah_vokal, jumlah_konsonan, jumlah_kata, total_karakter):
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "kalimat_asli": kalimat_asli,
            "kalimat_dibalik": kalimat_dibalik,
            "jumlah_vokal": jumlah_vokal,
            "jumlah_konsonan": jumlah_konsonan,
            "jumlah_kata": jumlah_kata,
            "total_karakter": total_karakter
        }
        
        self.history.append(entry)
        
        # Batasi riwayat hingga 50 entri terakhir
        if len(self.history) > 50:
            self.history = self.history[-50:]
        
        self.save_history()
    
    # Mengembalikan seluruh riwayat
    def get_history(self):
        return self.history
    
    # Menghapus semua riwayat
    def clear_history(self):
        self.history = []
        self.save_history()