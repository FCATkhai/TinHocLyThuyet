import tkinter as tk
class NFAe:
    def __init__(self, steps_display):
        self.states = set()  # Tập trạng thái Q
        self.start_state = None  # Trạng thái bắt đầu
        self.accept_states = set()  # Trạng thái kết thúc
        self.transitions = {}  # Hàm chuyển
        self.steps_display = steps_display

    def add_state(self, state, is_start=False, is_accept=False):
        self.states.add(state)
        if is_start:
            self.start_state = state
        if is_accept:
            self.accept_states.add(state)

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
        # print(closure)
        self.steps_display.insert(tk.END, f"Trạng thái mới sau khi tính e-closure: {closure if closure else "∅"}\n")
        return closure

    # Chuyển trạng thái hiện tại sang trạng thái mới trên nhãn symbol
    def move(self, states, symbol):
        new_states = set()
        for state in states:
            new_states.update(self.transitions.get((state, symbol), []))
        self.steps_display.insert(tk.END, f"Trạng thái mới trên nhãn {symbol}: {new_states}\n")
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
        return not current_states.isdisjoint(self.accept_states)  # Kiểm tra trạng thái kết thúc
