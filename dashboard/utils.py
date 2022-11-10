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
