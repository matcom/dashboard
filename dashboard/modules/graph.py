from streamlit_agraph import agraph, Node, Edge, Config
from modules.utils import darken_color, count_theses_by_advisor, count_theses_between_two_advisors

from typing import List, Tuple
from models import Person
from uuid import UUID

from random import randint
import streamlit as st

def build_advisors_graph( advisors, theses ) -> any:
    
    nodes = []
    edges = []
    count_theses = count_theses_by_advisor( theses )
    max_theses = max(count_theses.values())

    for advisor in advisors:
        nodes.append(Node(
            id=advisor,
            label=advisor,
            title=f"{advisor}\n{count_theses[ advisor ]} tesis",
            color=darken_color('#ACDBC9', count_theses[advisor], 2*max_theses),
            size=25 + count_theses[advisor] * 3,
        ))

    for thesis in theses:
        for advisor in thesis.advisors:
            for advisor_2 in thesis.advisors:
                if advisor == advisor_2:
                    continue 
                count_thesis = count_theses_between_two_advisors( theses, advisor, advisor_2 )
                edges.append( Edge(
                    source=advisor, 
                    label=f"{count_thesis} tesis",
                    target=advisor_2,
                    color=darken_color('#52FFCC', count_thesis, max_theses ),
                    directed=False,
                    collapsible=False
                ))

    config = Config( width=900, height=700 )
    return agraph(nodes=nodes, edges=edges, config=config)

class NodeGraph:
    def __init__(self, info: Person) -> None:
        self.info = info
        self.color = '#ACDBC9'
        self.size = 25

class EdgeGraph:
    def __init__(self, source:NodeGraph, target:NodeGraph, info) -> None:
        self.source = source
        self.target = target
        self.info = info
        self.color = '#ACDBC9'

def build_nodes_and_edges( publications: any ) -> Tuple[ List[NodeGraph], List[EdgeGraph] ]:
    all_nodes: dict[UUID, Person] = {}
    nodes: List[NodeGraph] = []
    edges: List[EdgeGraph] = []
    
    for publication in publications:
        # save nodes
        for author in publication.authors:
            if author.uuid not in all_nodes:
                nn = NodeGraph(author)
                all_nodes[ author.uuid ] = nn
                nodes.append( nn )

        # save edges 
        for i in range( len(publication.authors) ):
            author = publication.authors[i]
            for j in range(i + 1, len(publication.authors)):
                author_2 = publication.authors[j]
                edges.append(EdgeGraph(all_nodes[author.uuid], all_nodes[author_2.uuid], publication))

    del all_nodes
    return (nodes, edges)

def build_publications_graph( publications: List[any], width = 900, height = 700 ) -> any:
    nodesGraph, edgesGraph = build_nodes_and_edges( publications )
    nodes: List[Node] = []
    edges: List[Edge] = []

    for node in nodesGraph:
        nodes.append(Node( 
            id=f"{node.info.uuid}",
            label=node.info.name,
            title=node.info.name,
            color=node.color,
            size=25
        ))
        
    for edge in edgesGraph:
        edges.append(Edge(
            source=f"{edge.source.info.uuid}", 
            label=f"{5} publicación",
            target=f"{edge.target.info.uuid}",
            color=edge.color,
            directed=False,
            collapsible=False
        ))
        edges.append(Edge(
            source=f"{edge.target.info.uuid}", 
            label=f"{5} publicación",
            target=f"{edge.source.info.uuid}",
            color=edge.color,
            directed=False,
            collapsible=False
        ))

    config = Config( width=width, height=height )
    return agraph(nodes=nodes, edges=edges, config=config)
