<template>
    <div style="font-size: 35px;">
        Obras Sociales
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
    
<el-table :data="obraSocialfiltrado" style="width: 100%">
    <el-table-column label="Nombre" prop="nombre" />
    <el-table-column label="Asociados" prop="asociados" />
    <el-table-column label="Operaciones">
    <template #default="scope">
        <el-dropdown>
        <el-button type="primary">
            Operaciones
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
        </el-button>
        <template #dropdown>
            <el-dropdown-menu>
            <el-dropdown-item @click="verPacientesObra(scope.row)">Detalles</el-dropdown-item>
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

<el-dialog v-model="formMod" title="Modificar Obra Social" width="500">
    <el-form :model="obraSocialAct" ref="formRef" :rules="reglas">
    <el-form-item label="Nombre" prop="nombre">
        <el-input v-model="obraSocialAct.nombre" />
    </el-form-item>
    </el-form>
    <template #footer>
    <div class="dialog-footer">
        <el-button @click="cancelar">Cancelar</el-button>
        <el-button type="primary" @click="modificar_datos">Confirmar</el-button>
    </div>
    </template>
</el-dialog>

<el-dialog v-model="formReg" title="Registrar Nueva Obra Social" width="500">
    <el-form :model="form" ref="formRef" :rules="reglas">
    <el-form-item label="Nombre" prop="nombre">
        <el-input v-model="form.nombre" />
    </el-form-item>
    </el-form>
    <template #footer>
    <div class="dialog-footer">
        <el-button @click="cancelar">Cancelar</el-button>
        <el-button type="primary" @click="registrar" round>
        Confirmar
        </el-button>
    </div>
    </template>
</el-dialog>

<el-dialog v-model="diagDetalles" title="Pacientes de la obra social" >
    <el-table :data="pacientesObra" :border="true" >
        <el-table-column label="Nombre" prop="nombre" />
        <el-table-column label="Apellido" prop="apellido" />
        <el-table-column label="DNI" prop="dni" />
        <el-table-column label="Telefono" prop="telefono" />
    </el-table>
    <template #footer>
    <div class="dialog-footer">
        <el-button @click="exportToExcelPacientes">📂 Exportar a Excel</el-button>
        <el-button @click="printListPacientes">🖨️ Imprimir</el-button>
        <el-button @click="cancelar">Cancelar</el-button>
    </div>
    </template>
</el-dialog>

<!-- Contenido para imprimir (oculto) -->
<div ref="printArea" style="display: none;">
<h2>Lista de Obras Sociales</h2>
<table border="1" cellspacing="0" cellpadding="5" style="width: 100%; text-align: left;">
<thead>
    <tr>
    <th>Nombre</th>
    <th>Asociados</th>
    </tr>
</thead>
<tbody>
    <tr v-for="p in obraSocial" :key="p.ID_os">
    <td>{{ p.nombre }}</td>
    <td>{{ p.asociados }}</td>
    </tr>
</tbody>
</table>
</div>

<div ref="printAreaPacientes" style="display: none;">
<h2>Lista de pacientes</h2>
<table border="1" cellspacing="0" cellpadding="5" style="width: 100%; text-align: left;">
<thead>
    <tr>
    <th>Nombre</th>
    <th>Apellido</th>
    <th>DNI</th>
    <th>Telefono</th>
    </tr>
</thead>
<tbody>
    <tr v-for="p in pacientesObra" :key="p.ID_os">
    <td>{{ p.nombre }}</td>
    <td>{{ p.apellido }}</td>
    <td>{{ p.dni }}</td>
    <td>{{ p.telefono }}</td>
    </tr>
</tbody>
</table>
</div>


</template>


<script lang="ts" setup>

import { ArrowDown, MoreFilled } from "@element-plus/icons-vue"; // Iconos del botón
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
import { computed, nextTick, onMounted, reactive, ref } from 'vue';
import * as XLSX from "xlsx";

const obraSocial  = ref([])
const resumen  = ref([])
const buscar = ref('')
const obraSocialAct = ref({})
const formRef = ref(null)
const formReg = ref(null)
const formMod = ref(false)
const printArea = ref(null)
const printAreaPacientes = ref(null)
const diagDetalles = ref(false)
const pacientesObra = ref([])
const obraSeleccionada = ref(null)


