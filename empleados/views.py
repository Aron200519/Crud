from django.shortcuts import render, redirect, get_object_or_404
import os
import uuid
from django.core.files.uploadedfile import SimpleUploadedFile

from decimal import Decimal  # Asegúrate de importar Decimal
from django.contrib import messages  # Para usar mensajes flash
from django.core.exceptions import ObjectDoesNotExist

# Para el informe (Reporte) Excel
import pandas as pd

import json

import logging

from django.utils import timezone
from openpyxl import Workbook  # Para generar el informe en excel
from django.http import HttpResponse, JsonResponse

from .models import Empleado, Tarea  # Importando el modelo de Empleado y Tarea
from .forms import EmpleadoForm, TareaForm
from datetime import datetime


def inicio(request):
    return render(request, 'empleados/inicio.html')


def listar_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleados/listar_empleados.html', {'empleados': empleados})


def view_form_carga_masiva(request):
    return render(request, 'empleados/form_carga_masiva.html')


def detalles_empleado(request, id):
    try:
        empleado = Empleado.objects.get(id=id)
        data = {"empleado": empleado}
        return render(request, "empleados/detalles.html", data)
    except Empleado.DoesNotExist:
        error_message = f"No existe ningún registro para la búsqueda id: {id}"
        return render(request, "empleados/lista_empleados.html", {"error_message": error_message})


def registrar_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado registrado exitosamente')
            return redirect('listar_empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'empleados/registrar_empleado.html', {'form': form})


def view_form_update_empleado(request, id):
    try:
        empleado = Empleado.objects.get(id=id)
        opciones_edad = [(int(edad), int(edad)) for edad in range(18, 51)]

        data = {"empleado": empleado,
                'opciones_edad': opciones_edad,
                }
        return render(request, "empleados/form_update_empleado.html", data)
    except ObjectDoesNotExist:
        error_message = f"El Empleado con id: {id} no existe."
        return render(request, "empleados/lista_empleados.html", {"error_message": error_message})


def actualizar_empleado(request, id):
    try:
        if request.method == "POST":
            empleado = Empleado.objects.get(id=id)

            empleado.nombre_empleado = request.POST.get('nombre_empleado')
            empleado.apellido_empleado = request.POST.get('apellido_empleado')
            empleado.email_empleado = request.POST.get('email_empleado')
            empleado.edad_empleado = int(request.POST.get('edad_empleado'))
            empleado.genero_empleado = request.POST.get('genero_empleado')

            salario_empleado = Decimal(request.POST.get(
                'salario_empleado').replace(',', '.'))
            empleado.salario_empleado = salario_empleado

            if 'foto_empleado' in request.FILES:
                empleado.foto_empleado = generate_unique_filename(
                    request.FILES['foto_empleado'])

            empleado.save()
        return redirect('listar_empleados')
    except ObjectDoesNotExist:
        error_message = f"El Empleado con id: {id} no se actualizó."
        return render(request, "empleados/lista_empleados.html", {"error_message": error_message})


def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        empleado.delete()
        messages.success(request, 'Empleado eliminado exitosamente')
        return redirect('listar_empleados')
    return render(request, 'empleados/eliminar_empleado.html', {'empleado': empleado})


def cargar_archivo(request):
    try:
        if request.method == 'POST':
            archivo_xlsx = request.FILES['archivo_xlsx']
            if archivo_xlsx.name.endswith('.xlsx'):
                df = pd.read_excel(archivo_xlsx, header=0)

                for _, row in df.iterrows():
                    nombre_empleado = row['Nombre']
                    apellido_empleado = row['Apellido']
                    edad_empleado = row['Edad']
                    email_empleado = row['Email']
                    genero_empleado = row['Sexo']
                    salario_empleado = row['Salario']

                    empleado, creado = Empleado.objects.update_or_create(
                        email_empleado=email_empleado,
                        defaults={
                            'nombre_empleado': nombre_empleado,
                            'apellido_empleado': apellido_empleado,
                            'edad_empleado': edad_empleado,
                            'email_empleado': email_empleado,
                            'genero_empleado': genero_empleado,
                            'salario_empleado': salario_empleado,
                            'foto_empleado': '',
                        }
                    )

                return JsonResponse({'status_server': 'success', 'message': 'Los datos se importaron correctamente.'})
            else:
                return JsonResponse({'status_server': 'error', 'message': 'El archivo debe ser un archivo de Excel válido.'})
        else:
            return JsonResponse({'status_server': 'error', 'message': 'Método HTTP no válido.'})

    except Exception as e:
        logging.error("Error al cargar el archivo: %s", str(e))
        return JsonResponse({'status_server': 'error', 'message': f'Error al cargar el archivo: {str(e)}'})


def generate_unique_filename(file):
    extension = os.path.splitext(file.name)[1]
    unique_name = f'{uuid.uuid4()}{extension}'
    return SimpleUploadedFile(unique_name, file.read())


def editar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado actualizado exitosamente')
            return redirect('listar_empleados')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'empleados/editar_empleado.html', {'form': form, 'empleado': empleado})


def asignar_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea asignada correctamente')
            return redirect('listar_tareas')
    else:
        form = TareaForm()
    return render(request, 'empleados/asignar_tarea.html', {'form': form})


def listar_tareas(request):
    tareas = Tarea.objects.all()
    return render(request, 'empleados/listar_tareas.html', {'tareas': tareas})
