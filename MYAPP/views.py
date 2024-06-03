from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.models import Group
from .models import Proyecto
from .forms import crearProyecto, patrocinadorForm

def is_docente(user):
    return user.groups.filter(name='Docente').exists()

def is_estudiante(user):
    return user.groups.filter(name='Estudiante').exists()

def main(request):
    proyectos = Proyecto.objects.all()
    temas = Proyecto.objects.values_list('nombreTema', flat=True).distinct()  
    return render(request, "main.html", {"cursos": proyectos, "temas": temas})

def filtrar_proyectos(request):
    tema = request.GET.get('temaProyecto')
    if tema:
        proyectos_filtrados = Proyecto.objects.filter(nombreTema=tema)
    else:
        proyectos_filtrados = Proyecto.objects.all()
    return render(request, 'main.html', {'cursos': proyectos_filtrados})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.groups.filter(name='Estudiante').exists():
                return redirect('estudiante')
            elif user.groups.filter(name='Docente').exists():
                return redirect('docente')
        else:
            return render(request, 'login.html', {'error': 'Nombre de usuario o contraseña incorrectos.'})
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('UTFSM')

def anonimo(request):
    proyectos = Proyecto.objects.all()
    return render(request, "anonimo.html", {"cursos": proyectos})

@user_passes_test(is_estudiante)
def estudiante(request):
    proyectos = Proyecto.objects.all()
    return render(request, "estudiante.html", {"cursos": proyectos})

@user_passes_test(is_estudiante)
def subir_proyecto(request):
    if request.method == 'POST':
        form = crearProyecto(request.POST)
        if form.is_valid():
            form.save()
            return redirect('estudiante')
    else:
        form = crearProyecto()
    return render(request, 'subir_proyecto.html', {'form': form})

@user_passes_test(is_docente)
def docente(request):
    is_docente = False
    if request.user.is_authenticated:
        is_docente = request.user.groups.filter(name='Docente').exists()

    proyectos_patrocinados = Proyecto.objects.exclude(nombrePatrocinador="-")
    proyectos_no_patrocinados = Proyecto.objects.filter(nombrePatrocinador="-")
    
    filtro = request.GET.get('filtro', 'todos')
    
    if filtro == 'patrocinados':
        proyectos = proyectos_patrocinados
    elif filtro == 'no_patrocinados':
        proyectos = proyectos_no_patrocinados
    else:
        proyectos = Proyecto.objects.all()
    
    return render(request, "docente.html", {"cursos": proyectos, "filtro": filtro, "is_docente": is_docente})

@user_passes_test(is_docente)
def patrocinar(request, nombreProyecto):
    proyecto = get_object_or_404(Proyecto, nombreProyecto=nombreProyecto)
    if request.method == 'POST':
        form = patrocinadorForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('docente')
    else:
        form = patrocinadorForm(instance=proyecto)
    return render(request, 'patrocinar.html', {'form': form, 'proyecto': proyecto})
