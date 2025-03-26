from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registrar_empleado/', views.registrar_empleado, name='registrar_empleado'),
    path('empleados/', views.listar_empleados, name='listar_empleados'),
    path('editar_empleado/<int:id>/', views.editar_empleado, name='editar_empleado'),
    path('eliminar_empleado/<int:id>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('cargar_archivo/', views.cargar_archivo, name='cargar_archivo'),
    path('form_carga_masiva/', views.view_form_carga_masiva, name='form_carga_masiva'),
    path('asignar-tarea/', views.asignar_tarea, name='asignar_tarea'),
    path('listar-tareas/', views.listar_tareas, name='listar_tareas'),
]
