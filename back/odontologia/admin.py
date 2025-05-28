from django.contrib import admin
from .models import Paciente, Obra_social, Tipo, Turno, Tratamiento, Material, Insumo, DetalleTurno, Pieza, Cara, Odontograma, DetalleOdontograma, Radiografia, Referencia

admin.site.register(Paciente)
admin.site.register(Obra_social)
admin.site.register(Tipo)
admin.site.register(Turno)
admin.site.register(Tratamiento)
admin.site.register(Material)
admin.site.register(Insumo)
admin.site.register(DetalleTurno)
admin.site.register(Pieza)
admin.site.register(Cara)
admin.site.register(Odontograma)
admin.site.register(DetalleOdontograma)
admin.site.register(Radiografia)
admin.site.register(Referencia)