from datetime import date

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from myapp.models import Autor, Libro


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def autor_data():
    return {
        "nombre": "Gabriel",
        "apellido": "García Márquez",
        "fecha_nacimiento": "1927-03-06",
        "biografia": "Escritor colombiano, premio Nobel de Literatura",
    }


@pytest.fixture
def libro_data():
    return {
        "titulo": "Cien años de soledad",
        "fecha_publicacion": "1967-05-30",
        "isbn": "9780307474728",
        "descripcion": "Una obra maestra de la literatura latinoamericana",
        "paginas": 417,
    }


@pytest.fixture
def autor(autor_data):
    return Autor.objects.create(**autor_data)


@pytest.fixture
def libro(libro_data, autor):
    libro = Libro.objects.new(**libro_data)
    libro.autores.append(autor)
    libro.save()
    return libro


@pytest.mark.django_db
class TestAutorViewSet:
    def test_list_autores(self, api_client, autor):
        url = reverse("autor-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_autor(self, api_client, autor_data):
        url = reverse("autor-list")
        response = api_client.post(url, autor_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Autor.objects.count() == 1

    def test_retrieve_autor(self, api_client, autor_data):
        autor = Autor.objects.create(**autor_data)
        url = reverse("autor-detail", args=[autor.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["nombre"] == autor_data["nombre"]

    def test_update_autor(self, api_client, autor_data):
        autor = Autor.objects.create(**autor_data)
        url = reverse("autor-detail", args=[autor.id])
        updated_data = autor_data.copy()
        updated_data["nombre"] = "Gabriel José"
        response = api_client.put(url, updated_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["nombre"] == "Gabriel José"

    def test_delete_autor(self, api_client, autor_data):
        autor = Autor.objects.create(**autor_data)
        url = reverse("autor-detail", args=[autor.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Autor.objects.count() == 0


@pytest.mark.django_db
class TestLibroViewSet:
    def test_list_libros(self, api_client, libro_data):
        Libro.objects.create(**libro_data)
        url = reverse("libro-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_libro(self, api_client, libro_data):
        url = reverse("libro-list")
        response = api_client.post(url, libro_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Libro.objects.count() == 1

    def test_retrieve_libro(self, api_client, libro_data):
        libro = Libro.objects.create(**libro_data)
        url = reverse("libro-detail", args=[libro.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["titulo"] == libro_data["titulo"]

    def test_update_libro(self, api_client, libro_data):
        libro = Libro.objects.create(**libro_data)
        url = reverse("libro-detail", args=[libro.id])
        updated_data = libro_data.copy()
        updated_data["titulo"] = "El amor en los tiempos del cólera"
        response = api_client.put(url, updated_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["titulo"] == "El amor en los tiempos del cólera"

    def test_delete_libro(self, api_client, libro_data):
        libro = Libro.objects.create(**libro_data)
        url = reverse("libro-detail", args=[libro.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Libro.objects.count() == 0
