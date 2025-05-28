<template>
<div style="font-size: 35px;">
    Pacientes
    <el-space />
    <el-button @click="formReg = true" type="primary" round>Nuevo</el-button>

    <div style="display: flex; justify-content: flex-end;">
<el-dropdown>
    <el-button type="primary" size="small">
    <el-icon><MoreFilled /></el-icon>
    </el-button>
    <template #dropdown>
    <el-dropdown-menu>
        <el-dropdown-item @click="exportToExcel">📂 Exportar a Excel</el-dropdown-item>
        <el-dropdown-item @click="printList">🖨️ Imprimir Lista</el-dropdown-item>
    </el-dropdown-menu>
    </template>
</el-dropdown>
</div>
</div>

<el-table :data="pacientefiltrado" style="width: 100%">
    <el-table-column label="Apellido" prop="apellido" />
    <el-table-column label="Nombre" prop="nombre" />
    <el-table-column label="DNI" prop="dni" />
    <el-table-column label="Telefono" prop="telefono" />
    <el-table-column label="Operaciones">
    <template #default="scope">
        <el-dropdown>
        <el-button type="primary">
            Operaciones
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
        </el-button>
        <template #dropdown>
            <el-dropdown-menu>
            <el-dropdown-item @click="detalles(scope.row)">Detalles</el-dropdown-item>
            <el-dropdown-item @click="modificar(scope.row)">Modificar</el-dropdown-item>
            <el-dropdown-item @click="eliminar(scope.row)">Eliminar</el-dropdown-item>
            </el-dropdown-menu>
        </template>
        </el-dropdown>
    </template>
    </el-table-column>
    <el-table-column align="right">
    <template #header>
        <el-input v-model="buscar" size="small" placeholder="Buscar" />
    </template>
    </el-table-column>
</el-table>

<el-dialog v-model="formReg" title="Registrar Nuevo Paciente" width="500">
    <el-form :model="form" ref="formRef" :rules="reglas">
    <el-form-item label="Nombre" prop="nombre">
        <el-input v-model="form.nombre" />
    </el-form-item>
    <el-form-item label="Apellido" prop="apellido">
        <el-input v-model="form.apellido" />
    </el-form-item>
    <el-form-item label="DNI" prop="dni">
        <el-input v-model="form.dni" placeholder="Ingrese el DNI sin puntos"/>
    </el-form-item>
    <el-form-item label="Fecha de nacimiento" prop="fechaNac">
        <el-date-picker
        v-model="form.fechaNac"
        type="date"
        placeholder="Seleccione una fecha"
        :size="size"
        format="DD/MM/YYYY"
        value-format="YYYY-MM-DD"
        />
    </el-form-item>
    <el-form-item label="Telefono" prop="telefono">
        <el-input v-model="form.telefono" />
    </el-form-item>
    <el-form-item label="Direccion" prop="direccion">
        <el-input v-model="form.direccion" show-word-limit maxlength="100" />
    </el-form-item>
    <el-form-item label="Obra Social" prop="obra_social">
        <div style="display: flex; gap: 8px; align-items: center; width: 100%;">
        <el-select
            v-model="form.obra_social"
            placeholder="Selecciona una Obra Social"
            filterable
            clearable
            style="flex: 1"
            >
            <el-option
                v-for="obra in options"
                :key="obra.value"
                :label="obra.label"
                :value="obra.value"
            />
        </el-select>
        <el-button type="primary" circle @click="formRegObra = true" plain>
            <span style="font-weight: bold;">+</span>
        </el-button>
        </div>
    </el-form-item>

    </el-form>
    <template #footer>
    <div class="dialog-footer">
        <el-button type="primary" @click="registrar" round>Confirmar</el-button>
        <el-button @click="cancelar">Cancelar</el-button>
    </div>
    </template>
</el-dialog>

