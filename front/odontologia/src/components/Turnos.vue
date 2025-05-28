<template>

<div class="week-nav" style="display: flex; justify-content: center; gap: 10px; margin-bottom: 16px;">

    <el-button size="small" round @click="añoAnterior">
    <i class="el-icon-d-arrow-left" style="margin-right: 4px;"></i> Año anterior
    </el-button>
    <el-button size="small" round @click="mesAnterior">
    <i class="el-icon-arrow-left" style="margin-right: 4px;"></i> Mes anterior
    </el-button>
    <el-button size="small" type="primary" round @click="semanaAnterior">
        <i class="el-icon-arrow-left" style="margin-right: 4px;"></i> Semana anterior
    </el-button>
    <el-button size="small" round @click="hoy">
        Hoy
    </el-button>
    <el-button size="small" type="primary" round @click="semanaSiguiente">
        Semana siguiente <i class="el-icon-arrow-right" style="margin-left: 4px;"></i>
    </el-button>
    <el-button size="small" round @click="mesSiguiente">
        Mes siguiente <i class="el-icon-arrow-right" style="margin-left: 4px;"></i>
    </el-button>
    <el-button size="small" round @click="añoSiguiente">
        Año siguiente <i class="el-icon-d-arrow-right" style="margin-left: 4px;"></i>
    </el-button>
</div>

<div style="overflow-x:auto;">
    <el-table
    :data="semana"
    border
    style="min-width:900px;"
    :row-class-name="rowClassName"
    v-loading="loading"
    element-loading-text="Cargando..."
    >

    <el-table-column label="Día / Fecha" fixed width="160">
        <template #default="{ row }">
        <strong>{{ row.dia }} ({{ row.fecha }})</strong>
        </template>
    </el-table-column>

    <el-table-column
        v-for="hora in horas"
        :key="hora"
        :label="hora"
        width="158"
    >
        <template #default="{ row }">
        <div
        class="celda-evento"
        :class="[
            { bloqueado: isWeekend(row.date) || isTimeBlocked(hora) },
            { asistio: eventos[row.fechaISO]?.[hora]?.asistencia },
            { noAsistio: eventos[row.fechaISO]?.[hora] && !eventos[row.fechaISO]?.[hora]?.asistencia },
            {
            libre:
                !isWeekend(row.date) &&
                !isTimeBlocked(hora) &&
                !eventos[row.fechaISO]?.[hora]
            }
        ]"
        @click="!isWeekend(row.date) && !isTimeBlocked(hora) && abrirModal(row, hora)"
        >

        <template v-if="eventos[row.fechaISO]?.[hora]">
            {{ pacienteMap[eventos[row.fechaISO]?.[hora]?.pacienteId]?.nombre || '' }}
            {{ pacienteMap[eventos[row.fechaISO]?.[hora]?.pacienteId]?.apellido || '' }}
        </template>


        <template v-else-if="!isWeekend(row.date) && !isTimeBlocked(hora)">
            Libre
        </template>
        </div>
        </template>
    </el-table-column>
    </el-table>
</div>

<el-dialog v-model="formReg" title="Registrar Nuevo Turno" width="500">
    <el-form :model="form" ref="formRef" :rules="reglas">
        <el-form-item label="Paciente" prop="paciente">
        <div style="display: flex; gap: 8px; align-items: center; width: 100%;">
        <el-select
            v-model="form.paciente"
            placeholder="Selecciona un Paciente"
            filterable
            clearable
            style="flex: 1"
            >
            <el-option
                v-for="obra in optionsPaciente"
                :key="obra.value"
                :label="obra.label"
                :value="obra.value"
            />
        </el-select>
        </div>
        </el-form-item>

        <el-form-item label="Tratamiento" prop="tratamiento">
        <div style="display: flex; gap: 8px; align-items: center; width: 100%;">
        <el-select
            v-model="form.tratamientoSeleccionado"
            placeholder="Selecciona un Tratamiento"
            filterable
            clearable
            style="flex: 1"
            >
            <el-option
                v-for="obra in optionsTratamiento"
                :key="obra.value"
                :label="obra.label"
                :value="obra.value"
            />
        </el-select>
        </div>
    </el-form-item>
    
    <el-form-item>
        <el-input
    v-model="form.observacion"
    style="width: 500px"
    :rows="5"
    type="textarea"
    placeholder="Observaciones"
    />
    </el-form-item>

    <el-form-item>
        <div style="width: 100%; display: flex; justify-content: center;">
            <el-checkbox v-model="form.asistencia" label="Asistencia" size="large" border />
        </div>
</el-form-item>
    </el-form>
    <template #footer>
    <div class="dialog-footer">
        <el-button type="danger" @click="eliminar" round >Eliminar</el-button>
        <el-button @click="cancelar">Cancelar</el-button>
        <el-button type="primary" @click="registrar" round>Confirmar</el-button>
    </div>
    </template>
