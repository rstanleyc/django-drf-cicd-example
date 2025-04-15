from django.contrib import admin

from .models import Autor, Libro


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "fecha_nacimiento")
    search_fields = ("nombre", "apellido")
    list_filter = ("fecha_nacimiento",)


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "fecha_publicacion", "isbn", "paginas")
    search_fields = ("titulo", "isbn")
    list_filter = ("fecha_publicacion", "autores")
    filter_horizontal = ("autores",)
