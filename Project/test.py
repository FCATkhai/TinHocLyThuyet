import os
import tkinter as tk
from tkinter import filedialog, messagebox
from graphviz import Digraph
from PIL import Image, ImageTk
from NFAe import NFAe

# # Create a directed graph
# dot = Digraph()
#
# # Add nodes
# dot.node('A', 'Start')
# dot.node('B', 'Decision')
# dot.node('C', 'End')
#
# # Add edges
# dot.edge('A', 'B', label='Path 1')
# dot.edge('B', 'C', label='Path 2')
#
# # Render graph (view=True opens the output file)
# dot.render('example_graph', format='png', view=True)




def read_nfa_from_file(filename, steps_display):
    nfae = NFAe(steps_display)
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


def draw_nfae(nfae):
    dot = Digraph(format="png")
    dot.attr(rankdir="LR")

    for state in nfae.states:
        if state in nfae.accept_states:
            dot.node(state, shape="doublecircle")
        else:
            dot.node(state, shape="circle")

    dot.node("start", shape="point")
    dot.edge("start", nfae.start_state)

    for (from_state, symbol), to_state in nfae.transitions.items():
        print(to_state)
        label = "ε" if symbol == "e" else symbol
        dot.edge(from_state, to_state, label=label)

    output_file = r"./diagram"
    try:
        dot.render(output_file, view=True, cleanup=True)
        return output_file + ".png"
    except Exception as e:
        print("Lỗi vẽ đồ thị: ", e)
        return None


nfae = read_nfa_from_file("test_1.txt", None)
draw_nfae(nfae)