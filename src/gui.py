import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import tkinter.font as tkFont
from kalimat_utils import balik_kalimat, hitung_vokal, hitung_konsonan, hitung_kata, hitung_karakter
from history_manager import HistoryManager

class KalimatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analisis Text")
        self.root.geometry("800x700")
        self.root.configure(bg="#f0f0f0")
        
        # Inisialisasi history manager
        self.history_manager = HistoryManager()
        
        # Buat font custom
        self.title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.normal_font = tkFont.Font(family="Helvetica", size=10)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame utama
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Judul
        title_label = ttk.Label(main_frame, text="Analisis Text", 
                               font=self.title_font, foreground="#2c3e50")
        title_label.pack(pady=(0, 20))
        
        # Frame input
        input_frame = ttk.LabelFrame(main_frame, text="Input Kalimat", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Label dan entry untuk input kalimat
        ttk.Label(input_frame, text="Masukkan kalimat:").pack(anchor=tk.W)
        self.kalimat_entry = tk.Text(input_frame, height=4, width=70, font=self.normal_font)
        self.kalimat_entry.pack(fill=tk.X, pady=(5, 0))
        self.kalimat_entry.bind("<KeyRelease>", self.update_preview)
        
        # Preview kalimat
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.preview_label = ttk.Label(preview_frame, text="", font=self.normal_font, 
                                      wraplength=700, justify=tk.LEFT)
        self.preview_label.pack(fill=tk.X)
        
        # Frame tombol
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Tombol proses
        self.process_button = ttk.Button(button_frame, text="Proses Kalimat", 
                                        command=self.proses_kalimat, state=tk.DISABLED)
        self.process_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Tombol hapus input
        ttk.Button(button_frame, text="Hapus Input", command=self.hapus_input).pack(side=tk.LEFT, padx=(0, 10))
        
        # Frame hasil
        result_frame = ttk.LabelFrame(main_frame, text="Hasil Analisis", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Buat notebook (tab) untuk hasil
        self.notebook = ttk.Notebook(result_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab hasil utama
        main_result_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(main_result_frame, text="Hasil Utama")
        
        # Grid untuk menampilkan hasil
        ttk.Label(main_result_frame, text="Kalimat Asli:", font=self.normal_font).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.kalimat_asli_label = ttk.Label(main_result_frame, text="", font=self.normal_font, wraplength=500)
        self.kalimat_asli_label.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_result_frame, text="Kalimat Dibalik:", font=self.normal_font).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.kalimat_dibalik_label = ttk.Label(main_result_frame, text="", font=self.normal_font, wraplength=500)
        self.kalimat_dibalik_label.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_result_frame, text="Jumlah Huruf Vokal:", font=self.normal_font).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.jumlah_vokal_label = ttk.Label(main_result_frame, text="", font=self.normal_font)
        self.jumlah_vokal_label.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_result_frame, text="Jumlah Huruf Konsonan:", font=self.normal_font).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.jumlah_konsonan_label = ttk.Label(main_result_frame, text="", font=self.normal_font)
        self.jumlah_konsonan_label.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_result_frame, text="Jumlah Kata:", font=self.normal_font).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.jumlah_kata_label = ttk.Label(main_result_frame, text="", font=self.normal_font)
        self.jumlah_kata_label.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_result_frame, text="Total Karakter:", font=self.normal_font).grid(row=5, column=0, sticky=tk.W, pady=5)
        self.total_karakter_label = ttk.Label(main_result_frame, text="", font=self.normal_font)
        self.total_karakter_label.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Tab riwayat
        history_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(history_frame, text="Riwayat")
        
        # Tombol untuk riwayat
        history_button_frame = ttk.Frame(history_frame)
        history_button_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(history_button_frame, text="Muat Ulang Riwayat", 
                  command=self.tampilkan_riwayat).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(history_button_frame, text="Hapus Riwayat", 
                  command=self.hapus_riwayat).pack(side=tk.LEFT)
        
        # Area teks untuk menampilkan riwayat
        self.history_text = scrolledtext.ScrolledText(history_frame, width=70, height=20, font=self.normal_font)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # Tampilkan riwayat saat pertama kali dibuka
        self.tampilkan_riwayat()
    
    # Memperbarui preview kalimat saat pengguna mengetik
    def update_preview(self, event=None):
        kalimat = self.kalimat_entry.get("1.0", tk.END).strip()
        
        if kalimat:
            self.preview_label.config(text=f"Preview: {kalimat}")
            self.process_button.config(state=tk.NORMAL)
        else:
            self.preview_label.config(text="")
            self.process_button.config(state=tk.DISABLED)
    
    # Menghapus input dan hasil
    def hapus_input(self):
        self.kalimat_entry.delete("1.0", tk.END)
        self.preview_label.config(text="")
        self.clear_results()
        self.process_button.config(state=tk.DISABLED)
    
    # Mengosongkan semua label hasil
    def clear_results(self):
        self.kalimat_asli_label.config(text="")
        self.kalimat_dibalik_label.config(text="")
        self.jumlah_vokal_label.config(text="")
        self.jumlah_konsonan_label.config(text="")
        self.jumlah_kata_label.config(text="")
        self.total_karakter_label.config(text="")
    
    # Memproses kalimat dan menampilkan hasil
    def proses_kalimat(self):
        kalimat = self.kalimat_entry.get("1.0", tk.END).strip()
        
        if not kalimat:
            messagebox.showwarning("Peringatan", "Masukkan kalimat terlebih dahulu!")
            return
        
        # Proses kalimat
        kalimat_dibalik = balik_kalimat(kalimat)
        jumlah_vokal = hitung_vokal(kalimat)
        jumlah_konsonan = hitung_konsonan(kalimat)
        jumlah_kata = hitung_kata(kalimat)
        total_karakter = hitung_karakter(kalimat)
        
        # Tampilkan hasil
        self.kalimat_asli_label.config(text=kalimat)
        self.kalimat_dibalik_label.config(text=kalimat_dibalik)
        self.jumlah_vokal_label.config(text=str(jumlah_vokal))
        self.jumlah_konsonan_label.config(text=str(jumlah_konsonan))
        self.jumlah_kata_label.config(text=str(jumlah_kata))
        self.total_karakter_label.config(text=str(total_karakter))
        
        # Simpan ke riwayat
        self.history_manager.add_entry(
            kalimat, kalimat_dibalik, jumlah_vokal, 
            jumlah_konsonan, jumlah_kata, total_karakter
        )
        
        # Pindah ke tab hasil
        self.notebook.select(0)
        
        # Tampilkan pesan sukses
        messagebox.showinfo("Berhasil", "Kalimat berhasil diproses!")
    
    # Menampilkan riwayat analisis
    def tampilkan_riwayat(self):
        riwayat = self.history_manager.get_history()
        
        self.history_text.delete("1.0", tk.END)
        
        if not riwayat:
            self.history_text.insert(tk.END, "Belum ada riwayat analisis.")
            return
        
        for i, entry in enumerate(reversed(riwayat), 1):
            self.history_text.insert(tk.END, f"Analisis #{i}\n")
            self.history_text.insert(tk.END, f"Waktu: {entry['timestamp']}\n")
            self.history_text.insert(tk.END, f"Kalimat Asli: {entry['kalimat_asli']}\n")
            self.history_text.insert(tk.END, f"Kalimat Dibalik: {entry['kalimat_dibalik']}\n")
            self.history_text.insert(tk.END, f"Jumlah Vokal: {entry['jumlah_vokal']}\n")
            self.history_text.insert(tk.END, f"Jumlah Konsonan: {entry['jumlah_konsonan']}\n")
            self.history_text.insert(tk.END, f"Jumlah Kata: {entry['jumlah_kata']}\n")
            self.history_text.insert(tk.END, f"Total Karakter: {entry['total_karakter']}\n")
            self.history_text.insert(tk.END, "-" * 50 + "\n\n")
    
    # Menghapus semua riwayat
    def hapus_riwayat(self):
         if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus semua riwayat?"):
            self.history_manager.clear_history()
            self.tampilkan_riwayat()
            messagebox.showinfo("Berhasil", "Riwayat berhasil dihapus!")