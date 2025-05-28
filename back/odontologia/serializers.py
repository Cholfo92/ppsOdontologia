from rest_framework import serializers
from .models import Referencia, Paciente, Obra_social, Tipo, Turno, Tratamiento, Material, Insumo, DetalleTurno, Pieza, Cara, Odontograma, DetalleOdontograma, Radiografia

class PacienteSerializer(serializers.ModelSerializer):

    fecha_nacimiento = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Paciente
        fields = '__all__'

class Obra_socialSerializer(serializers.ModelSerializer):
    asociados = serializers.IntegerField(read_only=True)

    class Meta:
        model = Obra_social
        fields = ['ID_os', 'nombre', 'asociados']  # agregá 'asociados'

class TipoSerializer(serializers.ModelSerializer):
    cantidad = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tipo
        fields = '__all__'

class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = ['ID_turno', 'ID_paciente', 'Fecha', 'Hora', 'asistencia']

class TratamientoSerializer(serializers.ModelSerializer):
    
    ID_tipo = serializers.PrimaryKeyRelatedField(queryset=Tipo.objects.all())

    class Meta:
        model = Tratamiento
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class InsumoSerializer(serializers.ModelSerializer):
    ID_material = serializers.PrimaryKeyRelatedField(
        queryset=Material.objects.all()
    )

    class Meta:
        model = Insumo
        fields = ['ID_insumo', 'ID_material','ID_tratamiento', 'Cantidad' ]

class DetalleTurnoSerializer(serializers.ModelSerializer):

    ID_tratamiento = serializers.PrimaryKeyRelatedField(queryset=Tratamiento.objects.all())
    ID_turno = serializers.PrimaryKeyRelatedField(queryset=Turno.objects.all())

    class Meta:
        model = DetalleTurno
        fields = '__all__'

class PiezaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pieza
        fields = '__all__'

class CaraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cara
        fields = '__all__'

class OdontogramaSerializer(serializers.ModelSerializer):

    paciente = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all())
    turno = serializers.PrimaryKeyRelatedField(queryset=Turno.objects.all())

    class Meta:
        model = Odontograma
        fields = '__all__'

class DetalleOdontogramaSerializer(serializers.ModelSerializer):
    odontograma = serializers.PrimaryKeyRelatedField(queryset=Odontograma.objects.all())
    referencia = serializers.PrimaryKeyRelatedField(queryset=Referencia.objects.all())
    pieza = serializers.PrimaryKeyRelatedField(queryset=Pieza.objects.all())
    cara = serializers.PrimaryKeyRelatedField(queryset=Cara.objects.all())

    class Meta:
        model = DetalleOdontograma
        fields = '__all__'

class RadiografiaSerializer(serializers.ModelSerializer):

    ID_pieza = serializers.PrimaryKeyRelatedField(queryset=Pieza.objects.all())
    ID_paciente = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all())
    ID_turno = serializers.PrimaryKeyRelatedField(queryset=Turno.objects.all())

    class Meta:
        model = Radiografia
        fields = '__all__'

class ReferenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referencia
        fields = '__all__'

class ResumenSerializer(serializers.Serializer):
    Paciente = serializers.IntegerField()
    Obra_social = serializers.IntegerField()
    Tratamiento = serializers.IntegerField()