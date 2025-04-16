from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from myapp.models import Autor, Libro

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "password": "testpass123",
        "email": "test@example.com",
    }


@pytest.fixture
def user(user_data):
    return User.objects.create_user(**user_data)


@pytest.fixture
def authenticated_api_client(api_client, user):
    # Obtener token JWT
    url = reverse("token_obtain_pair")
    response = api_client.post(
        url,
        {"username": user.username, "password": "testpass123"},
        format="json",
    )
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


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
    libro = Libro.objects.create(**libro_data)
    libro.autores.add(autor)
    libro.save()
    return libro


@pytest.mark.django_db
class TestAutorViewSet:
    def test_list_autores_unauthenticated(self, api_client, autor):
        url = reverse("autor-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_autores(self, authenticated_api_client, autor):
        url = reverse("autor-list")
        response = authenticated_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_autor_unauthenticated(self, api_client, autor_data):
        url = reverse("autor-list")
        response = api_client.post(url, autor_data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_autor(self, authenticated_api_client, autor_data):
        url = reverse("autor-list")
        response = authenticated_api_client.post(url, autor_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Autor.objects.count() == 1

    def test_retrieve_autor_unauthenticated(self, api_client, autor_data):
        autor = Autor.objects.create(**autor_data)
        url = reverse("autor-detail", args=[autor.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_autor(self, authenticated_api_client, autor_data):
        autor = Autor.objects.create(**autor_data)
        url = reverse("autor-detail", args=[autor.id])
        response = authenticated_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["nombre"] == autor_data["nombre"]

    def test_update_autor_unauthenticated(self, api_client, autor_data):
        autor = Autor.objects.create(**autor_data)
        url = reverse("autor-detail", args=[autor.id])
        updated_data = autor_data.copy()
        updated_data["nombre"] = "Gabriel José"
        response = api_client.put(url, updated_data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_autor(self, authenticated_api_client, autor_data):
        autor = Autor.objects.create(**autor_data)
        url = reverse("autor-detail", args=[autor.id])
        updated_data = autor_data.copy()
        updated_data["nombre"] = "Gabriel José"
        response = authenticated_api_client.put(url, updated_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["nombre"] == "Gabriel José"

    def test_delete_autor_unauthenticated(self, api_client, autor_data):
        autor = Autor.objects.create(**autor_data)
        url = reverse("autor-detail", args=[autor.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_autor(self, authenticated_api_client, autor_data):
        autor = Autor.objects.create(**autor_data)
        url = reverse("autor-detail", args=[autor.id])
        response = authenticated_api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Autor.objects.count() == 0


@pytest.mark.django_db
class TestLibroViewSet:
    def test_list_libros_unauthenticated(self, api_client, libro_data):
        Libro.objects.create(**libro_data)
        url = reverse("libro-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_libros(self, authenticated_api_client, libro_data):
        Libro.objects.create(**libro_data)
        url = reverse("libro-list")
        response = authenticated_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_libro_unauthenticated(self, api_client, libro_data):
        url = reverse("libro-list")
        response = api_client.post(url, libro_data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_libro(self, authenticated_api_client, libro_data):
        url = reverse("libro-list")
        response = authenticated_api_client.post(url, libro_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Libro.objects.count() == 1

    def test_retrieve_libro_unauthenticated(self, api_client, libro_data):
        libro = Libro.objects.create(**libro_data)
        url = reverse("libro-detail", args=[libro.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_libro(self, authenticated_api_client, libro_data):
        libro = Libro.objects.create(**libro_data)
        url = reverse("libro-detail", args=[libro.id])
        response = authenticated_api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["titulo"] == libro_data["titulo"]

    def test_update_libro_unauthenticated(self, api_client, libro_data):
        libro = Libro.objects.create(**libro_data)
        url = reverse("libro-detail", args=[libro.id])
        updated_data = libro_data.copy()
        updated_data["titulo"] = "El amor en los tiempos del cólera"
        response = api_client.put(url, updated_data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_libro(self, authenticated_api_client, libro_data):
        libro = Libro.objects.create(**libro_data)
        url = reverse("libro-detail", args=[libro.id])
        updated_data = libro_data.copy()
        updated_data["titulo"] = "El amor en los tiempos del cólera"
        response = authenticated_api_client.put(url, updated_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["titulo"] == "El amor en los tiempos del cólera"

    def test_delete_libro_unauthenticated(self, api_client, libro_data):
        libro = Libro.objects.create(**libro_data)
        url = reverse("libro-detail", args=[libro.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_libro(self, authenticated_api_client, libro_data):
        libro = Libro.objects.create(**libro_data)
        url = reverse("libro-detail", args=[libro.id])
        response = authenticated_api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Libro.objects.count() == 0
