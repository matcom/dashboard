import itertools

rows = ["A", "B", "C", "D"]
left = list(range(2, 16, 1))
right = list(range(17, 31, 1))

sits = []

while True:
    if left:
        sits.append(left.pop(0))

    if left:
        sits.append(left.pop(0))

    if right:
        sits.append(right.pop(0))

    if right:
        sits.append(right.pop(0))

    if not left and not right:
        break

names = [
    "Carmen Irene Cabrera Rodríguez",
    "Ana Paula Argüelles Terrón",
    "Pedro Alejandro Rodríguez San Pedro",
    "Omar Alejandro Hernández Ramírez",
    "Marco Alejandro Torres Bobadilla",
    "Marcos Adrián Valdivié Rodríguez",
    "Jean Pierre Gómez Matos",
    "Javier Alejandro Lopetegui González",
    "Javier Rodríguez Rodríguez",
    "Jorge Junior Morgado Vega",
    "Jorge Mederos Alvarado",
    "Leyanis Falcon Hernández",
    "Verónica Medina Rodríguez",
    "Manuel Antonio Vilas Valiente",
    "Andy Gabriel Rodríguez Alfonso",
    "Amalia Nilda Ibarra Rodríguez",
    "Darian Ramón Mederos",
    "Javier Díaz Martín",
    "Aldo Javier Verdesia Delgado",
    "Ernesto Lima Cruz",
    "Yordan Rodríguez Rosales",
    "Iván Ernesto Ernand Hernández",
    "William Martin Andrés",
    "Andy Ledesma García",
    "Carlos Toledo Silva",
    "Abel Molina Sánchez",
    "Bryan Machín García",
    "Rocio Ortiz Gancedo",
    "Ariel Alfonso Triana Pérez",
    "Sheila Artiles Fagundo",
    "Roberto García Rodríguez",
    "Adrianna Alvarez Lorenzo",
    "Andrés Alejandro León Almaguer",
    "Juan Pablo Madrazo Vazquez",
    "Henri Daniel Peña Dequero",
    "Alejandro Escobar Giraudy",
    "Grettel Hernández Garbey",
    "Frank Abel Blanco Gómez",
    "David Orlando de Quesada Oliva",
    "Karel Díaz Vergara",
    "Alben Luis Urquiza Rojas",
    "Gustavo Despaigne Dita",
    "Miguel Alejandro Rodríguez Hernández",
    "Airelys Collazo Perez",
    "Javier Enrique Domínguez Hernández",
    "José Alejandro Solís Fernández",
    "Arnel Sánchez Rodríguez",
    "David Campanería Cisneros",
    "Frank Adrian Pérez Morales",
    "Camilo Rodríguez Velázquez",
    "Victor Manuel Lantigua Cano",
    "Dayron Fernández Acosta",
    "Julio José Horta Vázquez",
    "David Guaty Domínguez",
    "Enrique Martínez González",
    "Karla Olivera Hernández",
    "Adrian Rodríguez Portales",
    "Victor Manuel Cardentey Fundora",
    "Claudia Olavarrieta Martínez",
    "Javier Alejandro Campos Matanzas",
    "Luis Ernesto Ibarra Vázquez",
    "Osmany Pérez Rodríguez",
    "Abel Antonio Cruz Suárez",
    "Rodrigo Daniel Pino Trueba",
    "Enmanuel Verdesia Suárez",
    "Carlos Alejandro Arrieta Montes de Oca",
    "Ariel Antonio Huerta Martín",
    "Miguel Alejandro Asin Barthelemy",
    "Gabriel Fernando Martín Fernández",
    "Darian Dominguez Alayón",
    "Richard García de la Osa",
    "Thalia Blanco Figueras",
    "Daniel Orlando Ortiz Pacheco",
    "Olivia González Peña",
    "Ariel Plasencia Díaz",
    "Luis Enrique Dalmau Coopat",
    "Amanda  González Borrell",
    "Javier Alejandro Valdés González",
    "Sandra Martos Llanes",
    "José Carlos Hernández Piñera",
    "Laura Brito Guerrero",
    "Samuel David Suárez Rodríguez",
    "Adrián Hernández Pérez",
    "Daniel Reynel Domínguez Ceballos",
    "Yan Carlos González Blanco",
    "Nadia González Fernández",
    "Juan Carlos Casteleiro Wong",
    "Gelin Eguinosa Rosique",
    "Sheyla Cruz Castro",
    "Rodrigo García Gómez",
    "Luis Alejandro Lara Rojas",
    "Laura Tamayo Blanco",
    "Juan José López Martínez",
    "Damian O'Hallorans Toledo",
    "Henry Estévez Gómez",
    "Eduardo Moreira González",
    "Reinaldo Barrera Travieso",
    "Yasmin Milagro Cisneros Cimadevila",
    "Yandy Sanchez Orosa",
    "Tony Raúl Blanco Fernández",
    "Jessy Gigato Izquierdo",
    "José Alejandro Labourdette Lartigue Soto",
    "Yadiel Felipe Medina",
    "Eziel Christian Ramos Piñon",
    "Pablo Adrián Fuentes González",
]

with open("/home/apiad/graduacion.csv", "w") as fp:
    for name, (row, sit) in zip(names, itertools.product(rows, sits)):
        fp.write(f"{name},{row}-{sit}\n")