<el-dialog v-model="formRefMod" title="Modificar Paciente" width="500">
    <el-form :model="pacienteAct" ref="formRef" :rules="reglas">
    <el-form-item label="Nombre" prop="nombre">
        <el-input v-model="pacienteAct.nombre" />
    </el-form-item>
    <el-form-item label="Apellido" prop="apellido">
        <el-input v-model="pacienteAct.apellido" />
    </el-form-item>
    <el-form-item label="DNI" prop="dni">
        <el-input v-model="pacienteAct.dni" />
    </el-form-item>
    <el-form-item label="Fecha de nacimiento" prop="fechaNac">
        <el-date-picker
        v-model="pacienteAct.fecha_nacimiento"
        type="date"
        placeholder="Pick a day"
        format="DD/MM/YYYY"
        value-format=""
        />
    </el-form-item>
    <el-form-item label="Telefono" prop="telefono">
        <el-input v-model="pacienteAct.telefono" />
    </el-form-item>
    <el-form-item label="Direccion" prop="direccion">
        <el-input v-model="pacienteAct.direccion" show-word-limit maxlength="100" />
    </el-form-item>
    <el-form-item label="Obra Social" prop="obra_social">
    <div style="display: flex; gap: 8px; align-items: center; width: 100%;">
    <el-select
        v-model="pacienteAct.obra_social"
        placeholder="Selecciona una Obra Social"
        filterable
        clearable
        >
        <el-option
        v-for="obra in options"
        :key="obra.value"
        :label="obra.label"
        :value="obra.value"
        />
    </el-select>
    <el-button type="primary" circle @click="formRegObra = true" plain>
            <span style="font-weight: bold;">+</span>
    </el-button>
    </div>
    </el-form-item>
    </el-form>
    <template #footer>
    <div class="dialog-footer">
        <el-button @click="cancelar">Cancelar</el-button>
        <el-button type="primary" @click="modificar_datos">Confirmar</el-button>
    </div>
    </template>
</el-dialog>

<el-dialog v-model="diag_detalles" title="Detalles del Paciente">
    <el-form :model="form" ref="formRef">
    <el-form-item label="Nombre" prop="nombre" >
        <el-input v-model="pacienteAct.nombre" disabled />
    </el-form-item>
    <el-form-item label="Apellido" prop="apellido" >
        <el-input v-model="pacienteAct.apellido" disabled />
    </el-form-item>
    <el-form-item label="Fecha de nacimiento" prop="fechaNac">
    <el-date-picker
        v-model="pacienteAct.fecha_nacimiento"
        type="date"
        format="DD/MM/YYYY"
        value-format=""
        placeholder="Pick a day"
        :size="size"
        disabled
    />
    </el-form-item>
    <el-form-item label="Telefono" prop="telefono" >
        <el-input v-model="pacienteAct.telefono" disabled />
    </el-form-item>
    <el-form-item label="Direccion" prop="direccion" >
        <el-input v-model="pacienteAct.direccion" disabled />
    </el-form-item>
    <el-form-item label="Obra Social" prop="obra_social">
        <el-input :value="obraMap[pacienteAct.obra_social]?.nombre || 'No especificada'" disabled />
    </el-form-item>
    </el-form>
    <template #footer>
    <div class="dialog-footer">
        <el-button round type="primary" @click="abrirHistoriaClinica(pacienteAct)">Historia Clinica</el-button>
        <el-button @click="abrirOdontogramas(pacienteAct)">Odontograma</el-button>
        <el-button @click="abrirRadiografia(pacienteAct)">Radiografia</el-button>
        <el-button @click="cancelar">Cancelar</el-button>
    </div>
    </template>
</el-dialog>

<el-dialog v-model="formRegObra" title="Registrar Nueva Obra Social" width="500">
    <el-form :model="formObra" ref="formObraRef" :rules="{ nombre: [{ required: true, message: 'El Nombre es obligatorio', trigger: 'blur' }] }">
        <el-form-item label="Nombre" prop="nombre">
        <el-input v-model="formObra.nombre" />
        </el-form-item>
    </el-form>
    <template #footer>
        <div class="dialog-footer">
        <el-button @click="cancelarObra">Cancelar</el-button>
        <el-button type="primary" @click="registrar_obra" round>Confirmar</el-button>
        </div>
    </template>
