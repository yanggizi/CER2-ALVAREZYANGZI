from django.contrib import admin
from django.urls import path
from MYAPP import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.anonimo, name='anonimo'),
    path('main/', views.main, name='UTFSM'),
    path('login/', views.login, name='login'),
    path('estudiante/', views.estudiante, name='estudiante'),
    path('docente/', views.docente, name='docente'),
    path('subir_proyecto/', views.subir_proyecto, name='subir_proyecto'),
    path('logout/', views.logout_view, name='logout'),
    path('patrocinar/<str:nombreProyecto>/', views.patrocinar, name='patrocinar'),
    path('filtrar-proyectos/', views.filtrar_proyectos, name='filtrar_proyectos'),
]
