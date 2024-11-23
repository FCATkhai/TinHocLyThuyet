# Xây dựng NFA
class NFA():
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_state:list = self.start_state

    def transition_to_state_with_input(self, input_value):
        print("state: ", self.current_state)
        temp_state = []
        for c_state in self.current_state:
            if (c_state, input_value) in self.transition_function.keys():
                state = self.transition_function[(c_state, input_value)]
                if isinstance(state, (int)):
                    if state not in temp_state:
                        temp_state.append(state)
                else:
                    temp_state += state 
        
        if len(temp_state) == 0:
            self.current_state = []
        else:
            self.current_state = temp_state.copy()
        return
        

    def in_accept_state(self):
        for c_state in self.current_state:
            if c_state in self.accept_states:
                return True
        return False

    def go_to_initial_state(self):
        self.current_state = self.start_state
        return

    def run_with_input_list(self, input_list):
        self.go_to_initial_state()
        for inp in input_list:
            self.transition_to_state_with_input(inp)

        return self.in_accept_state()

states = {0, 1, 2, 3 ,4}
alphabet = {'0', '1'}
start_state = [0]
accept_states = {2, 4}

tf = dict()
tf[(0, '0')] = [0, 3]
tf[(0, '1')] = [0, 1]
tf[(1, '1')] = 2
tf[(2, '0')] = 2
tf[(2, '1')] = 2
tf[(3, '0')] = 4
tf[(4, '0')] = 4
tf[(4, '1')] = 4
L = list('10111011')


nfa1 = NFA(states, alphabet, tf, start_state, accept_states)
print(nfa1.run_with_input_list(L))