</el-dialog>


<el-dialog v-model="historiaClinica" title="Historia Clínica">
    <el-table :data="historiaClinicaData" :border="true">
        <el-table-column label="Fecha" prop="fecha" />
        <el-table-column label="Hora" prop="hora" />
        <el-table-column label="Tratamiento" prop="tratamiento" />
        <el-table-column label="Observaciones" prop="observacion" />
        <el-table-column label="Radiografía">
            <template #default="{ row }">
                <div style="display: flex; flex-direction: column; align-items: center;">
                <template v-if="row.radiografia === 'Sin Radiografia'">
                    <span style="color: #999;">No disponible</span>
                </template>
                <template v-else>
                    <el-button
                    type="primary"
                    icon="Download"
                    size="small"
                    style="margin-top: 5px;"
                    @click="downloadImage(row.radiografia, `radiografia ${row.tratamiento}.jpg`)"
                    >
                    Descargar
                    </el-button>
                </template>
                </div>
            </template>
        </el-table-column>
        <el-table-column label="Pieza" prop="pieza" />
        <el-table-column label="Asistencia" prop="asistencia" />
    </el-table>
    <template #footer>
        <div class="dialog-footer">
        <el-button @click="exportarHistoria">📂 Exportar a Excel</el-button>
        <el-button @click="imprimirHistoria">🖨️ Imprimir</el-button>
        <el-button @click="cancelarHistoria">Cancelar</el-button>
        </div>
    </template>
</el-dialog>

<el-dialog v-model="radiografia" title="Radiografias">
    <el-table :data="radiografiaData" :border="true">
        <el-table-column label="Fecha" prop="fecha" />
        <el-table-column label="Tipo" prop="tipo" />
        <el-table-column label="Observaciones" prop="observacion" />
        <el-table-column label="Tratamiento" prop="tratamiento" />
        <el-table-column label="Pieza" prop="pieza" />
        <el-table-column label="Radiografía">
        <template #default="{ row }">
            <div style="display: flex; flex-direction: column; align-items: center;">
                <el-button
                    type="primary"
                    icon="Download"
                    size="small"
                    style="margin-top: 5px;"
                    @click="downloadImage(row.radiografia, `radiografia ${row.pieza}.jpg`)"
                >
                    Descargar
                </el-button>
            </div>
        </template>
        </el-table-column>
        <el-table-column label="Eliminar">
            <template #default="scope">
            <el-button type="danger" round  icon="Delete" @click="eliminarRad(scope.row)">Eliminar</el-button>
            </template>
        </el-table-column>

    </el-table>
    <template #footer>
        <div class="dialog-footer">
        <el-button @click="abrirNuevaRad(pacienteAct)" round type="primary">Nuevo</el-button>
        <el-button @click="cancelarRadiografia">Cancelar</el-button>
        </div>
    </template>
</el-dialog>

<el-dialog v-model="nuevaRad" title="Cargar Radiografía" width="500">
    <el-form :model="formRad" ref="formRef">
    <el-form-item label="Turno" prop="turno">
        <div style="display: flex; gap: 8px; align-items: center; width: 100%;">
        <el-select
            v-model="formRad.turno"
            placeholder="Selecciona un turno del paciente"
            filterable
            clearable
            style="flex: 1"
            >
            <el-option
                v-for="obra in optionsTurno"
                :key="obra.value"
                :label="obra.label"
                :value="obra.value"
            />
        </el-select>
        </div>
    </el-form-item>
    <el-form-item label="Archivo" prop="imagen">
        <el-upload
            v-model:file-list="fileList"
            class="upload-demo"
            :auto-upload="false"
            :on-change="handleFileChange"
            :limit="1"
            >
            <el-button type="primary">Subir archivo</el-button>
        </el-upload>
    </el-form-item>
    <el-form-item label="Pieza" prop="pieza">
        <div style="display: flex; gap: 8px; align-items: center; width: 100%;">
        <el-select
            v-model="formRad.pieza"
            placeholder="Selecciona una píeza dental"
            filterable
            clearable
            style="flex: 1"
            >
            <el-option
                v-for="obra in optionsPieza"
                :key="obra.value"
                :label="obra.label"
                :value="obra.value"
            />
        </el-select>
        </div>
    </el-form-item>
    <el-form-item label="Tipo" prop="tipo">
        <el-input v-model="formRad.tipo" />
    </el-form-item>
    <el-form-item>
        <el-input
        v-model="formRad.observacion"
        style="width: 500px"
        :rows="5"
        type="textarea"
        placeholder="Observaciones"
        />
    </el-form-item>
    </el-form>
    <template #footer>
        <div class="dialog-footer">
        <el-button @click="guardarRadiografia" round type="primary">Guardar</el-button>
        <el-button @click="cancelarNuevaRad">Cancelar</el-button>
        </div>
    </template>
