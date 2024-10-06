import numpy as np
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkinter import filedialog
import csv

data = []

def import_data():
    global data
    """Import student data from a CSV file."""
    # Mở hộp thoại để chọn file CSV
    file_path = filedialog.askopenfilename(defaultextension=".csv",
                                           filetypes=[("CSV files", "*.csv"), ("All files", "*.*")], title="Chọn file CSV để nhập")
    if not file_path:
        return None

    data = []
    try:
        #

        messagebox.showinfo(
            "Thành công", f"Dữ liệu đã được nhập từ file {file_path}.")
        data = load_data(file_path)
        print(data)
        return
    except Exception as e:
        messagebox.showerror("Error", f"Đã xảy ra lỗi khi nhập file CSV: {e}")
        return None