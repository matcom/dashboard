from streamlit_agraph import agraph, Node, Edge, Config
from random import randint
import colorsys

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

def count_theses_between_two_advisors( theses, advisor_1, advisor_2 ) -> any:
    count = 0
    for thesis in theses:
        if advisor_1 in thesis.advisors and advisor_2 in thesis.advisors:
            count += 1
    return count

def darken_color(color:str, number:int, range:int) -> str:
    color = color.lstrip('#')
    
    h, l, s = colorsys.rgb_to_hls(*[int(color[i:i+2], 16)/255 for i in (0, 2, 4)])
    l = max(0.1, l - (number / range))
    return '#%02x%02x%02x' % tuple(int(i*255) for i in colorsys.hls_to_rgb(h, l, s))


def build_advisors_graph( advisors, theses ) -> any:
    
    nodes = []
    edges = []
    count_theses = count_theses_by_advisor( theses )
    max_theses = max(count_theses.values())

    for advisor in advisors:
        nodes.append(Node(
            id=advisor,
            label=advisor,
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