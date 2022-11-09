import pandas as pd
from models import JournalPaper, Journal, Person, ConferencePresentation, Book, BookChapter
import Levenshtein

df = pd.read_csv("/src/data/publications.csv")

people = Person.all()

for i, row in df.iterrows():
    if row["Tipo"] not in ["Libro", "Capítulo de libro"]:
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

    if row['Tipo'] == "Libro":
        paper = Book(
            title=title.strip(),
            authors=checked_authors,
            url=url,
            publisher=row['Publisher'],
            year=year,
            isbn=row['Metadata'],
        )
    elif row['Tipo'] == 'Capítulo de libro':
        paper = BookChapter(
            chapter=title.strip(),
            title=row['Venue'],
            authors=checked_authors,
            url=url,
            publisher=row['Publisher'],
            year=year,
            isbn=row['Metadata'],
        )

    print(paper)
    paper.save()