</el-dialog>


<el-dialog v-model="formMod" title="Modificar Turno" width="500">
    <el-form :model="form" ref="formRef" :rules="reglas">
        <el-form-item label="Paciente" prop="paciente">
        <div style="display: flex; gap: 8px; align-items: center; width: 100%;">
        <el-select
            v-model="form.paciente"
            placeholder="Selecciona un Paciente"
            filterable
            clearable
            style="flex: 1"
            >
            <el-option
                v-for="obra in optionsPaciente"
                :key="obra.value"
                :label="obra.label"
                :value="obra.value"
            />
        </el-select>
        </div>
        </el-form-item>

        <el-form-item label="Tratamiento" prop="tratamiento">
        <div style="display: flex; gap: 8px; align-items: center; width: 100%;">
        <el-select
            v-model="form.tratamientoSeleccionado"
            placeholder="Selecciona un Tratamiento"
            filterable
            clearable
            style="flex: 1"
            >
            <el-option
                v-for="obra in optionsTratamiento"
                :key="obra.value"
                :label="obra.label"
                :value="obra.value"
            />
        </el-select>
        </div>
    </el-form-item>
    
    <el-form-item>
        <el-input
    v-model="form.observacion"
    style="width: 500px"
    :rows="5"
    type="textarea"
    placeholder="Observaciones"
    />
    </el-form-item>

    <el-form-item>
        <div style="width: 100%; display: flex; justify-content: center;">
            <el-checkbox v-model="form.asistencia" label="Asistencia" size="large" border :disabled="asistenciaDeshabilitada"/>
        </div>
    </el-form-item>

    <div style="width: 100%; display: flex; justify-content: center;">
        <el-button type="success" @click="">Cargar Odontograma</el-button>
    </div>

    </el-form>
    <template #footer>
    <div class="dialog-footer">
        <el-button type="danger" @click="eliminar" round >Eliminar</el-button>
        <el-button @click="cancelar">Cancelar</el-button>
        <el-button type="primary" @click="modificar" round>Modificar</el-button>
    </div>
    </template>
</el-dialog>
</template>

<script lang="ts" setup>

import axios from 'axios';
import { addDays, isWeekend as dfIsWeekend, format, startOfWeek } from "date-fns";
import { es } from "date-fns/locale";
import { ElMessage, ElMessageBox } from 'element-plus';
import { onMounted, reactive, ref, watch } from "vue";

const loading = ref(false)
const weekStart = ref(startOfWeek(new Date(), { weekStartsOn: 1, locale: es }))
const semana = ref([])
const horas = ref(Array.from({ length: 10 }, (_, i) => `${i + 9}:00`))
const eventos = ref({})
const eventoFecha = ref("")
const eventoHora = ref("")
const formRef = ref(null)
const formReg = ref(false)
const formMod = ref(false)
const optionsPaciente = ref([])
const optionsTratamiento = ref([])
const pacienteMap = ref({})
const tratamientoMap = ref({})
const asistenciaDeshabilitada = ref(false)


const isWeekend = (d: Date) => dfIsWeekend(d)

const reglas = {
    nombre: [{ required: true, message: 'El Nombre es obligatorio', trigger: 'blur' }]
}

const form_ini = {
    paciente: null,
    tratamientoSeleccionado : null,
    asistencia : false,
    observacion : ''
}

const eliminar = async (row) => {
    try {
        const confirmacion = await ElMessageBox.confirm('¿Desea seguir con la eliminacion?', 'Eliminar Turno', {
            confirmButtonText: 'Aceptar',
            cancelButtonText: 'Cancelar',
            type: 'warning'
        })
        if (confirmacion) {
            await axios.delete(`http://127.0.0.1:8000/api/Turno/${eventos.value[eventoFecha.value][eventoHora.value].id}/`)
            await cargarTurnos()
            ElMessage.success('Turno eliminado correctamente')
            formMod.value = false
        }
    } catch (error) {
        console.error(error)
        ElMessage.error('Error al eliminar el Turno')
    }
}

const form = reactive({ ...form_ini })

function cargarSemana() {
    loading.value = true;
    setTimeout(() => {
    semana.value = Array.from({ length: 7 }, (_, i) => {
        const fechaObj = addDays(weekStart.value, i);
        return {
        /* para mostrar */
        dia: format(fechaObj, "EEEE", { locale: es }),
        fecha: format(fechaObj, "dd-MM-yyyy", { locale: es }),
        /* para lógica interna */
        fechaISO: format(fechaObj, "yyyy-MM-dd"),
        date: fechaObj
        };
    });
    loading.value = false}, 250)
}

function semanaAnterior() { 
    loading.value = true;
    setTimeout(() => {
    weekStart.value = addDays(weekStart.value, -7);
    loading.value = false}, 250)
}

