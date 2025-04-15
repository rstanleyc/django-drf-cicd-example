from django.db import models

# Create your models here.


class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    biografia = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name_plural = "Autores"


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autores = models.ManyToManyField(Autor, related_name="libros")
    fecha_publicacion = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    descripcion = models.TextField(blank=True)
    paginas = models.PositiveIntegerField()

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "Libros"