</el-dialog>

<el-dialog v-model="listaOdontograma" title="Odontogramas">
<El-table :data="odontogramaData" style="width: 100%" :border="true">
    <el-table-column label="Fecha" prop="fecha"/>
    <el-table-column label="Observaciones" prop="observaciones"/>
    <el-table-column label="Odontograma">
        <template #default="scope">
        <el-button
        round
        type="success"
        icon="Download"
        @click=""
        >
        Ver
        </el-button>
        </template>
    </el-table-column>
    </El-table>
    <template #footer>
        <div class="dialog-footer">
        <el-button @click="cancelarListaOdontograma">Cancelar</el-button>
        </div>
    </template>
</el-dialog>

<!-- Contenido para imprimir (oculto) -->
<div ref="printArea" style="display: none;">
<h2>Lista de Pacientes</h2>
<table border="1" cellspacing="0" cellpadding="5" style="width: 100%; text-align: left;">
<thead>
    <tr>
    <th>Nombre</th>
    <th>Apellido</th>
    <th>DNI</th>
    <th>Fecha de Nacimiento</th>
    <th>Teléfono</th>
    <th>Dirección</th>
    <th>Obra Social</th>
    </tr>
</thead>
<tbody>
    <tr v-for="p in paciente" :key="p.id">
    <td>{{ p.nombre }}</td>
    <td>{{ p.apellido }}</td>
    <td>{{ p.dni }}</td>
    <td>{{ p.fecha_nacimiento }}</td>
    <td>{{ p.telefono }}</td>
    <td>{{ p.direccion }}</td>
    <td>{{ obraMap[p.obra_social]?.nombre || 'No especificada' }}</td>
    </tr>
</tbody>
</table>
</div>

</template>

<script lang="ts" setup>

import { ArrowDown, MoreFilled } from "@element-plus/icons-vue"
import axios from 'axios'
import { ElMessage, ElMessageBox, rowContextKey } from 'element-plus'
import { computed, nextTick, onMounted, reactive, ref } from 'vue'
import * as XLSX from "xlsx"

const paciente = ref([])
const buscar = ref('')
const formReg = ref(false)
const formRegObra = ref(false)
const formMod = ref(false)
const formRef = ref(null)
const diag_detalles = ref(false)
const historiaClinica =ref(false)
const radiografia = ref(false)
const pacienteAct = ref({})
const formRefMod = ref(null)
const obraMap = ref({})
const options = ref([])
const printArea = ref(null)
const historiaClinicaData = ref([])
const radiografiaData = ref([])
const nuevaRad = ref(false)
const optionsTurno = ref([])
const turnoMap = ref({})
const optionsPieza = ref([])
const piezaMap = ref({})
const fileList = ref<File[]>([])
const listaOdontograma = ref(false)
const odontogramaData = ref([])

const formObraIni = { nombre: '' }
const formObra = reactive({ ...formObraIni })
const formObraRef = ref<typeof formObra>(null)


