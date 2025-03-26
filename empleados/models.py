from django.db import models

# Definir una tupla con los valores del select genero_empleado
generos = (
    ("Masculino", "Masculino"),
    ("Femenino", "Femenino"),
    ("Otro", "Otro"),
)


class Empleado(models.Model):
    nombre_empleado = models.CharField(max_length=200)
    apellido_empleado = models.CharField(max_length=100)
    email_empleado = models.EmailField(max_length=50)
    edad_empleado = models.IntegerField()
    genero_empleado = models.CharField(max_length=80, choices=generos)
    salario_empleado = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    foto_empleado = models.ImageField(
        upload_to='fotos_empleados/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def es_extension_valida(self):
        extensiones_validas = ['.jpg', '.jpeg', '.png', '.gif']
        return any(self.foto_empleado.name.lower().endswith(ext) for ext in extensiones_validas)

    """ la clase Meta dentro de un modelo se utiliza para proporcionar metadatos adicionales sobre el modelo."""
    class Meta:
        db_table = "empleados"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nombre_empleado} {self.apellido_empleado}"


class Tarea(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='tareas')
    titulo_tarea = models.CharField(max_length=200)
    descripcion_tarea = models.TextField()
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateTimeField()
    estado_tarea = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada')
    ], default='pendiente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tareas"
        ordering = ['-fecha_asignacion']

    def __str__(self):
        return f"{self.titulo_tarea} - {self.empleado.nombre_empleado}"
