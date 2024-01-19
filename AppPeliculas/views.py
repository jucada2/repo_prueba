from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from AppPeliculas.models import Serie, Pelicula, Futbol, Avatar
from AppPeliculas.forms import SerieFormulario, PeliculaFormulario, RegistrarUsuario, EditarPerfil, AvatarFormulario

# Create your views here.

def agregar_avatar(request):
    if request.method=="POST":

        mi_formulario = AvatarFormulario(request.POST, request.FILES)

        if mi_formulario.is_valid():
            info=mi_formulario.cleaned_data
            usuario_actual = User.objects.get(username=request.user)
            avatar_nuevo = Avatar(usuario=usuario_actual, imagen=info["imagen"])
            avatar_nuevo.save()
            print(request.user.avatar_set.first)
            return render(request, "AppPeliculas/inicio.html")
    
    else:

        mi_formulario = AvatarFormulario()
    
    return render(request, "AppPeliculas/avatares.html", {"formu":mi_formulario})

def inicio(request):

    return render(request, "AppPeliculas/inicio.html")


# Vistas de register/login/logout
def inicio_sesion(request):

    if request.method == "POST": #Si el usuario hace click en el botón
            
        formulario = AuthenticationForm(request, data = request.POST)  #obtener la información (usuario y contraseña) del formulario

        if formulario.is_valid():
                
                info = formulario.cleaned_data #la información que puso el usuario se pasa a diccionario

                usuario = info["username"]
                contra = info["password"]

                usuario_actual = authenticate(username=usuario, password=contra) #comprobar si es que el usuario existe

                if usuario_actual is not None: #si el usuario actual es "algo" (encontró un usuario)
                    login(request, usuario_actual) #iniciar sesión con ese usuario
                    
                    return render(request,"AppPeliculas/inicio.html",  {"mensaje":f"Bienvenido {usuario}"} )
                
        else: #el usuario es None y el formulario no ha sido valido (no ha encontrado un usuario con los datos brindados)
            
            return render(request,"AppPeliculas/inicio.html", {"mensaje":"Error, datos incorrectos"} )

    else:
        
        formulario = AuthenticationForm()

    return render(request, "registro/inicio_sesion.html", {"formu":formulario})



def registro(request):

    if request.method == "POST": #si le doy click a registrarse

        formulario = RegistrarUsuario(request.POST) #tengo la información

        if formulario.is_valid():

            info = formulario.cleaned_data

            usuario = info["first_name"] #obtener el nombre de usuario con el que se registro

            formulario.save() #ya te crea el usuario en la base de datos!!!!

            return render(request, "AppPeliculas/inicio.html", {"mensaje":f"Bienvenido {usuario}"} )

    else:   
        formulario = RegistrarUsuario()

    return render(request, "registro/registrar_usuario.html", {"formu":formulario})



def editar_perfil(request):

    usuario_actual = request.user

    if request.method=="POST":
        mi_formulario = EditarPerfil(request.POST)

        if mi_formulario.is_valid():

            info = mi_formulario.cleaned_data

            usuario_actual.email = info["email"]
            usuario_actual.first_name = info["first_name"]
            usuario_actual.last_name = info["last_name"]
            usuario_actual.set_password(info["password1"])
            usuario_actual.save()

            return render(request, "AppPeliculas/inicio.html")
        
    else:
        mi_formulario = EditarPerfil(initial={"email":usuario_actual.email,
                                                  "first_name":usuario_actual.first_name,
                                                  "last_name":usuario_actual.last_name})

    return render(request,"registro/editar_perfil.html", {"formu":mi_formulario, "usuario":usuario_actual})


def cerrar_sesion(request):
    logout(request)

    return render(request, "registro/cerrar_sesion.html")

#CRUD de Serie (Vistas basadas en funciones)

# C (Create) del CRUD de Series
def agregar_serie(request):
    
    #Depende de darle click al botón enviar o guardar

    if request.method == "POST":

        nuevo_formulario = SerieFormulario(request.POST) #obtener los datos del formulario HTML

        if nuevo_formulario.is_valid():

            info = nuevo_formulario.cleaned_data #para tenerlos en modo diccionario

            serie_nueva = Serie(nombre=info["nombre"], año=info["año"], temporadas=info["temporadas"])

            serie_nueva.save()

            return render(request, "AppPeliculas/inicio.html") #muestrame la plantilla de inicio luego de guardar la info!!!
    
    else: #si la persona no la ha hecho click al botón enviar

        nuevo_formulario  = SerieFormulario() #mostraremos un formulario vacio

    return render(request, "AppPeliculas/formu_serie.html", {"mi_formu":nuevo_formulario})


#R (Read) del CRUD de Series
@login_required #es un decorador!!! --- agregar funcionalidades a mi vista
def ver_serie(request):

    mis_series = Serie.objects.all() #obtener todos los datos en mi tabla Serie

    info = {"series":mis_series}

    return render(request, "AppPeliculas/series.html", info)


#U (Update) del CRUD de Series
def actualizar_serie(request, serie_nombre):
    
    #¿¿qué serie quiero actualizar?? 
    serie_escogida = Serie.objects.get(nombre=serie_nombre) #encuentro la serie a actualizar

    #Depende de darle click al botón actualizar
    if request.method == "POST":

        nuevo_formulario = SerieFormulario(request.POST) #obtener los datos del formulario HTML

        if nuevo_formulario.is_valid():

            info = nuevo_formulario.cleaned_data #para tenerlos en modo diccionario
            
            #actualizar los datos de la serie escogida
            serie_escogida.nombre = info["nombre"]
            serie_escogida.año = info["año"]
            serie_escogida.temporadas = info["temporadas"]

            serie_escogida.save()

            return render(request, "AppPeliculas/inicio.html") #muestrame la plantilla de inicio luego de guardar la info!!!
    
    else: #si la persona no la ha hecho click al botón enviar

        nuevo_formulario  = SerieFormulario(initial={"nombre":serie_escogida.nombre, 
                                                     "año":serie_escogida.año, 
                                                     "temporadas":serie_escogida.temporadas}) #mostraremos un formulario vacio

    return render(request, "AppPeliculas/update_serie.html", {"mi_formu":nuevo_formulario})


