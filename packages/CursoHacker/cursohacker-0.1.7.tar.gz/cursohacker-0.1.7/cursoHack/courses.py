class Course:

    def __init__(self, name, duration, link):

        self.name = name
        self.duration = duration
        self.link = link

    def __repr__(self):

        return f"{self.name} [{self.duration}] horas [{self.link}]"

courses = [
    Course("Introducción al Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/"),
    Course("Personalización de Linux", 3, "https://hack4u.io/cursos/personalizacion-de-entorno-en-linux/"),
    Course("Introducción al Hacking", 53, "https://hack4u.io/cursos/introduccion-al-hacking/")
]

def list_courses():

    for course in courses:
        print(course)


class Vehiculo:

    def __init__(self, marca, modelo):

        self.marca = marca
        self.modelo = modelo

    def mostrar_informcion(self):

        return f"Marca : {self.marca}, Modelo: {self.modelo}"

class Coche(Vehiculo):

    def __init__(self, marca, modelo, tipo):

        super().__init__(marca, modelo)
        self.tipo = tipo

    def mostrar_informacion(self):

        super().mostrar_informacion()
        print(f"Tipo {self.tipo}")


def search_course_by_name(name):

    for course in courses:
        if course.name == name:
            return course

    return None


