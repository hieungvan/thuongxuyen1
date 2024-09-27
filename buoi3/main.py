import numpy as np
import tkinter as tk
from tkinter import messagebox


def giai_he_phuong_trinh(A, B):
    """
    Giải hệ phương trình tuyến tính A * x = B
    """
    rank_A = np.linalg.matrix_rank(A)
    augmented_matrix = np.column_stack((A, B))
    rank_augmented = np.linalg.matrix_rank(augmented_matrix)
    n = A.shape[1]

    if rank_A == rank_augmented:
        if rank_A == n:
            try:
                x = np.linalg.solve(A, B)
                return x
            except np.linalg.LinAlgError:
                return "Lỗi không thể giải hệ phương trình."
        else:
            return "Hệ phương trình có vô số nghiệm."
    else:
        return "Hệ phương trình vô nghiệm."


def lay_gia_tri():
    """
    Lấy giá trị từ các Entry và xử lý
    """
    try:
        n = int(entry_n.get())  # Lấy số phương trình và ẩn số từ Entry
        A = []
        B = []

        # Lấy ma trận A
        for i in range(n):
            hang = []
            for j in range(n):
                hang.append(float(entries_A[i][j].get()))
            A.append(hang)

        # Lấy vector B
        for i in range(n):
            B.append(float(entries_B[i].get()))

        # Chuyển về dạng numpy array
        A = np.array(A)
        B = np.array(B)

        # Giải hệ phương trình
        ket_qua = giai_he_phuong_trinh(A, B)

        if isinstance(ket_qua, np.ndarray):
            ket_qua = ", ".join(
                [f"x{i+1} = {val:.2f}" for i, val in enumerate(ket_qua)])
        messagebox.showinfo(
            "Kết quả", f"Nghiệm của hệ phương trình:\n{ket_qua}")

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ.")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


def tao_giao_dien_ma_tran():
    """
    Tạo giao diện nhập ma trận A, ma trận C và vector B dựa trên số phương trình
    """
    try:
        n = int(entry_n.get())
        for widget in frame_A.winfo_children():
            widget.destroy()

        for widget in frame_B.winfo_children():
            widget.destroy()

        for widget in frame_C.winfo_children():
            widget.destroy()

        global entries_A, entries_B, entries_C
        entries_A = []
        entries_B = []
        entries_C = []

        # Tạo các ô nhập cho ma trận A
        for i in range(n):
            row_entries = []
            for j in range(n):
                entry = tk.Entry(frame_A, width=5)
                entry.grid(row=i, column=j)
                row_entries.append(entry)
            entries_A.append(row_entries)

        # Tạo các ô nhập cho vector B
        for i in range(n):
            entry = tk.Entry(frame_B, width=5)
            entry.grid(row=i, column=0)
            entries_B.append(entry)

        # Tạo các ô nhập cho ma trận C
        for i in range(n):
            row_entries = []
            for j in range(n):
                entry = tk.Entry(frame_C, width=5)
                entry.grid(row=i, column=j)
                row_entries.append(entry)
            entries_C.append(row_entries)

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên hợp lệ.")


def lay_ma_tran():
    """
    Lấy giá trị từ các Entry và trả về ma trận A, C và B
    """
    try:
        n = int(entry_n.get())  # Lấy số phương trình và ẩn số từ Entry
        A = []
        B = []
        C = []

        # Lấy ma trận A
        for i in range(n):
            hang = []
            for j in range(n):
                hang.append(float(entries_A[i][j].get()))
            A.append(hang)

        # Lấy ma trận C
        for i in range(n):
            hang = []
            for j in range(n):
                hang.append(float(entries_C[i][j].get()))
            C.append(hang)

        # Lấy vector B
        for i in range(n):
            B.append(float(entries_B[i].get()))

        A = np.array(A)
        B = np.array(B)
        C = np.array(C)
        return A, B, C
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ.")


# Các chức năng ma trận

def cong_ma_tran():
    try:
        A, _, C = lay_ma_tran()
        A_plus_C = A + C  # Thực hiện phép cộng
        messagebox.showinfo("Kết quả", f"Kết quả phép cộng A + C:\n{A_plus_C}")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


