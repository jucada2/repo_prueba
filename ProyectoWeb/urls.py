"""
URL configuration for ProyectoWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AppPeliculas.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", inicio, name="Inicio"),

    path("avatar/", agregar_avatar, name="Agregar Avatar"),

    path("login/", inicio_sesion, name="Iniciar Sesion"),
    path("signup/", registro, name = "Registrar Usuario"),
    path("edit/", editar_perfil, name="Editar Usuario"),
    path("logout/", cerrar_sesion, name="Cerrar Sesión"),

    #CRUD de Película
    path("listaPelis/", ListaPeliculas.as_view(), name="Lista de Peliculas"),
    path("crearPelis/", CrearPeliculas.as_view(), name="Crear Peliculas"),
    path("actualizarPeli/<int:pk>", ActualizarPeliculas.as_view(), name="Actualizar Pelicula"),
    path("borrarPeli/<int:pk>", BorrarPeliculas.as_view(), name="Borrar Pelicula"),

    #CRUD de Partido de Fútbol
    path("listaPartidos/", ListaPartidos.as_view(), name="Lista de Partidos"),
    path("detallePartido/<int:pk>", DetallePartidos.as_view(), name="Detalle Partido"),
    path("crearPartidos/", CrearPartidos.as_view(), name="Crear Partido"),
    path("actualizarPartido/<int:pk>", ActualizarPartidos.as_view(), name="Actualizar Partido"),
    path("borrarPartido/<int:pk>", BorrarPartidos.as_view(), name="Borrar Partido"),




    #URLs de los modelos creados
    path("series/", ver_serie, name="Series"),
    #path("pelis/", ver_pelis, name="Peliculas"),
    path("futbol/", ver_partidos, name="Partidos de Futbol"),

    #URLs para crear nuevos datos
    path("nuevaSerie/", agregar_serie, name="Nueva Serie"),
    path("nuevaPeli/", agregar_pelicula),

    #URLs para buscar datos
    path("buscarSerieAño/", busqueda_serie_por_año),
    path("resultadosSerie/", resultados_buscar_serie_año),
    
    #path("nuevaPeli/", agregar_pelicula),

    #URLs para actualizar 
    path("actualizarSerie/<serie_nombre>", actualizar_serie, name="Actualizar Serie"),

    #URLs para eliminar
    path("eliminarSerie/<serie_nombre>", eliminar_serie, name="Eliminar Serie"),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)