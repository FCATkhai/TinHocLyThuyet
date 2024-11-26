import tkinter as tk


def read_NFAe_from_file(filename, steps_display):
    nfae = NFAe(
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


# Helper Class for Unique State Representation
class State:
    counter = 0

    def __init__(self):
        self.id = f"q{State.counter}"
        State.counter += 1

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, State) and self.id == other.id


def create_nfa(postfix, steps_display):
    """
    Constructs an NFAe using the new NFAe class from a postfix regex.
    """
    nfa_stack = []
    for char in postfix:
        if char.isalnum():  # Literal character
            nfa = NFAe(steps_display)
            start = State()
            accept = State()
            nfa.add_state(start, is_start=True)
            nfa.add_state(accept, is_accept=True)
            nfa.add_transition(start, char, accept)
            nfa_stack.append(nfa)
        elif char == '*':  # Kleene star
            nfa = nfa_stack.pop()
            start = State()
            accept = State()
            nfa.add_transition(start, "e", nfa.start_state)
            nfa.add_transition(start, "e", accept)
            for accept_state in nfa.accept_states:
                nfa.add_transition(accept_state, "e", nfa.start_state)
                nfa.add_transition(accept_state, "e", accept)

            nfa.add_state(start, is_start=True)
            nfa.reset_accept_states()
            nfa.add_state(accept, is_accept=True)
            nfa_stack.append(nfa)

        elif char == '|':  # Union
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            nfa = NFAe(steps_display)
            start = State()
            accept = State()
            nfa.add_state(start, is_start=True)
            nfa.add_state(accept, is_accept=True)
            nfa.add_transition(start, "e", nfa2.start_state)
            nfa.add_transition(start, "e", nfa1.start_state)
            for accept_state in nfa1.accept_states:
                nfa.add_transition(accept_state, "e", accept)
            for accept_state in nfa2.accept_states:
                nfa.add_transition(accept_state, "e", accept)
            nfa.states.update(nfa1.states)
            nfa.states.update(nfa2.states)
            nfa.transitions.update(nfa1.transitions)
            nfa.transitions.update(nfa2.transitions)
            nfa_stack.append(nfa)

        elif char == '.':  # Concatenation
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            for accept_state in nfa1.accept_states:
                nfa1.add_transition(accept_state, "e", nfa2.start_state)
            nfa1.states.update(nfa2.states)
            nfa1.transitions.update(nfa2.transitions)
            nfa1.accept_states = nfa2.accept_states
            nfa_stack.append(nfa1)

    return nfa_stack.pop()


def regex_to_postfix(regex):
    """
    Converts an infix regular expression to postfix (RPN).
    """
    precedence = {'|': 1, '.': 2, '*': 3}
    output = []
    operators = []

    def add_concat_operator(regex):
        """Add explicit concatenation operator '.' in regex."""
        result = []
        for i, token in enumerate(regex):
            result.append(token)
            if token not in '(|' and i + 1 < len(regex) and regex[i + 1] not in '|)*':
                result.append('.')
        return result

    regex = add_concat_operator(regex)

    for char in regex:
        if char.isalnum():  # Alphanumeric characters are treated as literals
            output.append(char)
        elif char == '(':
            operators.append(char)
        elif char == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()  # Remove '('
        else:  # Operator
            while (operators and operators[-1] != '(' and
                   precedence[operators[-1]] >= precedence[char]):
                output.append(operators.pop())
            operators.append(char)

    while operators:
        output.append(operators.pop())

    return ''.join(output)


def regex_to_nfae(regex, steps_display=True):
    """
    Converts a regular expression to an NFAe using the updated class.
    """
    postfix = regex_to_postfix(regex)
    return create_nfa(postfix, steps_display)


# Example Usage
if __name__ == "__main__":
    # regex = "01"
    # nfa = regex_to_nfae(regex, steps_display=True)
    # nfa.print_structure()
    # for state in nfa.states:
    #     print(state)
    steps_display = tk.Text(None, height=10, width=60, state="disabled")
    nfa = read_NFAe_from_file("test_1.txt", steps_display)
    print(nfa.accepts("0122"))
