from django import forms
from .models import Proyecto

class crearProyecto(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombreProyecto', 'nombreEstudiante', 'nombrePatrocinador', 'nombreTema']

class patrocinadorForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombrePatrocinador']