#D (Delete) del CRUD de Series

def eliminar_serie(request, serie_nombre):

    #¿¿qué serie quiero eliminar?? 
    serie_escogida = Serie.objects.get(nombre=serie_nombre) #encuentro la serie a eliminar

    serie_escogida.delete() #eliminando la serie escogida

    return render(request, "AppPeliculas/series.html")


"""
def ver_pelis(request):

    mis_pelis = Serie.objects.all() #obtener todos los datos en mi tabla Serie

    info = {"pelis":mis_pelis}

    return render(request, "AppPeliculas/peliculas.html", info)
"""
    
@login_required
def ver_partidos(request):

    mis_partidos = Futbol.objects.all() #obtener todos los datos en mi tabla Serie

    info = {"partidos":mis_partidos}

    return render(request, "AppPeliculas/partidos.html", info)


def agregar_pelicula(request):
    
    #Depende de darle click al botón enviar o guardar

    if request.method == "POST":

        nuevo_formulario = PeliculaFormulario(request.POST) #obtener los datos del formulario HTML

        if nuevo_formulario.is_valid():

            info = nuevo_formulario.cleaned_data #para tenerlos en modo diccionario

            peli_nueva = Pelicula(nombre=info["nombre"], año=info["año"], director=info["director"],
                                  genero=info["genero"], duracion=info["duracion"])

            peli_nueva.save()

            return render(request, "AppPeliculas/inicio.html") #muestrame la plantilla de inicio luego de guardar la info!!!
    
    else: #si la persona no la ha hecho click al botón enviar

        nuevo_formulario  = PeliculaFormulario() #mostraremos un formulario vacio

    return render(request, "AppPeliculas/formu_peli.html", {"mi_formu":nuevo_formulario})


def busqueda_serie_por_año(request):

    return render(request, "AppPeliculas/buscar_serie_año.html")


def resultados_buscar_serie_año(request):

    if request.method=="GET":

        año_pedido = request.GET["año"]
        resultados_series = Serie.objects.filter(año__icontains=año_pedido)


        return render(request, "AppPeliculas/buscar_serie_año.html", {"series":resultados_series})

    else:
        return render(request, "AppPeliculas/buscar_serie_año.html")


#CRUD de Partidos de Futbol (Vistas basadas en Clases)

#R (Read) de Partidos --- ListView

class ListaPartidos(ListView): 

    model = Futbol
    #nombre por defecto: futbol_list.html
    template_name = "AppPeliculas/partidos/lista_de_partidos.html"


class DetallePartidos(DetailView):

    model = Futbol
    template_name = "AppPeliculas/partidos/detalle_partidos.html"

#C (Create) de Partidos ---- CreateView
    
class CrearPartidos(CreateView):
    
    model = Futbol
    template_name = "AppPeliculas/partidos/crear_partidos.html"
    fields = ["equipo_local", "equipo_visitante", "resultado", "fecha"]
    success_url = "/listaPartidos/"


#U (Update) de Partidos ----  UpdateView

class ActualizarPartidos(UpdateView):
    
    model = Futbol
    template_name = "AppPeliculas/peliculas/crear_peliculas.html"
    fields = ["equipo_local", "equipo_visitante", "resultado", "fecha"]
    success_url = "/listaPartidos/"


#D (Delete) de Partidos --- DeleteView
class BorrarPartidos(DeleteView):

    model = Futbol
    template_name = "AppPeliculas/peliculas/borrar_partidos.html"
    success_url = "/listaPartidos/"




#CRUD de Películas (Vistas basadas en Clases)

#R (Read) de Películas --- ListView

class ListaPeliculas(ListView): 

    model = Pelicula
    #nombre por defecto: pelicula_list.html
    template_name = "AppPeliculas/peliculas/lista_de_peliculas.html"

#C (Create) de Películas ---- CreateView
    
class CrearPeliculas(CreateView):
    
    model = Pelicula
    template_name = "AppPeliculas/peliculas/crear_peliculas.html"
    fields = ["nombre", "año", "director", "genero", "duracion"]
    success_url = "/listaPelis/"


#U (Update) de Películas ----  UpdateView

class ActualizarPeliculas(UpdateView):
    
    model = Pelicula
    template_name = "AppPeliculas/peliculas/crear_peliculas.html"
    fields = ["nombre", "año", "director", "genero", "duracion"]
    success_url = "/listaPelis/"


#D (Delete) de Películas --- DeleteView
class BorrarPeliculas(DeleteView):

    model = Pelicula
    template_name = "AppPeliculas/peliculas/borrar_peliculas.html"
    success_url = "/listaPelis/"


"""

def agregar_serie_con_html(request):

    #saber que el usuario ha dado click en el botón del formulario
    if request.method == "POST":

        serie_nueva = Serie(
            nombre = request.POST["name"], 
            año = request.POST["year"], 
            temporadas = request.POST["seasons"]
            )

        serie_nueva.save()

    return render(request, "AppPeliculas/nueva_serie.html")
    


def agregar_pelicula(request):
    
    pelicula1 = Pelicula(nombre="La La Land", año=2017, director="Damien Chazelle", 
                         genero="Musical", duracion=1.50) #Crear un objeto usando el modelo
    pelicula1.save()

    return HttpResponse("Se agregó una pelicula...")
"""