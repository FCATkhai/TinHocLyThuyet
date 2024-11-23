import tkinter as tk
from tkinter import filedialog, messagebox
from NFAe import NFAe


def read_nfa_from_file(filename):
    nfae = NFAe()
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


# ----------- GUI ---------------


DEFAULT_WIDTH = 600
DEFAULT_HEIGHT = 600
BG_COLOR = "#f5f2fa"
BUTTON_COLOR = "#ffffff"
BUTTON_TEXT_COLOR = "#625285"
NORMAL_FONT = ("Helvetica", 16)


class NFAeMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Kiểm tra NFAe")

        self.nfa = None
        self.root.configure(bg=BG_COLOR)
        self.root.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT}")  # Kích thước cửa sổ
        # Label
        self.label = tk.Label(root, text="Kiểm tra NFAe", font=("Helvetica", 30, "bold"))
        self.label.pack(pady=10)

        # Load NFA Button
        self.load_nfa_button = tk.Button(root, text="Nạp NFAe từ File", font=("Helvetica", 20),
                                         bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, command=self.load_nfa)
        self.load_nfa_button.pack(pady=10)

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

    def load_nfa(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                self.nfa = read_nfa_from_file(file_path)
                messagebox.showinfo("Success", "Nạp thành công NFAe!")
            except Exception as e:
                messagebox.showerror("Error", f"Nạp thất bại NFAe: {e}")

    def check_string(self):
        if not self.nfa:
            messagebox.showwarning("Warning", "Hãy nạp NFAe trước!")
            return

        input_string = self.input_entry.get()
        if self.nfa.accepts(input_string):
            self.result_label.config(text="NFAe CHẤP NHẬN chuỗi đã nhập.", fg="green")
        else:
            self.result_label.config(text="NFAe KHÔNG CHẤP NHẬN chuỗi đã nhập.", fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = NFAeMenu(root)
    root.mainloop()
