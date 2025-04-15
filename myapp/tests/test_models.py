from datetime import date

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from myapp.models import Autor, Libro


@pytest.mark.django_db
class TestAutorModel:
    def test_crear_autor(self):
        autor = Autor.objects.create(
            nombre="Gabriel",
            apellido="García Márquez",
            fecha_nacimiento=date(1927, 3, 6),
            biografia="Escritor colombiano, premio Nobel de Literatura",
        )
        assert autor.nombre == "Gabriel"
        assert autor.apellido == "García Márquez"
        assert str(autor) == "Gabriel García Márquez"

    def test_autor_sin_fecha_nacimiento(self):
        autor = Autor.objects.create(nombre="Gabriel", apellido="García Márquez")
        assert autor.fecha_nacimiento is None
        assert autor.biografia == ""

    def test_autor_nombre_max_length(self):
        with pytest.raises(ValidationError):
            autor = Autor(
                nombre="a" * 101,  # Más del límite de 100 caracteres
                apellido="García Márquez",
            )
            autor.full_clean()

    def test_autor_apellido_max_length(self):
        with pytest.raises(ValidationError):
            autor = Autor(
                nombre="Gabriel", apellido="a" * 101  # Más del límite de 100 caracteres
            )
            autor.full_clean()


@pytest.mark.django_db
class TestLibroModel:
    @pytest.fixture
    def autor(self):
        return Autor.objects.create(nombre="Gabriel", apellido="García Márquez")

    def test_crear_libro(self, autor):
        libro = Libro.objects.create(
            titulo="Cien años de soledad",
            fecha_publicacion=date(1967, 5, 30),
            isbn="9780307474728",
            descripcion="Una obra maestra de la literatura latinoamericana",
            paginas=417,
        )
        libro.autores.add(autor)

        assert libro.titulo == "Cien años de soledad"
        assert libro.isbn == "9780307474728"
        assert libro.paginas == 417
        assert str(libro) == "Cien años de soledad"
        assert autor in libro.autores.all()

    def test_libro_sin_descripcion(self, autor):
        libro = Libro.objects.create(
            titulo="Cien años de soledad",
            fecha_publicacion=date(1967, 5, 30),
            isbn="9780307474728",
            paginas=417,
        )
        libro.autores.add(autor)
        assert libro.descripcion == ""

    def test_libro_titulo_max_length(self, autor):
        with pytest.raises(ValidationError):
            libro = Libro(
                titulo="a" * 201,  # Más del límite de 200 caracteres
                fecha_publicacion=date(1967, 5, 30),
                isbn="9780307474728",
                paginas=417,
            )
            libro.full_clean()

    def test_libro_isbn_unico(self, autor):
        Libro.objects.create(
            titulo="Cien años de soledad",
            fecha_publicacion=date(1967, 5, 30),
            isbn="9780307474728",
            paginas=417,
        )
        with pytest.raises(IntegrityError):
            Libro.objects.create(
                titulo="El amor en los tiempos del cólera",
                fecha_publicacion=date(1985, 1, 1),
                isbn="9780307474728",  # ISBN duplicado
                paginas=368,
            )

    def test_libro_paginas_positivas(self, autor):
        with pytest.raises(ValidationError):
            libro = Libro(
                titulo="Cien años de soledad",
                fecha_publicacion=date(1967, 5, 30),
                isbn="9780307474728",
                paginas=-1,  # Número negativo de páginas
            )
            libro.full_clean()
