# Xây dựng DFA
class DFA(object):
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_state = start_state

    def transition_to_state_with_input(self, input_value):
        if ((self.current_state, input_value) not in self.transition_function.keys()):
            self.current_state = None
            return
        self.current_state = self.transition_function[(self.current_state, input_value)]
        return

    def in_accept_state(self):
        return self.current_state in self.accept_states

    def go_to_initial_state(self):
        self.current_state = self.start_state
        return

    def run_with_input_list(self, input_list):
        self.go_to_initial_state()
        for inp in input_list:
            self.transition_to_state_with_input(inp)

        return self.in_accept_state()


def dfa_file(filename):
    with open(filename, 'r') as f:
        L = f.readlines()
        states = set(map(int, L[0].split(',')))
        alphabet = set(L[1].strip().split(','))
        start_state = int(L[2])
        accept_states = set(map(int, L[3].split(',')))
        tf = {}
        for line in L[4:]:
            part = line.strip().split(',')
            state_from = int(part[0])
            char = part[1]
            state_to = int(part[2])
            tf[(state_from, char)] = state_to

        return DFA(states, alphabet, tf, start_state, accept_states)

L = list('1011101')
dfa1 = dfa_file(r"./DFA_sample.txt")

dfa1.go_to_initial_state()
print(dfa1.run_with_input_list(L))


states = {0, 1, 2}
alphabet = {'0', '1'}
start_state = 0
accept_states = {0}

tf = dict()
tf[(0, '0')] = 0
tf[(0, '1')] = 1
tf[(1, '0')] = 2
tf[(1, '1')] = 0
tf[(2, '0')] = 1
tf[(2, '1')] = 2

dfa1 = DFA(states, alphabet, tf, start_state, accept_states)