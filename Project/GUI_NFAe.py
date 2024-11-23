import os
import tkinter as tk
from tkinter import filedialog, messagebox
from graphviz import Digraph
from PIL import Image, ImageTk
from NFAe import NFAe


def read_nfa_from_file(filename, steps_display):
    nfae = NFAe(steps_display)
    with open(filename, 'r') as file:
        lines = file.readlines()
        initial_state_line, accept_states_line, *transitions_lines = map(str.strip, lines)

        start_state = initial_state_line.split()[1]
        nfae.add_state(start_state, is_start=True)

        accept_states = accept_states_line.split()[1:]
        for state in accept_states:
            nfae.add_state(state, is_accept=True)

        for transition in transitions_lines:
            from_state, symbol, to_state = transition.split()
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


class NFAeMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Kiểm tra NFAe")

        self.nfae = None
        self.root.configure(bg=BG_COLOR)
        self.root.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT}")  # Kích thước cửa sổ
        # Label
        self.label = tk.Label(root, text="Kiểm tra NFAe", font=("Helvetica", 30, "bold"))
        self.label.pack(pady=10)

        # Load NFA Button
        self.load_nfae_button = tk.Button(root, text="Nạp NFAe từ File", font=("Helvetica", 20),
                                          bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, command=self.load_nfa)
        self.load_nfae_button.pack(pady=10)

        # Load NFA Button
        self.view_nfae_button = tk.Button(root, text="Xem NFAe", font=("Helvetica", 20),
                                          bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, command=self.show_nfae_diagram)
        self.view_nfae_button.pack(pady=10)

        # Input String Entry
        self.input_label = tk.Label(root, text="Nhập chuỗi để kiểm tra:", font=NORMAL_FONT)
        self.input_label.pack(pady=20)

        self.input_entry = tk.Entry(root, width=25, font=NORMAL_FONT)
        self.input_entry.pack(pady=5)

        # Check Button
        self.check_button = tk.Button(root, text="Kiểm tra", font=("Helvetica", 20),
                                      bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, command=self.check_string)
        self.check_button.pack(pady=10)
        # Result Label
        self.result_label = tk.Label(root, text="", font=NORMAL_FONT, fg="blue")
        self.result_label.pack(pady=10)

        self.steps_display = tk.Text(root, height=10, width=60, font=("Helvetica", 20))
        self.steps_display.pack(pady=10)

    def load_nfa(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                self.nfae = read_nfa_from_file(file_path, self.steps_display)
                messagebox.showinfo("Success", "Nạp thành công NFAe!")
                draw_nfae(self.nfae)
            except Exception as e:
                messagebox.showerror("Error", f"Nạp thất bại NFAe: {e}")

    def check_string(self):
        if not self.nfae:
            messagebox.showwarning("Warning", "Hãy nạp NFAe trước!")
            return

        input_string = self.input_entry.get()
        if self.nfae.accepts(input_string):
            self.result_label.config(text="NFAe CHẤP NHẬN chuỗi đã nhập.", fg="green")
        else:
            self.result_label.config(text="NFAe KHÔNG CHẤP NHẬN chuỗi đã nhập.", fg="red")

    def show_nfae_diagram(self, image_path="./diagram.png"):
        if not self.nfae:
            messagebox.showwarning("Warning", "Hãy nạp NFAe trước!")
            return

        diagram_window = tk.Toplevel(self.root)
        diagram_window.title("NFAe Diagram")
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file does not exist at: {image_path}")

            # Mở hình ảnh với Pillow
            img = Image.open(image_path)

            # Chuyển đổi thành đối tượng mà Tkinter có thể sử dụng
            img = ImageTk.PhotoImage(img)

            # Tạo Label để hiển thị hình ảnh
            label = tk.Label(diagram_window, image=img)
            label.image = img  # Lưu tham chiếu để tránh bị thu hồi
            label.pack()

        except Exception as e:
            print(f"Error loading image: {e}")  # In ra lỗi nếu có
            error_label = tk.Label(diagram_window, text=f"Unable to load image: {e}")
            error_label.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = NFAeMenu(root)
    root.mainloop()
