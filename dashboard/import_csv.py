import pandas as pd
from models import JournalPaper, Person

df = pd.read_csv("/src/data/publications.csv")

for i, row in df.iterrows():
    authors = row['Autores'].split('\n')

    for author in authors:
        person = Person(name=author, institution="-")

        for p2 in Person.all():
            if p2.name == person.name:
                break
        else:
            print(person)
            person.save()
