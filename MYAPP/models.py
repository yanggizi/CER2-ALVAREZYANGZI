from django.db import models

# Create your models here.

class Proyecto(models.Model):
    nombreProyecto=models.CharField(primary_key=True,max_length=50)
    nombreEstudiante=models.CharField(max_length=50)
    nombrePatrocinador=models.CharField(max_length=50)
    nombreTema=models.CharField(max_length=30)
    