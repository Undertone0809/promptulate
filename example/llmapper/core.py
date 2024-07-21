from io import BytesIO
from typing import List, Optional

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import pne
from prompt import summary_prompt
from pydantic import BaseModel, Field

# Fixed the matplotlib font display issue
matplotlib.use("Agg")


class AppConfig:
    model_name: Optional[str] = None
    api_key: Optional[str] = None
    api_base: Optional[str] = None


class Node(BaseModel):
    id: str = Field(..., title="ID")
    title: str = Field(..., title="Title")


class Edge(BaseModel):
    from_: str = Field(..., title="From", alias="from")
    to: str = Field(..., title="To")
    title: str = Field(..., title="Title")


class Graph(BaseModel):
    nodes: List[Node] = Field(..., title="Nodes")
    edges: List[Edge] = Field(..., title="Edges")


def create_knowledge_graph(graph: Graph):
    graph: dict = graph.model_dump()
    G = nx.DiGraph()

    for node in graph["nodes"]:
        layer = node["id"]
        G.add_node(node["id"], title=node["title"], layer=layer)

    for edge in graph["edges"]:
        G.add_edge(edge["from_"], edge["to"], title=edge["title"])

    return G


def draw_graph(G):
    pos = nx.spring_layout(G, weight="layer")
    fig, ax = plt.subplots(figsize=(12, 8))

    nx.draw_networkx_nodes(G, pos, node_shape="s", node_color="skyblue", ax=ax)
    nx.draw_networkx_edges(
        G, pos, edge_color="gray", arrowstyle="->", arrowsize=15, ax=ax
    )

    # Draw node label
    labels = nx.get_node_attributes(G, "title")
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=12)

    # Draw the label of the edge
    edge_labels = nx.get_edge_attributes(G, "title")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, ax=ax)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    return buf


def generate_nodes(query_result: str, app_config: AppConfig) -> Graph:
    _prompt = f"""
    Please generate a knowledge graph based on the requirements of {summary_prompt}
    and the content of {query_result}
    """

    return pne.chat(
        model=app_config.model_name,
        messages=_prompt,
        model_config={"api_base": app_config.api_base, "api_key": app_config.api_key},
        output_schema=Graph,
    )
