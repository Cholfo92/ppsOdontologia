from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from .models import Referencia, Paciente, Obra_social, Tipo, Turno, Tratamiento, Material, Insumo, DetalleTurno, Pieza, Cara, Odontograma, DetalleOdontograma, Radiografia
from .serializers import ReferenciaSerializer, ResumenSerializer, PacienteSerializer, Obra_socialSerializer, TipoSerializer, TurnoSerializer, TratamientoSerializer, MaterialSerializer, InsumoSerializer, DetalleTurnoSerializer, PiezaSerializer, CaraSerializer, OdontogramaSerializer, RadiografiaSerializer, DetalleOdontogramaSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        nombre = self.request.query_params.get('nombre', None)
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        apellido = self.request.query_params.get('apellido', None)
        if apellido:
            queryset = queryset.filter(apellido__icontains=apellido)
        dni = self.request.query_params.get('dni', None)
        if dni:
            queryset = queryset.filter(dni=dni)
        paciente_id = self.request.query_params.get('paciente', None)
        if paciente_id:
            queryset = queryset.filter(id=paciente_id)
        return queryset
    
class Obra_socialViewSet(viewsets.ModelViewSet):
    queryset = Obra_social.objects.annotate(asociados=Count('paciente'))
    serializer_class = Obra_socialSerializer

    @action(detail=True, methods=['get'])
    def pacientes(self, request, pk=None):
        pacientes = Paciente.objects.filter(obra_social_id=pk)
        serializer = PacienteSerializer(pacientes, many=True)
        return Response(serializer.data)

