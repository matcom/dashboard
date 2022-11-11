import pandas as pd
from models import JournalPaper, Journal, Person, ConferencePresentation, Book, BookChapter
import Levenshtein

df = pd.read_csv("/src/data/profesores.csv")

people = Person.all()

matches = {
    'Jose Luis Castañeda Lorenzo' :  'José Luis Castañeda Lorenzo' ,
    'Ernesto Alejandro Lopez Cadalso' :  'Ernesto Alejandro López Cadalso' ,
    'Juan Pablo Consuegra Ayala' :  'Juan Pablo Consuegra Ayala' ,
    'Suilan Estevez Velarde' :  'Suilan Estévez Velarde' ,
    'Maria Elvira Fernandez Sa' :  'María Elvira Fernández Sa' ,
    'Alejandro Piad Morffis' :  'Alejandro Piad Morffis' ,
    'Carmen Teresa Fernandez Montoto' :  'Carmen Fernández' ,
    'Lucina Garcia Hernandez' :  'Lucina García' ,
    'Yudivian Almeida Cruz' :  'Yudivián Almeida Cruz' ,
    'Luciano Garcia Garrido' :  'Luciano García' ,
    'Alberto Fernandez Oliva' :  'Alberto Fernández ' ,
    'Joanna Campbell Amos' :  'Joanna Campbell Amos' ,
    'Juan Enrique Morales Calvo' :  'Juan Enrique Morales Calvo' ,
    'Aracelys Garcia Armenteros' :  'Aracelys García Armenteros' ,
    'Eduardo Quesada Orozco' :  'Eduardo Quesada Orozco' ,
    'Gemayqzel Bouza Allende' :  'Gemayqzel Bouza Allende' ,
    'Jose Alejandro Mesejo Chiong' :  'Jose A. Mesejo Chiong' ,
    'Damian Valdes Santiago' :  'Damian Valdés Santiago' ,
    'Fernando R. Rodriguez Flores' :  'Fernando Rodriguez Flores' ,
    'Elianys Garcia - Pola Cordoves' :  'Elianys García-Pola Cordobes' ,
    'Aymee De Los Angeles Marrero Severo' :  'Aymée Marrero Severo' ,
    'Julian Sarria Gonzalez' :  'Julián Sarría González' ,
    'Sofia Behar Jequin' :  'Sofía Behar Jequín' ,
    'Yanet Garcia Serrano' :  'Yanet Garcia Serrano' ,
    'Vivian Del R. Sistachs Vega' :  'Vivian del Rosario Sistachs Vega' ,
    'Carlos Narciso Bouza Herrera' :  'Carlos Bouza Herrera' ,
    'Sira Maria Allende Alonso' :  'Sira Allende Alonso' ,
    'Miraida Ferras Ferras' :  'Miraida Ferras Ferras' ,
    'Marta Lourdes Baguer Diaz Romanach' :  'Marta L. Baguer Diaz-Romanach' ,
    'Angela Mireya Leon Mecias' :  'Ángela Mireya León Mecías' ,
    'Frank Michel Enrique Hevia' :  'Frank Michel Enrique Hevia' ,
    'Wilfredo Morales Lezca' :  'Wilfredo Morales Lezca' ,
    'Marcel Ernesto Sanchez Aguilar' :  'Marcel Ernesto Sánchez Aguilar' ,
    'Jorge Estrada Hernandez' :  'Jorge Estrada Hernández' ,
    'Ernesto Luis Estevanell Valladares' :  'Ernesto Luis Estevanell Valladares' ,
    'Daniel Alejandro Valdes Perez' :  'Daniel Valdés Pérez' ,
    'Alejandro Roque Piedra' :  'Alejandro Roque Piedra' ,
    'Jose Fidel Hernandez Advincula' :  'José Fidel Hernández Advíncula' ,
    'Celia Tamara Gonzalez Gonzalez' :  'Celia T. González González' ,
    'Juan Carlos Lopez Realpozo' :  'Juan Pablo Consuegra Ayala' ,
    'Marleny Soler Martinez' :  'Marleny Soler Martínez' ,
    'Roxana Cabrera Puig' :  'Roxana Cabrera Puig' ,
    'Reynaldo Rodriguez Ramos' :  'Reinaldo Rodríguez Ramos' ,
    'Mariano Rodriguez Ricard' :  'Mariano Rodríguez Ricard' ,
    'Jose Enrique Valdes Castro' :  'Jose Enrique Valdes Castro' ,
    'Joaquin  Alberto Herrera Macias' :  'Joaquín Alberto Herrera Macías' ,
    'Lisset Suarez Plasencia' :  'Lisset Suárez Plasencia' ,
    'Yeneit Delgado Kios' :  'Yeneit Delgado Kios' ,
    'Ernesto Alejandro Borrego Rodriguez' :  'Ernesto Borrego Rodríguez' ,
}

for i, row in df.iterrows():
    name = row["Nombre"].title()
    department = row["Dpto"]
    academic_grade = row["Grado"]

    if name in matches:
        person = Person.find(name=matches[name])
    else:
        person = Person(name=name)

    person.institution="Universidad de La Habana"
    person.faculty = "Matemática y Computación"
    person.department = department
    person.scientific_grade = academic_grade

    print(person)
    person.save()