const exportToExcelPacientes = () => {
    const worksheet = XLSX.utils.json_to_sheet(pacientesObra.value)
    const workbook = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(workbook, worksheet, "Pacientes")
    XLSX.writeFile(workbook, "pacientes por obra social.xlsx")
}

const printListPacientes = async () => {
  await nextTick() // asegurarse que el DOM esté actualizado
    const content = printAreaPacientes.value.innerHTML

    const printWindow = window.open('', '', 'height=600,width=800')
    printWindow.document.write('<html><head><title>Lista de Pacientes</title></head><body>')
    printWindow.document.write(content)
    printWindow.document.write('</body></html>')
    printWindow.document.close()
    printWindow.focus()
    printWindow.print()
    printWindow.close()
}

const exportToExcel = () => {
    const worksheet = XLSX.utils.json_to_sheet(obraSocial.value)
    const workbook = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(workbook, worksheet, "Obras Sociales")
    XLSX.writeFile(workbook, "Obras Sociales.xlsx")
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

const reglas = {
    nombre: [{ required: true, message: 'El Nombre es obligatorio', trigger: 'blur' }]
}

const form_ini = {
    nombre: ''
}

const resetForm = () => {
    Object.assign(form, form_ini)
}

const form = reactive({ ...form_ini })

const obraSocialfiltrado = computed(() =>
    obraSocial.value.filter((data) =>
        !buscar.value ||
        Object.values(data).some((valor) =>
        String(valor).toLowerCase().includes(buscar.value.toLowerCase())
        )
    )
)

const cargar_Obras = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/Obra%20Social/')
        obraSocial.value = response.data
    } catch (error) {
        console.error(error)
    }
}

const registrar = async () => {
    formRef.value.validate(async (valid) => {
        if (valid) {
            try {
                const datos = {
                    nombre: form.nombre,
                }
                await axios.post('http://127.0.0.1:8000/api/Obra%20Social/', datos)
                resetForm()
                formReg.value = false
                await cargar_Obras()
                ElMessage.success('Se agrego correctamente')
            } catch (error) {
            if (error.response && error.response.data) {
                console.error(error.response.data)
                ElMessage.error('Error: ' + JSON.stringify(error.response.data))
            } else {
                ElMessage.error('No se pudo agregar la Obra Social')
            }
            }
        }
    })
}

const modificar = async (paciente) => {
    obraSocialAct.value = { ...paciente }

    formMod.value = true
}

const modificar_datos = async () => {
    formRef.value.validate(async (valid) => {
        if (valid) {
            try {
                const datos = {
                    nombre: obraSocialAct.value.nombre,
                }
                await axios.put(`http://localhost:8000/api/Obra%20Social/${obraSocialAct.value.ID_os}/`, datos)
                resetForm()
                formMod.value = false
                await cargar_Obras()
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

const eliminar = async (row) => {
    try {
        const confirmacion = await ElMessageBox.confirm('¿Desea seguir con la eliminacion?', 'Eliminar Obra Social', {
            confirmButtonText: 'Aceptar',
            cancelButtonText: 'Cancelar',
            type: 'warning'
        })
        if (confirmacion) {
            await axios.delete(`http://localhost:8000/api/Obra%20Social/${row.ID_os}/`)
            await cargar_Obras()
            ElMessage.success('Obra Social eliminada correctamente')
        }
    } catch (error) {
        console.error(error)
        ElMessage.error('Error al eliminar la Obra Social')
    }
}

const cancelar = () => {
    resetForm()
    formMod.value = false
    formReg.value = false
    diagDetalles.value = false
}

const verPacientesObra = async (obra) => {
    obraSeleccionada.value = obra
    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/Obra%20Social/${obraSeleccionada.value.ID_os}/pacientes/`)
        pacientesObra.value = response.data
        diagDetalles.value = true
    } catch (error) {
        console.error('Error al obtener pacientes:', error)
        ElMessage.error('No se pudieron cargar los pacientes')
    }
}

onMounted(() => {
    cargar_Obras()
})

</script>