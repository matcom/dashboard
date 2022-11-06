from random import randint

def generate_widget_key() -> str:
    return str(randint(0, 1000000))
