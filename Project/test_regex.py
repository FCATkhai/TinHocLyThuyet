class NFAe:
    def __init__(self, steps_display):
        self.states = set()  # Set of states (Q)
        self.start_state = None  # Start state (q0)
        self.accept_states = set()  # Set of accept states (F)
        self.transitions = {}  # Transition function (δ)
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

    def print_structure(self):
        print("NFAe Structure:")
        for (from_state, symbol), to_states in self.transitions.items():
            for to_state in to_states:
                transition_type = "ε" if symbol is None else symbol
                print(f"State {from_state} --{transition_type}--> State {to_state}")
        print(f"Start State: {self.start_state}")
        print(f"Accept States: {self.accept_states}")


# Helper Class for Unique State Representation
class State:
    counter = 0

    def __init__(self):
        self.id = State.counter
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
            nfa.add_state(start, is_start=True)
            nfa.add_state(accept, is_accept=True)
            nfa.add_transition(start, None, nfa.start_state)
            for accept_state in nfa.accept_states:
                nfa.add_transition(accept_state, None, nfa.start_state)
                nfa.add_transition(accept_state, None, accept)
            nfa.start_state = start
            nfa.accept_states = {accept}
            nfa_stack.append(nfa)
        elif char == '|':  # Union
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            nfa = NFAe(steps_display)
            start = State()
            accept = State()
            nfa.add_state(start, is_start=True)
            nfa.add_state(accept, is_accept=True)
            nfa.add_transition(start, None, nfa1.start_state)
            nfa.add_transition(start, None, nfa2.start_state)
            for accept_state in nfa1.accept_states:
                nfa.add_transition(accept_state, None, accept)
            for accept_state in nfa2.accept_states:
                nfa.add_transition(accept_state, None, accept)
            nfa.states.update(nfa1.states)
            nfa.states.update(nfa2.states)
            nfa.transitions.update(nfa1.transitions)
            nfa.transitions.update(nfa2.transitions)
            nfa_stack.append(nfa)
        elif char == '.':  # Concatenation
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            for accept_state in nfa1.accept_states:
                nfa1.add_transition(accept_state, None, nfa2.start_state)
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
    regex = "01*|1"
    nfa = regex_to_nfae(regex, steps_display=True)
    nfa.print_structure()
