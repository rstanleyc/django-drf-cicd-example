from rest_framework import serializers

from .models import Autor, Libro


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = "__all__"
        read_only_fields = ["id"]


class LibroSerializer(serializers.ModelSerializer):
    autores = AutorSerializer(many=True, read_only=True)

    class Meta:
        model = Libro
        fields = "__all__"
        read_only_fields = ["id"]