const exportToExcel = () => {
    const worksheet = XLSX.utils.json_to_sheet(paciente.value)
    const workbook = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(workbook, worksheet, "Pacientes")
    XLSX.writeFile(workbook, "pacientes.xlsx")
}

const printList = async () => {
  await nextTick() // asegurarse que el DOM esté actualizado
    const content = printArea.value.innerHTML

    const printWindow = window.open('', '', 'height=600,width=800')
    printWindow.document.write('<html><head><title>Lista de Pacientes</title></head><body>')
    printWindow.document.write(content)
    printWindow.document.write('</body></html>')
    printWindow.document.close()
    printWindow.focus()
    printWindow.print()
    printWindow.close()
}

const pacientefiltrado = computed(() =>
    paciente.value.filter((data) =>
        !buscar.value ||
        Object.values(data).some((valor) =>
        String(valor).toLowerCase().includes(buscar.value.toLowerCase())
        )
    )
)

const form_ini = {
    nombre: '',
    apellido: '',
    dni: '',
    fechaNac: '',
    telefono: '',
    direccion: '',
    obra_social: null,
}

const form = reactive({ ...form_ini })

const formRadini = {
    imagen: null,
    pieza: '',
    paciente: '',
    observacion: '',
    tipo: '',
    turno: ''
}

const formRad = reactive({...formRadini })

const cargar_paciente = async () => {
    try {
        const response = await axios.get('http://localhost:8000/api/Pacientes/')
        paciente.value = response.data.sort((a, b) => {
            const apellidoCompare = a.apellido.localeCompare(b.apellido)
            if (apellidoCompare !== 0) return apellidoCompare
            return a.nombre.localeCompare(b.nombre)
        })
    } catch (error) {
        console.error(error)
    }
}

const reglas = {
    nombre: [{ required: true, message: 'El Nombre es obligatorio', trigger: 'blur' }],
    dni: [{ required: true, message: 'El Dni es obligatorio', trigger: 'blur' }]
}

const fechaP = (date) => {
    if (!date) return null; // Verifica si la fecha está vacía o no definida
    const d = new Date(date);  // Crea un objeto Date a partir de la entrada
    if (isNaN(d.getTime())) return null;  // Verifica si la fecha es válida
    // Obtener el año, mes y día manualmente para evitar desfases por zona horaria
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0'); // Asegura que el mes tenga 2 dígitos
    const day = String(d.getDate()).padStart(2, '0');  // Asegura que el día tenga 2 dígitos
    return `${year}-${month}-${day}`;  // Retorna la fecha en formato YYYY-MM-DD
}

const registrar = async () => {
    formRef.value.validate(async (valid) => {
        
        if (valid) {
            try {
                const datos = {
                    nombre: form.nombre,
                    apellido: form.apellido,
                    dni: form.dni,
                    fecha_nacimiento: form.fechaNac,
                    direccion: form.direccion,
                    telefono: form.telefono,
                    obra_social: form.obra_social,
                }
                await axios.post('http://127.0.0.1:8000/api/Pacientes/', datos)
                resetForm()
                formReg.value = false
                await cargar_paciente()
                ElMessage.success('Se agrego correctamente')
            } catch (error) {
            if (error.response && error.response.data) {
                console.error(error.response.data)
                ElMessage.error('Error: ' + JSON.stringify(error.response.data))
            } else {
                ElMessage.error('No se pudo agregar el Paciente')
            }
            }
        }
    })
}

const registrar_obra = async () => {
    formObraRef.value.validate(async (valid: boolean) => {
        if (!valid) return
        try {
        const datos = { nombre: formObra.nombre }
        // asegúrate aquí de la URL real de tu endpoint:
        await axios.post('http://127.0.0.1:8000/api/Obra%20Social/', datos)
        ElMessage.success('Obra Social creada correctamente')
        // limpiar el formulario
        Object.assign(formObra, formObraIni)
        formRegObra.value = false
        await cargar_Obras()
        } catch (error: any) {
        console.error(error.response?.data || error)
        ElMessage.error('Error al crear la Obra Social')
        }
    })
}

