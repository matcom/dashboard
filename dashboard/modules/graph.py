from streamlit_agraph import agraph, Node, Edge, Config
from modules.utils import darken_color, count_theses_by_advisor, count_theses_between_two_advisors

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