from django.urls import path, include
from .views import ReferenciaViewSet, resumenViewSet, PacienteViewSet, Obra_socialViewSet, TurnoViewSet, TratamientoViewSet, TipoViewSet, MaterialViewSet, InsumoViewSet, DetalleTurnoViewSet, PiezaViewSet, CaraViewSet, OdontogramaViewSet, RadiografiaViewSet, DetalleOdontogramaViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Pacientes', PacienteViewSet)
router.register(r'Obra Social', Obra_socialViewSet)
router.register(r'Turno', TurnoViewSet)
router.register(r'Tratamiento', TratamientoViewSet)
router.register(r'Tipo', TipoViewSet)
router.register(r'Material', MaterialViewSet)
router.register(r'Insumos', InsumoViewSet)
router.register(r'DetalleTurno', DetalleTurnoViewSet)
router.register(r'Pieza', PiezaViewSet)
router.register(r'Cara', CaraViewSet)
router.register(r'Odontograma', OdontogramaViewSet)
router.register(r'Radiografia', RadiografiaViewSet)
router.register(r'DetalleOdontograma', DetalleOdontogramaViewSet)
router.register(r'Referencia', ReferenciaViewSet)
router.register(r'Resumen', resumenViewSet, basename = "Resumen")

urlpatterns = router.urls
#urlpatterns = [
#    path('admin/', admin.site.urls),
#    path('api/', include('odontologia.urls')),
#]