const resetForm = () => {
    Object.assign(form, form_ini)
}

const resetFormRad = () => {
    Object.assign(formRad, formRadini)
}

const cancelar = () => {
    resetForm()
    formReg.value = false
    formMod.value = false
    diag_detalles.value = false
    formRefMod.value = false
}

const cancelarObra = () => {
    resetForm()
    formRegObra.value = false
}

const cancelarHistoria = () => {
    historiaClinica.value = false
}

const cancelarRadiografia = () => {
    radiografia.value = false
}

const cancelarListaOdontograma = () => {
    listaOdontograma.value = false
}

const cancelarNuevaRad = () => {
    resetFormRad()
    nuevaRad.value = false
}

const modificar = async (paciente) => {
    pacienteAct.value = { ...paciente }

    form.obra_social = pacienteAct.value.obra_social

    formRefMod.value = true
}

const modificar_datos = async () => {
    formRef.value.validate(async (valid) => {
        if (valid) {
            try {
                const datos = {
                    nombre: pacienteAct.value.nombre,
                    apellido: pacienteAct.value.apellido,
                    dni: pacienteAct.value.dni,
                    fecha_nacimiento: fechaP(pacienteAct.value.fecha_nacimiento),
                    direccion: pacienteAct.value.direccion,
                    telefono: pacienteAct.value.telefono,
                    obra_social: pacienteAct.value.obra_social,
                }
                await axios.put(`http://localhost:8000/api/Pacientes/${pacienteAct.value.ID_paciente}/`, datos)
                resetForm()
                formRefMod.value = false
                await cargar_paciente()
                ElMessage.success('Se modificó correctamente')
            } catch (error) {
            if (error.response && error.response.data) {
                console.error(error.response.data)
                ElMessage.error('Error: ' + JSON.stringify(error.response.data))
            } else {
                ElMessage.error('No se pudo modificar el Paciente')
            }
            }
        }
    })
}

const detalles = async (paciente) => {
    pacienteAct.value = { ...paciente }
    diag_detalles.value = true
}

const eliminar = async (row) => {
    try {
        const confirmacion = await ElMessageBox.confirm('¿Desea seguir con la eliminacion?', 'Eliminar Paciente', {
            confirmButtonText: 'Aceptar',
            cancelButtonText: 'Cancelar',
            type: 'warning'
        })
        if (confirmacion) {
            await axios.delete(`http://127.0.0.1:8000/api/Pacientes/${row.ID_paciente}/`)
            await cargar_paciente()
            ElMessage.success('Paciente eliminado correctamente')
        }
    } catch (error) {
        console.error(error)
        ElMessage.error('Error al eliminar paciente')
    }
}

const eliminarRad = async (row) => {
    try {
        const confirmacion = await ElMessageBox.confirm('¿Desea seguir con la eliminacion?', 'Eliminar Radiografia', {
            confirmButtonText: 'Aceptar',
            cancelButtonText: 'Cancelar',
            type: 'warning'
        })
        if (confirmacion) {
            await axios.delete(`http://127.0.0.1:8000/api/Radiografia/${row.id}/`)
            await verRadiografia(pacienteAct.value.ID_paciente)
            ElMessage.success('Radiografia eliminada correctamente')
        }
    } catch (error) {
        console.error(error)
        ElMessage.error('Error al eliminar Radiografia')
    }
}

async function abrirHistoriaClinica(pacienteAct) {
    await verHistoriaClinica(pacienteAct.ID_paciente)
    historiaClinica.value = true
}

