class NFAe:
    def __init__(self):
        self.states = set()  # Tập trạng thái Q
        self.start_state = None  # Trạng thái bắt đầu
        self.accept_states = set()  # Trạng thái kết thúc
        self.transition = {}  # Hàm chuyển

    def add_state(self, state, is_start=False, is_accept=False):
        self.states.add(state)
        if is_start:
            self.start_state = state
        if is_accept:
            self.accept_states.add(state)

    def add_transition(self, from_state, symbol, to_state):
        if (from_state, symbol) not in self.transition:
            self.transition[(from_state, symbol)] = set()
        self.transition[(from_state, symbol)].add(to_state)

    # Tìm E-closure của 1 trạng thái
    def e_closure(self, states):
        closure = set(states)
        stack = list(states)

        while stack:
            current = stack.pop()
            for next_state in self.transition.get((current, 'e'), []):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        print(closure)
        return closure

    # Chuyển trạng thái hiện tại sang trạng thái mới trên nhãn symbol
    def move(self, states, symbol):
        new_states = set()
        for state in states:
            new_states.update(self.transition.get((state, symbol), []))
        return new_states

    def accepts(self, input_string):
        # Tính delta* của q0 trên nhãn e
        current_states = self.e_closure({self.start_state})

        # Chuyển trạng thái trên từng ký tự đầu vào
        for symbol in input_string:
            current_states = self.e_closure(self.move(current_states, symbol))
        return not current_states.isdisjoint(self.accept_states)  # Kiểm tra trạng thái kết thúc
