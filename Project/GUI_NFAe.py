import os
import traceback
import tkinter as tk
from tkinter import filedialog, messagebox
from graphviz import Digraph
from PIL import Image, ImageTk
from NFAe import NFAe


def read_NFAe_from_file(filename, steps_display):
    nfae = NFAe(
        states=set(),
        alphabet=set(),
        start_state="",
        accept_states=set(),
        transition={},
        steps_display=steps_display
    )
    with open(filename, 'r') as file:
        lines = file.readlines()

        states = lines[0].split(":")[1].strip().split(",")
        alphabet = lines[1].split(":")[1].strip().split(",")
        start_state = lines[2].split(":")[1].strip()
        accept_states = lines[3].split(":")[1].strip().split(",")

        # Nạp trạng thái
        for state in states:
            nfae.add_state(state.strip())
        # Nạp ký tự đầu vào
        nfae.alphabet = alphabet
        # Nạp trạng thái bắt đầu
        nfae.add_state(start_state, is_start=True)
        # Nạp trạng thái kết thúc
        for state in accept_states:
            nfae.add_state(state, is_accept=True)
        # Nạp hàm chuyển delta
        for line in lines[5:]:
            from_state, symbol, to_state = line.split()
            nfae.add_transition(from_state, symbol, to_state)

    return nfae


def draw_nfae(nfae):
    dot = Digraph(format="png")
    dot.attr(rankdir="LR")
    for state in nfae.states:
        if state in nfae.accept_states:
            dot.node(state, shape="doublecircle")
        else:
            dot.node(state, shape="circle")

    dot.node("start", shape="point")
    dot.edge("start", nfae.start_state)

    for (from_state, symbol), to_states in nfae.transitions.items():
        for to_state in to_states:
            label = "ε" if symbol == "e" else symbol
            dot.edge(from_state, to_state, label=label)

    output_file = r"./diagram"
    try:
        dot.render(output_file, cleanup=True)
        return output_file + ".png"
    except Exception as e:
        print("Lỗi vẽ đồ thị: ", e)
        return None


# ----------- GUI ---------------


DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 900
BG_COLOR = "#f5f2fa"
BUTTON_COLOR = "#ffffff"
BUTTON_TEXT_COLOR = "#625285"
NORMAL_FONT = ("Helvetica", 16)
BUTTON_FONT = ("Helvetica", 20)


class NFAeMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Kiểm tra NFAe")

        self.nfae = None
        self.root.configure(bg=BG_COLOR)
        self.root.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT}")  # Kích thước cửa sổ

        # Main Label
        self.label = tk.Label(root, text="Kiểm tra NFAe", font=("Helvetica", 30, "bold"))
        self.label.pack(pady=10)

        # Load NFAe Button
        self.load_NFAe_button = tk.Button(
            root, text="Nạp NFAe từ File", font=BUTTON_FONT,
            bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR,
            command=self.load_NFAe
        )
        self.load_NFAe_button.pack(pady=10)

        # View NFAe Button
        self.view_NFAe_button = tk.Button(
            root, text="Xem NFAe", font=BUTTON_FONT,
            bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR,
            command=self.show_NFAe_diagram
        )
        self.view_NFAe_button.pack(pady=10)

        # Input String Entry
        self.input_label = tk.Label(root, text="Nhập chuỗi để kiểm tra:", font=NORMAL_FONT)
        self.input_label.pack(pady=20)

        self.input_entry = tk.Entry(root, width=25, font=NORMAL_FONT)
        self.input_entry.pack(pady=5)

        # Check Button
        self.check_button = tk.Button(
            root, text="Kiểm tra", font=BUTTON_FONT,
            bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR,
            command=self.check_string
        )
        self.check_button.pack(pady=10)

        # Result Label
        self.result_label = tk.Label(root, text="", font=NORMAL_FONT, fg="blue")
        self.result_label.pack(pady=10)

        # Step display field
        self.steps_display = tk.Text(root, height=10, width=60, font=NORMAL_FONT, state="disabled")
        self.steps_display.pack(pady=10)

    def load_NFAe(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                self.nfae = read_NFAe_from_file(file_path, self.steps_display)
                messagebox.showinfo("Success", "Nạp thành công NFAe!")
                draw_nfae(self.nfae)
            except Exception as e:
                traceback.print_exception(e)
                messagebox.showerror("Error", f"Nạp thất bại NFAe: {e}")

    def check_string(self):
        self.steps_display.config(state="normal")
        if not self.nfae:
            messagebox.showwarning("Warning", "Hãy nạp NFAe trước!")
            return

        input_string = self.input_entry.get()
        if self.nfae.accepts(input_string):
            self.result_label.config(text="NFAe CHẤP NHẬN chuỗi đã nhập.", fg="green")
        else:
            self.result_label.config(text="NFAe KHÔNG CHẤP NHẬN chuỗi đã nhập.", fg="red")
        self.steps_display.config(state="disabled")

    def show_NFAe_diagram(self, image_path="./diagram.png"):
        if not self.nfae:
            messagebox.showwarning("Warning", "Hãy nạp NFAe trước!")
            return

        diagram_window = tk.Toplevel(self.root)
        diagram_window.title("NFAe Diagram")
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Không tồn tại hình ảnh tại đường dẫn: {image_path}")

            # Mở hình ảnh với Pillow
            img = Image.open(image_path)

            # Chuyển đổi thành đối tượng mà Tkinter có thể sử dụng
            img = ImageTk.PhotoImage(img)

            # Tạo Label để hiển thị hình ảnh
            label = tk.Label(diagram_window, image=img)
            label.image = img  # Lưu tham chiếu để tránh bị thu hồi
            label.pack()

        except Exception as e:
            print(f"Lỗi tải hình ảnh: {e}")
            error_label = tk.Label(diagram_window, text=f"Không thể tải hình ảnh: {e}")
            error_label.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = NFAeMenu(root)
    root.mainloop()