function semanaSiguiente() { 
    loading.value = true;
    setTimeout(() => {
    weekStart.value = addDays(weekStart.value, +7); 
    loading.value = false}, 250)
}

watch(weekStart, cargarSemana, { immediate: true });

function hoy() {
    loading.value = true;
    setTimeout(() => {
    weekStart.value = startOfWeek(new Date(), { weekStartsOn: 1 });
    loading.value = false}, 250)
}

function añoAnterior() {
    loading.value = true;
    setTimeout(() => {
    weekStart.value = addDays(weekStart.value, -365);
    loading.value = false}, 250)
}

function añoSiguiente() {
    loading.value = true;
    setTimeout(() => {
    weekStart.value = addDays(weekStart.value, 365);
    loading.value = false}, 250)
}

function mesAnterior() {
    loading.value = true;
    setTimeout(() => {
    const date = new Date(weekStart.value)
    date.setMonth(date.getMonth() - 1)
    weekStart.value = startOfWeek(date, { weekStartsOn: 1 })
    loading.value = false}, 250)
}

function mesSiguiente() {
    loading.value = true;
    setTimeout(() => {
        const date = new Date(weekStart.value)
        date.setMonth(date.getMonth() + 1)
        weekStart.value = startOfWeek(date, { weekStartsOn: 1 })
    loading.value = false}, 250)
}

const isTimeBlocked = (hora) => {
    const h = parseInt(hora, 10);
    return h >= 13 && h < 16;
}

const rowClassName = ({ row }: any) =>
    isWeekend(row.date) ? "fila-bloqueada" : ""

function abrirModal(row, hora) {
    eventoFecha.value = row.fechaISO;
    eventoHora.value  = hora;
    const ev = eventos.value[eventoFecha.value]?.[eventoHora.value];

    if (ev) {
        form.paciente                = ev.pacienteId;
        form.tratamientoSeleccionado = ev.tratamientoId;    // ← aquí
        form.asistencia              = ev.asistencia;
        form.observacion             = ev.observacion;
        asistenciaDeshabilitada.value = ev.asistencia === true;
        formMod.value = true;
    } else {
        form.paciente                = null;
        form.tratamientoSeleccionado = null;
        form.asistencia              = false;
        form.observacion             = '';
        asistenciaDeshabilitada.value = false;
        formReg.value = true;
    }
}

const resetForm = () => {
    Object.assign(form, form_ini)
}

const cancelar = () => {
    resetForm()
    formReg.value = false
    formMod.value = false
}

function registrar() {
    if (!eventos.value[eventoFecha.value]) {
        eventos.value[eventoFecha.value] = {}
    }
    
    eventos.value[eventoFecha.value][eventoHora.value] = {
        pacienteId: form.paciente,
        tratamiento: form.tratamientoSeleccionado,
        observacion: form.observacion,
        asistencia: form.asistencia
    }
    formRef.value.validate(async (valid) => {
        if (valid) {
            try {
                const datos = {
                    ID_paciente: eventos.value[eventoFecha.value][eventoHora.value].pacienteId,
                    Fecha: eventoFecha.value,
                    Hora:eventoHora.value,
                    asistencia: eventos.value[eventoFecha.value][eventoHora.value].asistencia
                }
                await axios.post('http://127.0.0.1:8000/api/Turno/', datos)
                
                const turno = await axios.get('http://127.0.0.1:8000/api/Turno/ultimo/')
                const datos2 = {
                    ID_tratamiento: eventos.value[eventoFecha.value][eventoHora.value].tratamiento,
                    ID_turno: turno.data.ID_turno,
                    Observacion: eventos.value[eventoFecha.value][eventoHora.value].observacion
                }
                await axios.post('http://127.0.0.1:8000/api/DetalleTurno/', datos2)
                await cargarTurnos()
                ElMessage.success('Se agrego correctamente')
            } catch (error) {
            if (error.response && error.response.data) {
                console.error(error.response.data)
                ElMessage.error('Error: ' + JSON.stringify(error.response.data))
            } else {
                ElMessage.error('No se pudo agregar el Turno')
            }
            }
        }
    })
    resetForm()
    formReg.value = false
}

