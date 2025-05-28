from django.db import models

class Obra_social(models.Model):
    ID_os = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Obra_Social'


class Paciente(models.Model):
    ID_paciente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=9, unique=True, db_column='DNI')
    fecha_nacimiento = models.DateField(db_column='Fecha_Nac')
    direccion = models.CharField(max_length=100, db_column='domicilio')
    telefono = models.CharField(max_length=20)
    obra_social = models.ForeignKey(Obra_social, on_delete=models.CASCADE, db_column='ID_os')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        db_table = 'Paciente'


class Tipo(models.Model):
    ID_tipo  = models.AutoField(primary_key=True, db_column='ID_tipo')
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Tipo'


class Turno(models.Model):
    ID_turno = models.AutoField(primary_key=True)
    ID_paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, db_column='ID_paciente')
    Fecha = models.DateField(db_column='Fecha')
    Hora = models.TimeField(db_column='Hora')
    asistencia = models.BooleanField()

    def __str__(self):
        return f'{self.ID_paciente.apellido}, {self.ID_paciente.nombre} - {self.Fecha}'

    class Meta: 
        db_table = 'Turno'


class Tratamiento(models.Model):
    ID_tratamiento = models.AutoField(primary_key=True, db_column='ID_tratamiento')
    Nombre = models.CharField(max_length=100, unique=True)
    ID_tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, db_column='ID_tipo')

    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = 'Tratamiento'


class Material(models.Model):
    ID_material = models.AutoField(primary_key=True, db_column='ID_material')
    Nombre = models.CharField(max_length=100, unique=True, db_column='Nombre')
    cantidad = models.IntegerField(db_column='Cant')
    min = models.IntegerField(db_column='min')

    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = 'Material'


class Insumo(models.Model):
    ID_insumo = models.AutoField(primary_key=True)
    ID_tratamiento = models.ForeignKey(Tratamiento, on_delete=models.CASCADE, db_column='ID_tratamiento')
    ID_material = models.ForeignKey(Material, on_delete=models.CASCADE, db_column='ID_material')
    Cantidad = models.IntegerField()

    def __str__(self):
        return f'{self.ID_tratamiento.nombre} - {self.ID_material.Nombre}'

    class Meta:
        db_table = 'Insumos'


class DetalleTurno(models.Model):
    ID_detalle = models.AutoField(primary_key=True)
    ID_turno = models.ForeignKey(Turno, on_delete=models.CASCADE, db_column='ID_turno')
    ID_tratamiento = models.ForeignKey(Tratamiento, on_delete=models.CASCADE, db_column='ID_tratamiento')
    Observacion = models.TextField(max_length=500, blank=True, null=True, db_column='Observacion' )

    def __str__(self):
        return f'{self.ID_turno.ID_paciente.apellido}, {self.ID_turno.ID_paciente.nombre} - {self.ID_tratamiento.Nombre}'

    class Meta:
        db_table = 'detalleTurno'


class Pieza(models.Model):
    ID_diente = models.AutoField(primary_key=True )
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'pieza'


class Cara(models.Model):
    ID_Cara = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Cara'


class Referencia(models.Model):
    ID_referencias = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=100, unique=True, db_column='Nombre')
    icon = models.CharField(max_length=10, blank=True, null=True)
    alterIcon = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Referencias'


class Odontograma(models.Model):
    ID_odonto = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, db_column='ID_paciente')
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, db_column='ID_turno')
    observacion = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.paciente.apellido}, {self.paciente.nombre}'

    class Meta:
        db_table = 'Odontograma'


class DetalleOdontograma(models.Model):
    ID_detalleOdonto = models.AutoField(primary_key=True)
    odontograma = models.ForeignKey(Odontograma, on_delete=models.CASCADE, db_column='ID_odonto')
    observacion = models.TextField(max_length=255, db_column='Observacion')
    referencia = models.ForeignKey(Referencia, on_delete=models.CASCADE, db_column='ID_referencias')
    pieza = models.ForeignKey(Pieza, on_delete=models.CASCADE, db_column='ID_diente')
    cara = models.ForeignKey(Cara, on_delete=models.CASCADE, db_column='ID_Cara')

    def __str__(self):
        return f'{self.odontograma.paciente.nombre} {self.odontograma.paciente.apellido}'

    class Meta:
        db_table = 'detalleOdontograma'


class Radiografia(models.Model):
    ID_radiografia = models.AutoField(primary_key=True)
    ID_turno = models.ForeignKey(Turno, on_delete=models.CASCADE, db_column='ID_turno')
    imagen = models.ImageField(upload_to='imagen/', db_column='Imagen')
    observacion = models.TextField(max_length=255, blank=True, null=True, db_column='Observacion')
    tipo = models.CharField(max_length=50, blank=True, null=True)
    ID_paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, db_column='ID_paciente')
    ID_pieza = models.ForeignKey(Pieza, on_delete=models.CASCADE, db_column='ID_diente')

    def __str__(self):
        return f'{self.paciente.nombre} {self.paciente.apellido} - {self.tipo}'

    class Meta:
        db_table = 'Radiografia'