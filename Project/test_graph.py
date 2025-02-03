import pygraphviz as pgv

# Create a new graph
G = pgv.AGraph(strict=True, directed=True)

# Add nodes
G.add_node("A", label="Start")
G.add_node("B", label="Decision")
G.add_node("C", label="End")

# Add edges
G.add_edge("A", "B", label="Path 1")
G.add_edge("B", "C", label="Path 2")

# Layout and render the graph
G.layout(prog="dot")  # Use the Graphviz "dot" layout engine
G.draw("example_graph.png")  # Save as PNG

print("Graph saved as example_graph.png")
