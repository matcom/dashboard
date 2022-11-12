from streamlit_agraph import agraph, Node, Edge, Config
from modules.utils import darken_color, count_theses_by_advisor, count_theses_between_two_advisors
from modules.utils import count_publications_by_person, count_publications_between_two_persons

from typing import List, Tuple
from models import Person
from uuid import UUID

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
    def __init__(self, info: Person, size = 25, color = '#ACDBC9') -> None:
        self.info = info
        self.color = color
        self.size = size

class EdgeGraph:
    def __init__(self, source:NodeGraph, target:NodeGraph, info, color='#ACDBC9') -> None:
        self.source = source
        self.target = target
        self.info = info
        self.color = color

def build_nodes_and_edges( publications: any ) -> Tuple[ List[NodeGraph], List[EdgeGraph] ]:
    all_nodes: dict[UUID, Person] = {}
    nodes: List[NodeGraph] = []
    edges: List[EdgeGraph] = []
    publications_by_person = count_publications_by_person( publications )
    
    for publication in publications:
        # save nodes
        for author in publication.authors:
            if author.uuid not in all_nodes:
                nn = NodeGraph(author, 25 + 5*publications_by_person[author.uuid])
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
    publ_by_person = count_publications_by_person( publications )
    
    for node in nodesGraph:
        publ = f"{publ_by_person[ node.info.uuid ]} {'publicación' if publ_by_person[node.info.uuid] == 1 else 'publicaciones'}"
        nodes.append(Node( 
            id=f"{node.info.uuid}",
            title=f"{node.info.name}\n{publ}",
            label=node.info.name,
            color=node.color,
            size=node.size
        ))
        
    for edge in edgesGraph:
        count_pub = count_publications_between_two_persons( publications, edge.source.info, edge.target.info )
        edges.append(Edge(
            source=f"{edge.source.info.uuid}", 
            label=f"{count_pub} {'publicación' if count_pub == 1 else 'publicaciones'}",
            target=f"{edge.target.info.uuid}",
            color=edge.color,
            directed=False,
            collapsible=False
        ))
        edges.append(Edge(
            source=f"{edge.target.info.uuid}", 
            target=f"{edge.source.info.uuid}",
            label="",
            color=edge.color,
            directed=False,
            collapsible=False
        ))

    config = Config( width=width, height=height )
    return agraph(nodes=nodes, edges=edges, config=config)
