import tkinter as tk
from tkinter import messagebox
import random
import os
import requests  # Untuk integrasi PHP opsional

def tebak_angka():
    angka_rahasia = random.randint(1, 100)
    percobaan = 0
    high_score_file = "high_score.txt"
    use_php_integration = tk.messagebox.askyesno("Integrasi Web?", "Gunakan integrasi dengan server PHP (XAMPP harus running)?")  # Opsional
    
    # Load high score lokal
    if os.path.exists(high_score_file):
        try:
            with open(high_score_file, "r") as f:
                high_score = int(f.read().strip())
        except (ValueError, IOError):
            high_score = float('inf')
    else:
        high_score = float('inf')
    
    def kirim_ke_php(nama, skor):
        if not use_php_integration:
            return
        try:
            response = requests.post("http://localhost/save_score.php", data={"nama": nama, "skor": skor}, timeout=5)
            if response.text == "success":
                messagebox.showinfo("Sukses", "Skor dikirim ke server web!")
            else:
                messagebox.showwarning("Warning", "Gagal kirim ke server: " + response.text)
        except requests.exceptions.RequestException:
            messagebox.showwarning("Warning", "Server tidak tersedia (jalankan XAMPP). Skor tetap lokal.")
    
    def cek_tebakan():
        nonlocal percobaan, angka_rahasia
        try:
            tebakan_str = entry.get().strip()
            if not tebakan_str:
                label_hasil.config(text="Masukkan angka valid (1-100)!")
                return
            tebakan = int(tebakan_str)
            if tebakan < 1 or tebakan > 100:
                label_hasil.config(text="Angka harus antara 1-100!")
                return
            percobaan += 1
            label_percobaan.config(text=f"Percobaan: {percobaan}")
            if tebakan < angka_rahasia:
                label_hasil.config(text="Terlalu rendah! Coba lagi.")
            elif tebakan > angka_rahasia:
                label_hasil.config(text="Terlalu tinggi! Coba lagi.")
            else:
                label_hasil.config(text=f"Selamat! Benar dalam {percobaan} percobaan!")
                # Update high score lokal
                if percobaan < high_score:
                    high_score = percobaan
                    try:
                        with open(high_score_file, "w") as f:
                            f.write(str(high_score))
                        label_high.config(text=f"High Score Baru: {high_score}")
                    except IOError:
                        label_high.config(text=f"High Score: {high_score} (Gagal simpan)")
                else:
                    label_high.config(text=f"High Score: {high_score}")
                # Input nama untuk kirim ke PHP
                nama = tk.simpledialog.askstring("High Score", "Masukkan nama Anda:")
                if nama:
                    kirim_ke_php(nama, percobaan)
                messagebox.showinfo("Menang!", f"Angka: {angka_rahasia}\nPercobaan: {percobaan}\nHigh Score: {high_score}")
            entry.delete(0, tk.END)
        except ValueError:
            label_hasil.config(text="Masukkan angka valid (1-100)!")
    
    def reset_game():
        nonlocal angka_rahasia, percobaan
        angka_rahasia = random.randint(1, 100)
        percobaan = 0
        label_hasil.config(text="")
        label_percobaan.config(text="Percobaan: 0")
        entry.delete(0, tk.END)
        # Reload high score
        if os.path.exists(high_score_file):
            try:
                with open(high_score_file, "r") as f:
                    current_high = int(f.read().strip())
                    label_high.config(text=f"High Score: {current_high}")
            except (ValueError, IOError):
                pass
    
    # GUI
    root = tk.Tk()
    root.title("Tebak Angka Desktop - Python")
    root.geometry("350x350")
    root.resizable(False, False)
    
    tk.Label(root, text="Tebak angka 1-100:", font=("Arial", 12, "bold")).pack(pady=10)
    
    entry = tk.Entry(root, font=("Arial", 12), justify="center", width=10)
    entry.pack(pady=5)
    entry.bind("<Return>", lambda e: cek_tebakan())
    
    tk.Button(root, text="Tebak!", command=cek_tebakan, bg="#4CAF50", fg="white", padx=20).pack(pady=5)
    tk.Button(root, text="Reset", command=reset_game, bg="#FF9800", fg="white", padx=20).pack(pady=5)
    
    label_hasil = tk.Label(root, text="", font=("Arial", 11), wraplength=300)
    label_hasil.pack(pady=10)
    
    label_percobaan = tk.Label(root, text="Percobaan: 0", font=("Arial", 10))
    label_percobaan.pack()
    
    label_high = tk.Label(root, text=f"High Score: {high_score if high_score != float('inf') else 'Belum ada'}", font=("Arial", 10, "italic"))
    label_high.pack(pady=5)
    
    # Import simpledialog untuk input nama
    from tkinter import simpledialog
    
    root.mainloop()

if __name__ == "__main__":
    tebak_angka()