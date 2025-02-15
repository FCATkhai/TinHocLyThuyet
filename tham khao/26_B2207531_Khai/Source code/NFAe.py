import tkinter as tk


# Class State để tạo các trạng thái khác nhau
class State:
    counter = 0

    def __init__(self):
        self.id = f"q{State.counter}"
        State.counter += 1

    @classmethod
    def reset_counter(cls):
        # Reset counter về 0
        cls.counter = 0

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, State) and self.id == other.id


class NFAe:
    def __init__(self, steps_display):
        self.states = set()  # Tập trạng thái Q
        self.alphabet = set()  # Ký tự nhập
        self.start_state = None  # Trạng thái bắt đầu
        self.accept_states = set()  # Trạng thái kết thúc
        self.transitions = {}  # Hàm chuyển đổi delta
        self.steps_display = steps_display  # Log các bước thực hiện

    def add_state(self, state, is_start=False, is_accept=False):
        self.states.add(state)
        if is_start:
            self.start_state = state
        if is_accept:
            self.accept_states.add(state)

    def reset_accept_states(self):
        self.accept_states = set()

    def add_transition(self, from_state, symbol, to_state):
        if (from_state, symbol) not in self.transitions:
            self.transitions[(from_state, symbol)] = set()
        self.transitions[(from_state, symbol)].add(to_state)

    # Tìm E-closure của 1 trạng thái
    def e_closure(self, states):
        closure = set(states)
        stack = list(states)

        while stack:
            current = stack.pop()
            for next_state in self.transitions.get((current, 'e'), []):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

        self.steps_display.insert(
            tk.END,
            f"Trạng thái mới sau khi tính e-closure: {closure if closure else "∅"}\n"
        )
        return closure

    # Chuyển trạng thái hiện tại sang trạng thái mới trên nhãn symbol
    def move(self, states, symbol):
        new_states = set()
        for state in states:
            new_states.update(self.transitions.get((state, symbol), []))
        self.steps_display.insert(
            tk.END,
            f"Trạng thái mới trên nhãn {symbol}: {new_states if new_states else "∅"}\n"
        )
        return new_states

    def accepts(self, input_string):
        # Tính delta* của q0 trên nhãn e
        current_states = self.e_closure({self.start_state})
        self.steps_display.delete(1.0, tk.END)
        self.steps_display.insert(tk.END, f"Trạng thái bắt đầu: {current_states}\n")

        # Chuyển trạng thái trên từng ký tự đầu vào
        for symbol in input_string:
            self.steps_display.insert(tk.END, f"Ký tự đang xét: {symbol}\n")
            current_states = self.e_closure(self.move(current_states, symbol))
        # Kiểm tra trạng thái cuối cùng
        if not current_states.isdisjoint(self.accept_states):
            self.steps_display.insert(
                tk.END,
                f"Trạng thái cuối cùng: {current_states if current_states else "∅"}\nChuỗi được chấp nhận vì trạng thái cuối cùng ({current_states}) chứa trạng thái kết thúc {current_states & self.accept_states}.\n"
            )
            return True
        else:
            self.steps_display.insert(
                tk.END,
                f"Trạng thái cuối cùng: {current_states if current_states else "∅"}\nChuỗi không được chấp nhận vì trạng thái cuối cùng không chứa trạng thái kết thúc {self.accept_states}.\n"
            )
            return False

    def print_structure(self):
        print("NFAe Structure:")
        for (from_state, symbol), to_states in self.transitions.items():
            for to_state in to_states:
                transition_type = "ε" if symbol == "e" else symbol
                print(f"{from_state} --{transition_type}--> {to_state}")
        print(f"Start State: {self.start_state}")
        print(f"Accept States: {self.accept_states}")
