from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pelicula(models.Model):  
    nombre = models.CharField(max_length=40)
    año = models.IntegerField()
    director = models.CharField(max_length=40)
    genero = models.CharField(max_length=30)
    duracion = models.FloatField()

    def __str__(self):

        return f"{self.nombre} --- {self.año}"
    
class Serie(models.Model):

    def __str__(self):

        return f"{self.nombre} --- {self.año}"

    nombre = models.CharField(max_length=40)
    año = models.IntegerField()
    temporadas = models.IntegerField()

class Futbol(models.Model):
    equipo_local = models.CharField(max_length=40)
    equipo_visitante = models.CharField(max_length=40)
    resultado = models.CharField(max_length=40)
    fecha = models.DateField()


class Avatar(models.Model):
    #foreignKey
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    #Atributo
    imagen = models.ImageField(upload_to="avatares", null=True, blank=True)

    def __str__(self):

        return f"{self.usuario} --- {self.imagen}"
    