from NFAe import NFAe


def read_nfa_from_file(filename):
    nfa = NFAe()
    with open(filename, 'r') as file:
        lines = file.readlines()
        initial_state_line, accept_states_line, *transitions_lines = map(str.strip, lines)

        start_state = initial_state_line.split()[1]
        nfa.add_state(start_state, is_start=True)

        accept_states = accept_states_line.split()[1:]
        for state in accept_states:
            nfa.add_state(state, is_accept=True)

        for transition in transitions_lines:
            from_state, symbol, to_state = transition.split()
            nfa.add_transition(from_state, symbol, to_state)

    return nfa


nfa1 = read_nfa_from_file("test_2_01Sao+1.txt")
#
print(nfa1.accepts("0012"))