async function modificar() {

    // 1) Validamos el form
    formRef.value.validate(async valid => {
        if (!valid) return;

        const idTurno = eventos.value[eventoFecha.value][eventoHora.value].id;

        try {
        // 2) PUT al Turno (campo Hora en mayúscula)
        await axios.put(`http://127.0.0.1:8000/api/Turno/${idTurno}/`,
            {
            ID_paciente: form.paciente,
            Fecha:       eventoFecha.value,
            Hora:        eventoHora.value,
            asistencia:  form.asistencia
            }
        );

        // 3) Obtener el detalle existente
        const detalleRes = await axios.get(`http://127.0.0.1:8000/api/DetalleTurno/?turno=${idTurno}`);
        if (detalleRes.data.length > 0) {
            const idDet = detalleRes.data[0].ID_detalle;  // ajusta al nombre real de tu PK
            // 4) PUT al DetalleTurno (campo tratamiento espera ID_tratamiento)
            console.log(idDet)
            await axios.put(`http://127.0.0.1:8000/api/DetalleTurno/${idDet}/`,
            {
                ID_tratamiento: form.tratamientoSeleccionado,
                ID_turno:       idTurno,
                Observacion:    form.observacion
            }
            );
        }

        // 5) Refrescar vista
        await cargarTurnos();
        ElMessage.success('Turno modificado correctamente');
        formMod.value = false;

        } catch (err) {
        console.error('Error modificando turno:', err.response?.data || err);
        ElMessage.error('No se pudo modificar el turno');
        }
    });
}

const cargar_paciente = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/Pacientes/')
        optionsPaciente.value = response.data.map(paciente => ({
        value: paciente.ID_paciente, // Identificador único
        label: paciente.nombre + " " + paciente.apellido + " - " + paciente.dni// Nombre de los pacientes para mostrar
        })).sort((a, b) => a.label.localeCompare(b.label));
        pacienteMap.value = response.data.reduce((acc, paciente) => {
        acc[paciente.ID_paciente] = paciente; // Mapea los pacientes por su ID
        return acc
        }, {})
    } catch (error) {
        console.error('Error al cargar los pacientes:', error)
    }
}

const cargarTratamientos = async () => {
    try {
        const [tratamientosRes, tiposRes] = await Promise.all([
            axios.get('http://127.0.0.1:8000/api/Tratamiento/'),
            axios.get('http://127.0.0.1:8000/api/Tipo/')
        ])
        const tiposMap = tiposRes.data.reduce((acc, tipo) => {
            acc[tipo.ID_tratamiento] = tipo.nombre;
            return acc;
        }, {})
        optionsTratamiento.value = tratamientosRes.data.map(tratamiento => ({
            value: tratamiento.ID_tratamiento,
            label: `${tiposMap[tratamiento.tipo]} - ${tratamiento.Nombre}`
        })).sort((a, b) => a.label.localeCompare(b.label));
        tratamientoMap.value = tratamientosRes.data.reduce((acc, tratamiento) => {
            acc[tratamiento.ID_tratamiento] = tratamiento;
            return acc;
        }, {})
    } catch (error) {
        console.error('Error al cargar los tratamientos o tipos:', error)
    }
}

const cargarTurnos = async () => {
    eventos.value = {};

    const [turnosRes, detallesRes] = await Promise.all([
        axios.get('http://127.0.0.1:8000/api/Turno/'),
        axios.get('http://127.0.0.1:8000/api/DetalleTurno/')
    ]);

    const detalleMap = new Map();
    detallesRes.data.forEach(d => {
        detalleMap.set(d.ID_turno, d);
    });

    turnosRes.data.forEach(turno => {
        const fechaKey = turno.Fecha;
        const horaKey = turno.Hora.slice(0, 5);

        if (!eventos.value[fechaKey]) eventos.value[fechaKey] = {};

        const det = detalleMap.get(turno.ID_turno);

        eventos.value[fechaKey][horaKey] = {
            id: turno.ID_turno,
            pacienteId: turno.ID_paciente,
            asistencia: turno.asistencia,
            tratamientoId: det ? det.ID_tratamiento : null,
            observacion: det ? det.Observacion : ''
        };
    });
};


onMounted(() => {
    cargar_paciente()
    cargarTratamientos()
    cargarTurnos()
})

</script>

<style scoped>

/* estilos base */
::v-deep .celda-evento {
height: 40px;
line-height: 40px;
text-align: center;
cursor: pointer;
background: #f5f5f5;
transition: background 0.2s;
}
::v-deep .celda-evento:hover {
background: #e0e0e0;
}

/* celdas bloqueadas (fin de semana o hora entre 13–16) */
::v-deep .celda-evento.bloqueado {
color: #f1f0f0;
background-color: #f1f0f0;
cursor: not-allowed;
}

/* fila entera de fin de semana */
::v-deep .fila-bloqueada > td {
background-color: #f1f0f0 !important;
}

::v-deep .celda-evento.asistio {
    background-color: #dcdf13; /* verde claro */
    color: #000000; /* texto verde oscuro, opcional */
    font-weight: bold;
}

::v-deep .celda-evento.noAsistio {
    background-color: #ec1212;
    color: #000000;
    font-weight: bold;
}

::v-deep .celda-evento.libre {
    background-color: #4ee040;
    color: #000000;
    font-weight: bold;
}

</style>