async function verHistoriaClinica(pacienteAct) {
    try {
        const [turnosRes, detallesRes, tratamientosRes, radiografiasRes] = await Promise.all([
            axios.get(`http://127.0.0.1:8000/api/Turno/?ID_paciente=${pacienteAct}`),
            axios.get('http://127.0.0.1:8000/api/DetalleTurno/'),
            axios.get('http://127.0.0.1:8000/api/Tratamiento/'),
            axios.get(`http://127.0.0.1:8000/api/Radiografia/?ID_paciente=${pacienteAct}`),
        ]);

        const turnos = turnosRes.data;
        const detalles = detallesRes.data;
        const tratamientos = tratamientosRes.data;
        const radiografias = radiografiasRes.data;

        const historia = [];

        // Agregar tratamientos
        turnos.forEach(turno => {
            const detallesDelTurno = detalles.filter(detalle => detalle.turno === turno.id);

            detallesDelTurno.forEach(detalle => {
                const tratamiento = tratamientos.find(t => t.id === detalle.tratamiento);

                historia.push({
                    fecha: turno.Fecha,
                    hora: turno.Hora,
                    tratamiento: tratamiento?.Nombre || '',
                    observacion: detalle?.Observacion || '',
                    radiografia: 'Sin Radiografia',
                    pieza: '-',
                    asistencia: turno.asistencia ? 'Sí' : 'No',
                });
            });
        });

        // Agregar radiografías
        radiografias.forEach(radio => {
            const turno = turnos.find(t => t.ID_turno === radio.turno);
            const detalle = detalles.find(d => d.ID_turno === radio.turno);
            const tratamiento = detalle ? tratamientos.find(t => t.ID_turno === detalle.ID_tratamiento) : null;

            historia.push({
                fecha: turno?.Fecha || 'Sin fecha',
                hora: turno?.Hora || '-',
                tratamiento: tratamiento?.Nombre || 'Sin tratamiento',
                observacion: radio.observacion || '',
                radiografia: radio?.imagen || 'Sin Radiografia',
                pieza: radio?.pieza ?? 'Desconocida',
                asistencia: turno?.asistencia ? 'Sí' : 'No',
            });
        });

        historiaClinicaData.value = historia;
    } catch (error) {
        console.error('Error al cargar historia clínica:', error);
    }
}

async function abrirRadiografia(pacienteAct) {
    await verRadiografia(pacienteAct.ID_paciente)
    radiografia.value = true
}

async function verRadiografia(pacienteAct) {
    try {
        // Obtener datos de radiografías, turnos, detalles, tratamientos y piezas
        const { data: radiografias } = await axios.get(`http://127.0.0.1:8000/api/Radiografia/?paciente=${pacienteAct}`)
        const { data: turnos } = await axios.get(`http://127.0.0.1:8000/api/Turno/?paciente=${pacienteAct}`)
        const { data: detalles } = await axios.get('http://127.0.0.1:8000/api/DetalleTurno/')
        const { data: tratamientos } = await axios.get('http://127.0.0.1:8000/api/Tratamiento/')
        const { data: piezas } = await axios.get('http://127.0.0.1:8000/api/Pieza/')

        // Formatear los datos de las radiografías
        const radiografiaFormateada = radiografias.map(radio => {
            const turno = turnos.find(t => t.ID_turno === radio.ID_turno)
            const detalle = detalles.find(d => d.ID_turno === radio.ID_turno)
            const tratamiento = detalle ? tratamientos.find(t => t.ID_tratamiento === detalle.ID_tratamiento) : null
            const pieza = piezas.find(p => p.ID_diente === radio.ID_pieza) // Buscar el nombre de la pieza

            return {
                id: radio.ID_radiografia,
                fecha: turno?.Fecha || 'Sin fecha',
                tipo: radio.tipo,
                observacion: radio.observacion,
                tratamiento: tratamiento?.Nombre || 'Sin tratamiento',
                pieza: pieza ? pieza.nombre : 'Pieza desconocida',
                radiografia: radio?.imagen || "Sin Radiografia"
            };
        });

        // Asignar los datos formateados a la variable de datos
        radiografiaData.value = radiografiaFormateada
    } catch (error) {
        console.error('Error al cargar las Radiografías:', error);
    }
}

