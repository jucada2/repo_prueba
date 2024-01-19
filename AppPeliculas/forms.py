from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from AppPeliculas.models import Avatar

class SerieFormulario(forms.Form):
    nombre=forms.CharField()
    año=forms.IntegerField()
    temporadas=forms.IntegerField()

class PeliculaFormulario(forms.Form):
    nombre = forms.CharField(max_length=40)
    año = forms.IntegerField()
    director = forms.CharField(max_length=40)
    genero = forms.CharField(max_length=30)
    duracion = forms.FloatField()

class RegistrarUsuario(UserCreationForm):
    email = forms.EmailField(label="Correo electronico", help_text=None)
    password1 = forms.CharField(label="Ingrese la contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirme la contraseña ", widget=forms.PasswordInput)
    first_name = forms.CharField(label="Ingrese su nombre")
    last_name = forms.CharField(label="Ingrese su apellido")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "first_name", "last_name"]

class EditarPerfil(UserCreationForm):
    email = forms.EmailField(label="Correo electronico", help_text=None)
    password1 = forms.CharField(label="Ingrese la contraseña nueva ", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirme la contraseña nueva ", widget=forms.PasswordInput)
    first_name = forms.CharField(label="Ingrese su nombre")
    last_name = forms.CharField(label="Ingrese su apellido")

    class Meta:
        model = User
        fields = ["email", "password1", "password2", "first_name", "last_name"]

class AvatarFormulario(forms.ModelForm):

    class Meta:

        model = Avatar
        fields = ['usuario', 'imagen']