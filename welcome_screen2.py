'''
import tkinter as tk
from tkinter import messagebox
import subprocess

def close_window():
    root.destroy()
    subprocess.run(["python", "main.py"])  

def toggle_info():
    if info_label.winfo_ismapped():  
        info_label.pack_forget()  
    else:
        info_label.pack()  

root = tk.Tk()
root.title("Slot Machine")
root.geometry("900x600")

root.configure(bg="#f0f0f0")  

info_label = tk.Label(root, text="Kada pokrenete igru, iznos i ulog sa kojim želite da igrate!\n\nNovac koji dobijate ne možete podići!\n\nSve je u vidu zabave, KOCKA NIJE PREPORUČENA NIKOME!", font=("Helvetica", 10), bg="#f0f0f0")

info_button = tk.Button(root, text="ℹ️ Info", command=toggle_info, bd=0, bg="#007bff", fg="white", font=("Helvetica", 14))
info_button.place(x=10, y=10)

welcome_text = "Dobrodošli u naš Slot Sistem!\n\nOvdje se možete zabaviti, ali ne i kockati!\n\nOva igra je u vidu zabave"
welcome_label = tk.Label(root, text=welcome_text, font=("Helvetica", 16), bg="#f0f0f0")
welcome_label.pack(pady=30, padx=50)

close_button = tk.Button(root, text="Pokreni igru", command=close_window, bd=0, bg="#28a745", fg="white", font=("Helvetica", 14))
close_button.pack(pady=20)

root.mainloop()
'''
