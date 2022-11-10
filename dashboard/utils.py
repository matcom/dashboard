from streamlit_agraph import agraph, Node, Edge, Config
from random import randint

def generate_widget_key() -> str:
    return str(randint(0, 1000000))


def count_theses_by_advisor( theses ) -> any:
    advisors = {}

    for thesis in theses:
        for advisor in thesis.advisors:
            if advisor not in advisors:
                advisors[advisor] = 0
            advisors[advisor] += 1

    return advisors

def build_tutors_graph( advisors, theses ) -> any:
    
    nodes = []
    edges = []
    count_theses = count_theses_by_advisor( theses )

    for advisor in advisors:
        nodes.append(Node(
            id=advisor,
            size=25 + count_theses[advisor] * 3,
        ))

    for thesis in theses:
        for advisor in thesis.advisors:
            for advisor_2 in thesis.advisors:
                if advisor == advisor_2:
                    continue 
                edges.append( Edge(
                    source=advisor, 
                    label=thesis.title, 
                    target=advisor_2,
                    directed=False,
                    collapsible=False
                ))

    config = Config( width=1000, height=700 )

    return agraph(nodes=nodes, edges=edges, config=config)