const cargar_Obras = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/Obra%20Social/')
        options.value = response.data.map(obra => ({
        value: obra.ID_os, // Identificador único
        label: obra.nombre // Nombre de la obra social para mostrar
        }))
        obraMap.value = response.data.reduce((acc, obra) => {
        acc[obra.ID_os] = obra; // Mapea los Obras Sociales por su ID
        return acc
        }, {})
    } catch (error) {
        console.error('Error al cargar las Obras Sociales:', error)
    }
}

async function abrirNuevaRad(pacienteAct) {
    await verTurnos(pacienteAct)
    nuevaRad.value = true
}

async function verTurnos(pacienteAct) {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/Turno/?paciente=${pacienteAct.id}`)
        optionsTurno.value = response.data.map(obra => ({
        value: obra.id, // Identificador único
        label: obra.fecha + " - " + obra.hora_inicio
        }))
        turnoMap.value = response.data.reduce((acc, obra) => {
        acc[obra.id] = obra; // Mapea los turnos por id
        return acc
        }, {})
    } catch (error) {
        console.error('Error al cargar los tratamientos:', error)
    }
}

const cargarPieza = async () => {
    try {
        const response = await axios.get("http://127.0.0.1:8000/api/Pieza/")
        optionsPieza.value = response.data.map(obra => ({
        value: obra.id, // Identificador único
        label: obra.nombre
        }))
        piezaMap.value = response.data.reduce((acc, obra) => {
        acc[obra.id] = obra; // Mapea las piezas por id
        return acc
        }, {})
    } catch (error) {
        console.error('Error al cargar las piesas dentales:', error)
    }
}

onMounted(() => {
    cargar_paciente()
    cargar_Obras()
    cargarPieza()
})

const downloadImage = async (imageUrl: string, filename: string) => {
    try {
        // Obtener la imagen como Blob
        const response = await fetch(imageUrl)
        const blob = await response.blob()

        // Crear un enlace para la descarga
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = filename
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
    } catch (error) {
        console.error('Error al descargar la imagen:', error)
    }
}

function handleFileChange(uploadFile: any, uploadFiles: any[]) {
    formRad.imagen = uploadFile.raw
}

async function guardarRadiografia() {
    if (!formRad.imagen) {
        ElMessage.warning('Por favor selecciona un archivo antes de guardar.')
        return
    }

    const formData = new FormData()
    formData.append('pieza', String(formRad.pieza))
    formData.append('paciente', String(pacienteAct.value.ID_paciente))
    formData.append('imagen', formRad.imagen)
    formData.append('observacion', formRad.observacion)
    formData.append('tipo', formRad.tipo)
    formData.append('turno', String(formRad.turno))

    try {
        await axios.post('http://127.0.0.1:8000/api/Radiografia/', formData)
        resetFormRad()
        ElMessage.success('Radiografía cargada correctamente.')
        nuevaRad.value = false
        fileList.value = []
    } catch (err: any) {
    console.error('Error BackEnd:', err.response?.data || err)
    ElMessage.error('Error al subir la radiografía.')
    }
}

async function abrirOdontogramas(pacienteAct) {
    await verOdontogramas(pacienteAct.id)
    listaOdontograma.value = true
}

async function verOdontogramas(pacienteAct) {
    try {
        // Obtener datos de radiografías, turnos, detalles, tratamientos y piezas
        const { data: odontogramas } = await axios.get(`http://127.0.0.1:8000/api/Odontograma/?paciente=${pacienteAct}`)
        const { data: turnos } = await axios.get(`http://127.0.0.1:8000/api/Turno/?paciente=${pacienteAct}`)

        // Formatear los datos de las radiografías
        const odontogramaFormateado = odontogramas.map(odonto => {
            const turno = turnos.find(t => t.id === odonto.turno)

            return {
                id: odonto.id,
                fecha: turno?.fecha || 'Sin fecha',
                observaciones: odonto?.observacion || 'Sin Observaciones'
            };
        });

        // Asignar los datos formateados a la variable de datos
        odontogramaData.value = odontogramaFormateado
    } catch (error) {
        console.error('Error al cargar las Radiografías:', error);
    }
}

</script>

