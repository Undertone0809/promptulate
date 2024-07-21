from io import BytesIO
from typing import List

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
from pydantic import BaseModel, Field

# Fixed the matplotlib font display issue
matplotlib.use("Agg")


class Node(BaseModel):
    id: str = Field(..., title="ID")
    title: str = Field(..., title="Title")


class Edge(BaseModel):
    from_: str = Field(..., title="From", alias="from")
    to: str = Field(..., title="To")
    title: str = Field(..., title="Title")


class LLMResponse(BaseModel):
    nodes: List[Node] = Field(..., title="Nodes")
    edges: List[Edge] = Field(..., title="Edges")


def create_knowledge_graph(data: dict):
    G = nx.DiGraph()
    # Add nodes and specify the layer attribute for each node
    for node in data["nodes"]:
        # The node ID is the number of tiers
        layer = node["id"]
        G.add_node(node["id"], title=node["title"], layer=layer)
    # Add a directed edge
    for edge in data["edges"]:
        G.add_edge(edge["from_"], edge["to"], title=edge["title"])
    return G


def draw_graph(G):
    # With spring layout,
    # it can be arranged vertically according to the hierarchical properties of nodes
    pos = nx.spring_layout(G, weight="layer")
    fig, ax = plt.subplots(figsize=(12, 8))

    # Draw nodes, where squares are used to represent nodes
    nx.draw_networkx_nodes(G, pos, node_shape="s", node_color="skyblue", ax=ax)

    # Draw edge
    nx.draw_networkx_edges(
        G, pos, edge_color="gray", arrowstyle="->", arrowsize=15, ax=ax
    )

    # Draw node label
    labels = nx.get_node_attributes(G, "title")
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=12)

    # Draw the label of the edge
    edge_labels = nx.get_edge_attributes(G, "title")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, ax=ax)

    # Save the graph to a BytesIO object
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf


def read_summarize_prompt(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content
