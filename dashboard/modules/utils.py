
from random import randint
import colorsys

from models import Person
from uuid import UUID

def generate_widget_key() -> str:
    return str(randint(0, 1000000))


def count_theses_by_advisor( theses ) -> dict:
    advisors = {}

    for thesis in theses:
        for advisor in thesis.advisors:
            if advisor not in advisors:
                advisors[advisor] = 0
            advisors[advisor] += 1

    return advisors

def count_theses_between_two_advisors( theses, advisor_1, advisor_2 ) -> int:
    count = 0
    for thesis in theses:
        if advisor_1 in thesis.advisors and advisor_2 in thesis.advisors:
            count += 1
    return count

def count_publications_between_two_persons( publications, person_1: Person, person_2: Person ) -> int:
    count = 0
    for publication in publications:
        if person_1 in publication.authors and person_2 in publication.authors:
            count += 1
    return count

def count_publications_by_person( publications ) -> dict:
    count: dict[ UUID, int ] = {}
    
    for publication in publications:
        for author in publication.authors:
            if author.uuid  not in count:
                count[ author.uuid ] = 0
            count[ author.uuid ] += 1

    return count

def darken_color(color:str, number:int, range:int) -> str:
    color = color.lstrip('#')
    
    h, l, s = colorsys.rgb_to_hls(*[int(color[i:i+2], 16)/255 for i in (0, 2, 4)])
    l = max(0.1, l - (number / range))
    return '#%02x%02x%02x' % tuple(int(i*255) for i in colorsys.hls_to_rgb(h, l, s))