class TurnoViewSet(viewsets.ModelViewSet):
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['Fecha', 'id']  # Permitimos ordenar por fecha o id
    ordering = ['Fecha']  # Orden predeterminado si no se especifica

    def get_queryset(self):
        queryset = super().get_queryset()
        turno_id = self.request.query_params.get('turno', None)
        if turno_id:
            queryset = queryset.filter(id=turno_id)
        asistencia = self.request.query_params.get('Asistencia', None)
        if asistencia:
            queryset = queryset.filter(asistencia=asistencia)
        paciente = self.request.query_params.get('ID_paciente', None)
        if paciente:
            queryset = queryset.filter(ID_paciente=paciente)
        return queryset
    
    @action(detail=False, methods=['get'])
    def ultimo(self, request):
        ultimo_turno = self.get_queryset().order_by('-ID_turno').first()
        serializer = self.get_serializer(ultimo_turno)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        turno = self.get_object()
        if turno.asistencia:
            return Response(
                {"detail": "No se puede modificar un turno con asistencia confirmada."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        turno = self.get_object()
        if turno.asistencia:
            return Response(
                {"detail": "No se puede eliminar un turno con asistencia confirmada."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    
class TratamientoViewSet(viewsets.ModelViewSet):
    queryset = Tratamiento.objects.all()
    serializer_class = TratamientoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tratamiento_id = self.request.query_params.get('tratamiento', None)
        if tratamiento_id:
            queryset = queryset.filter(id_tratamiento=tratamiento_id)
        tipo = self.request.query_params.get('tipo', None)
        if tipo:
            queryset = queryset.filter(ID_tipo=tipo)
        return queryset

class TipoViewSet(viewsets.ModelViewSet):
    queryset = Tipo.objects.annotate(cantidad=Count('tratamiento'))
    serializer_class = TipoSerializer

    @action(detail=True, methods=['get'])
    def tratamientos(self, request, pk=None):
        tratamiento = Tratamiento.objects.filter(ID_tipo=pk)
        serializer = TratamientoSerializer(tratamiento, many=True)
        return Response(serializer.data)

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class InsumoViewSet(viewsets.ModelViewSet):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        insumo_id = self.request.query_params.get('insumo', None)
        if insumo_id:
            queryset = queryset.filter(ID_insumo=insumo_id)
        tratamiento = self.request.query_params.get('tratamiento', None)
        if tratamiento:
            queryset = queryset.filter(ID_tratamiento=tratamiento)
        material = self.request.query_params.get('material', None)
        if material:
            queryset = queryset.filter(ID_material=material)
        return queryset

class DetalleTurnoViewSet(viewsets.ModelViewSet):
    queryset = DetalleTurno.objects.all()
    serializer_class = DetalleTurnoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        detalle_id = self.request.query_params.get('detalle', None)
        if detalle_id:
            queryset = queryset.filter(ID_detalle=detalle_id)
        tratamiento = self.request.query_params.get('tratamiento', None)
        if tratamiento:
            queryset = queryset.filter(ID_tratamiento=tratamiento)
        turno = self.request.query_params.get('turno', None)
        if turno:
            queryset = queryset.filter(ID_turno=turno)
        return queryset

class PiezaViewSet(viewsets.ModelViewSet):
    queryset = Pieza.objects.all()
    serializer_class = PiezaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        pieza_id = self.request.query_params.get('pieza', None)
        if pieza_id:
            queryset = queryset.filter(id=pieza_id)
        return queryset

class CaraViewSet(viewsets.ModelViewSet):
    queryset = Cara.objects.all()
    serializer_class = CaraSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        cara_id = self.request.query_params.get('cara', None)
        if cara_id:
            queryset = queryset.filter(id=cara_id)
        return queryset

class OdontogramaViewSet(viewsets.ModelViewSet):
    queryset = Odontograma.objects.all()
    serializer_class = OdontogramaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        odontograma_id = self.request.query_params.get('odontograma', None)
        if odontograma_id:
            queryset = queryset.filter(id=odontograma_id)
        paciente = self.request.query_params.get('paciente', None)
        if paciente:
            queryset = queryset.filter(paciente=paciente)
        turno = self.request.query_params.get('turno', None)
        if turno:
            queryset = queryset.filter(turno=turno)
        return queryset
    
    @action(detail=False, methods=['get'])
    def ultimo(self, request):
        ultimo_turno = self.get_queryset().order_by('-id').first()
        serializer = self.get_serializer(ultimo_turno)
        return Response(serializer.data)

class RadiografiaViewSet(viewsets.ModelViewSet):
    queryset = Radiografia.objects.all()
    serializer_class = RadiografiaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        radiografia_id = self.request.query_params.get('ID_radiografia', None)
        if radiografia_id:
            queryset = queryset.filter(ID_radiografia=radiografia_id)
        paciente = self.request.query_params.get('ID_paciente', None)
        if paciente:
            queryset = queryset.filter(ID_paciente=paciente)
        turno = self.request.query_params.get('ID_turno', None)
        if turno:
            queryset = queryset.filter(ID_turno=turno)
        return queryset

class DetalleOdontogramaViewSet(viewsets.ModelViewSet):
    queryset = DetalleOdontograma.objects.all()
    serializer_class = DetalleOdontogramaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        DetalleOdontograma_id = self.request.query_params.get('DetalleOdontograma', None)
        if DetalleOdontograma_id:
            queryset = queryset.filter(id=DetalleOdontograma_id)
        odontograma = self.request.query_params.get('odontograma', None)
        if odontograma:
            queryset = queryset.filter(odontograma=odontograma)
        diente = self.request.query_params.get('diente', None)
        if diente:
            queryset = queryset.filter(diente=diente)
        return queryset

class ReferenciaViewSet(viewsets.ModelViewSet):
    queryset = Referencia.objects.all()
    serializer_class = ReferenciaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        referencia_id = self.request.query_params.get('referencia', None)
        if referencia_id:
            queryset = queryset.filter(id=referencia_id)
        return queryset

class resumenViewSet(viewsets.ViewSet):
    def list(self, request):

        resumen_obras = Obra_social.objects.annotate(cantidad_pacientes=Count('paciente'))

        data = {
            "pacientes": Paciente.objects.count(),
            "obras_sociales": Obra_social.objects.count(),
            "tratamientos": Tratamiento.objects.count(),
            "asociados_por_obra": [
                {
                    "ID_os": obra.ID_os,
                    "nombre": obra.nombre,
                    "cantidad_pacientes": obra.cantidad_pacientes
                }
                for obra in resumen_obras
            ]
        }
        return Response(data)
    