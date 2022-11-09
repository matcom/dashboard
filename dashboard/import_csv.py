import pandas as pd
from models import JournalPaper, Journal, Person, ConferencePresentation
import Levenshtein

df = pd.read_csv("/src/data/publications.csv")

# Load authors

# for i, row in df.iterrows():
#     authors = row['Autores'].split('\n')

#     for author in authors:
#         person = Person(name=author, institution="-")

#         for p2 in Person.all():
#             if p2.name == person.name:
#                 break
#         else:
#             print(person)
#             person.save()

# Load papers

people = Person.all()

for i, row in df.iterrows():
    if row["Tipo"] not in ["Artículo publicado en proceeding de congreso", "Presentación en congreso (sin artículo)"]:
        continue

    title = row["Título"]
    authors = row["Autores"].split("\n")
    year = int(row["Fecha"].split("/")[-1])

    checked_authors = []

    for author_name in authors:
        best = max(people, key=lambda p: Levenshtein.ratio(p.name, author_name))
        checked_authors.append(best)

    url = row["URL"] if isinstance(row["URL"], str) else None

    print(url)

    paper = ConferencePresentation(
        title=title.strip(),
        authors=checked_authors,
        url=url,
        venue=row["Venue"].strip(),
        year=year,
        paper=row['Tipo'] == "Artículo publicado en proceeding de congreso"
    )

    print(paper)
    paper.save()