def tru_ma_tran():
    try:
        A, _, C = lay_ma_tran()
        A_minus_C = A - C  # Thực hiện phép trừ
        messagebox.showinfo("Kết quả", f"Kết quả phép trừ A - C:\n{A_minus_C}")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


def nhan_ma_tran():
    try:
        A, _, C = lay_ma_tran()
        A_mul_C = A @ C  # Thực hiện phép nhân
        messagebox.showinfo("Kết quả", f"Kết quả phép nhân A * C:\n{A_mul_C}")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


def chia_ma_tran():
    try:
        A, _, C = lay_ma_tran()
        A_div_C = A / C  # Thực hiện phép chia (element-wise)
        messagebox.showinfo("Kết quả", f"Kết quả phép chia A / C:\n{A_div_C}")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


def tim_ma_tran_nghich_dao():
    try:
        A, _, _ = lay_ma_tran()
        A_inv = np.linalg.inv(A)  # Tìm ma trận nghịch đảo
        messagebox.showinfo("Kết quả", f"Ma trận nghịch đảo của A:\n{A_inv}")
    except np.linalg.LinAlgError:
        messagebox.showerror("Lỗi", "Ma trận không khả nghịch.")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


def tim_hang_cua_ma_tran():
    try:
        A, _, _ = lay_ma_tran()
        rank = np.linalg.matrix_rank(A)  # Tìm hạng của ma trận
        messagebox.showinfo("Kết quả", f"Hạng của ma trận A:\n{rank}")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


# Tạo cửa sổ giao diện
root = tk.Tk()
root.title("Giải hệ phương trình và các phép toán ma trận")

# Khung nhập số phương trình
frame_n = tk.Frame(root)
frame_n.pack(pady=10)

label_n = tk.Label(frame_n, text="Nhập số phương trình và số ẩn số:")
label_n.pack(side=tk.LEFT)

entry_n = tk.Entry(frame_n, width=5)
entry_n.pack(side=tk.LEFT)

button_tao_giao_dien = tk.Button(
    frame_n, text="Tạo giao diện", command=tao_giao_dien_ma_tran)
button_tao_giao_dien.pack(side=tk.LEFT, padx=10)

# Khung nhập ma trận A
frame_A_label = tk.Label(root, text="Nhập ma trận hệ số A:")
frame_A_label.pack()

frame_A = tk.Frame(root)
frame_A.pack(pady=10)

# Khung nhập vector B
frame_B_label = tk.Label(root, text="Nhập vector kết quả B:")
frame_B_label.pack()

frame_B = tk.Frame(root)
frame_B.pack(pady=10)

# Khung nhập ma trận C
frame_C_label = tk.Label(root, text="Nhập ma trận hệ số C:")
frame_C_label.pack()

frame_C = tk.Frame(root)
frame_C.pack(pady=10)

# Nút giải hệ phương trình
button_giai = tk.Button(root, text="Giải hệ phương trình", command=lay_gia_tri)
button_giai.pack(pady=20)

# Nút chức năng ma trận
button_cong = tk.Button(root, text="Cộng ma trận A và C", command=cong_ma_tran)
button_cong.pack(pady=5)

button_tru = tk.Button(root, text="Trừ ma trận A và C", command=tru_ma_tran)
button_tru.pack(pady=5)

button_nhan = tk.Button(root, text="Nhân ma trận A và C", command=nhan_ma_tran)
button_nhan.pack(pady=5)

button_chia = tk.Button(root, text="Chia ma trận A và C", command=chia_ma_tran)
button_chia.pack(pady=5)

button_nghich_dao = tk.Button(
    root, text="Tìm ma trận nghịch đảo A", command=tim_ma_tran_nghich_dao)
button_nghich_dao.pack(pady=5)

button_hang = tk.Button(
    root, text="Tìm hạng của ma trận A", command=tim_hang_cua_ma_tran)
button_hang.pack(pady=5)

# Chạy ứng dụng
root.mainloop()
