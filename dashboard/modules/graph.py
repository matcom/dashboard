from streamlit_agraph import agraph, Node, Edge, Config
from modules.utils import darken_color, count_theses_by_advisor, count_theses_between_two_advisors

from typing import List, Tuple

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

def build_nodes_and_edges( publications: any ) -> Tuple[ List[Node], List[Edge] ]:
    is_nodes = {}
    nodes = []
    edges = []
    for publication in publications:
        for author in publication.authors:
            if author.name not in is_nodes:
                is_nodes[author.name] = True
                nodes.append( 
                    Node(
                    id=author.name,
                    label=author.name,
                    title=author.name,
                    color='#ACDBC9',
                    size=25,
                ))

            for author_2 in publication.authors:
                if author != author_2:
                    edges.append( 
                        Edge(
                            source=author.name, 
                            label="1",
                            target=author_2.name,
                            color='#52FFCC',
                            directed=False,
                            collapsible=False
                        ))
    del is_nodes
    return ( nodes, edges )


def build_publications_graph( publications: any ) -> any:

    nodes, edges = build_nodes_and_edges( publications )

    config = Config( width=900, height=700 )
    
    return agraph(nodes=nodes, edges=edges, config=config)
