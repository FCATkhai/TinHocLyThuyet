class State:
    state_counter = 0  # To give unique IDs to states

    def __init__(self):
        self.id = State.state_counter
        State.state_counter += 1
        self.transitions = {}  # Maps symbol to set of states (e.g., {'a': {state1, state2}})
        self.epsilon = set()  # Set of epsilon transitions (to other states)

    def __str__(self):
        return f"State({self.id})"


class NFAe:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept

    def print_structure(self):
        """
        Prints the structure of the NFAe.
        """
        visited = set()
        to_visit = [self.start]

        print("NFAe Structure:")
        while to_visit:
            state = to_visit.pop()
            if state in visited:
                continue
            visited.add(state)

            # Print transitions
            for symbol, states in state.transitions.items():
                for target in states:
                    print(f"State {state.id} --{symbol}--> State {target.id}")
                    if target not in visited:
                        to_visit.append(target)

            # Print epsilon transitions
            for target in state.epsilon:
                print(f"State {state.id} --ε--> State {target.id}")
                if target not in visited:
                    to_visit.append(target)

        print(f"Start State: {self.start.id}")
        print(f"Accept State: {self.accept.id}")


def regex_to_nfae(regex):
    """
    Converts a regular expression to an NFAε.
    """
    postfix = regex_to_postfix(regex)
    return create_nfa(postfix)


def regex_to_postfix(regex):
    """
    Converts infix regular expression to postfix (RPN).
    Supports: concatenation (implicit), union (|), and Kleene star (*).
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


def create_nfa(postfix):
    """
    Constructs an NFAe from a postfix regular expression.
    """
    stack = []

    for char in postfix:
        if char.isalnum():  # Literal character
            start = State()
            accept = State()
            start.transitions[char] = {accept}
            stack.append(NFAe(start, accept))
        elif char == '*':  # Kleene star
            nfa = stack.pop()
            start = State()
            accept = State()
            start.epsilon.add(nfa.start)
            start.epsilon.add(accept)
            nfa.accept.epsilon.add(nfa.start)
            nfa.accept.epsilon.add(accept)
            stack.append(NFAe(start, accept))
        elif char == '|':  # Union
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = State()
            accept = State()
            start.epsilon.add(nfa1.start)
            start.epsilon.add(nfa2.start)
            nfa1.accept.epsilon.add(accept)
            nfa2.accept.epsilon.add(accept)
            stack.append(NFAe(start, accept))
        elif char == '.':  # Concatenation
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1.accept.epsilon.add(nfa2.start)
            stack.append(NFAe(nfa1.start, nfa2.accept))

    return stack.pop()


# Example Usage
if __name__ == "__main__":
    regex = "b*"
    nfa = regex_to_nfae(regex)
    print("NFA constructed for regex:", regex)
    nfa.print_structure()
