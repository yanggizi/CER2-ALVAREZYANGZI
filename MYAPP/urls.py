from django.urls import path
from . import views

urlpatters=[
    path('/main',views.main)
    path('/login',views.login)
    path('/home',views.anonimo)
    path('/estudiante',views.estudiante)
    path('/docente',views.docente)
]