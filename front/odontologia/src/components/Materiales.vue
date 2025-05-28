<template>

<div style="font-size: 35px;">
    Materiales
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

<el-table :data="materialfiltrado" :row-class-name="rowClassName" style="width: 100%">
    <el-table-column label="Nombre" prop="Nombre" />
    <el-table-column label="Cantidad" prop="cantidad" />
    <el-table-column label="Minimo" prop="min" />
    <el-table-column label="Operaciones">
    <template #default="scope">
        <el-dropdown>
        <el-button type="primary">
            Operaciones
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
        </el-button>
        <template #dropdown>
            <el-dropdown-menu>
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


<el-dialog v-model="formReg" title="Registrar Nuevo Material" width="500">
    <el-form :model="form" ref="formRef" :rules="reglas">
    <el-form-item label="Nombre" prop="Nombre">
        <el-input v-model="form.nombre" />
    </el-form-item>
    <el-form-item label="Cantidad" prop="cantidad">
        <el-input v-model="form.cantidad" />
    </el-form-item>
    <el-form-item label="Minimo" prop="min">
        <el-input v-model="form.minimo" />
    </el-form-item>
    </el-form>
    <template #footer>
    <div class="dialog-footer">
        <el-button @click="cancelar">Cancelar</el-button>
        <el-button type="primary" @click="registrar" round>Confirmar</el-button>
    </div>
    </template>
</el-dialog>

<el-dialog v-model="formMod" title="Modificar Material" width="500">
    <el-form :model="materialAct" ref="formRef" :rules="reglas">
    <el-form-item label="Nombre" prop="Nombre">
        <el-input v-model="materialAct.Nombre" />
    </el-form-item>
    <el-form-item label="Cantidad" prop="cantidad">
        <el-input v-model="materialAct.cantidad" />
    </el-form-item>
    <el-form-item label="Minimo" prop="min">
        <el-input v-model="materialAct.min" />
    </el-form-item>
    </el-form>
    <template #footer>
    <div class="dialog-footer">
        <el-button @click="cancelar">Cancelar</el-button>
        <el-button type="primary" @click="modificarDatos" round>Confirmar</el-button>
    </div>
    </template>
</el-dialog>

<div ref="printArea" style="display: none;">
<h2>Lista de Matariales</h2>
<table border="1" cellspacing="0" cellpadding="5" style="width: 100%; text-align: left;">
<thead>
    <tr>
    <th>Nombre</th>
    <th>Cantidad</th>
    <th>Minimo</th>
    </tr>
</thead>
<tbody>
    <tr v-for="p in materialfiltrado" :key="p.id">
    <td>{{ p.Nombre }}</td>
    <td>{{ p.cantidad }}</td>
    <td>{{ p.min }}</td>
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

const material = ref([])
const buscar = ref('')
const formRef = ref(null)
const formReg = ref(false)
const formMod = ref(false)
const materialAct = ref({})
const printArea = ref(null)

const exportToExcel = () => {
    const worksheet = XLSX.utils.json_to_sheet(material.value)
    const workbook = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(workbook, worksheet, "Matariales")
    XLSX.writeFile(workbook, "Matariales.xlsx")
}

const printList = async () => {
  await nextTick() // asegurarse que el DOM esté actualizado
    const content = printArea.value.innerHTML

    const printWindow = window.open('', '', 'height=600,width=800')
    printWindow.document.write('<html><head><title>Lista de Matariales</title></head><body>')
    printWindow.document.write(content)
    printWindow.document.write('</body></html>')
    printWindow.document.close()
    printWindow.focus()
    printWindow.print()
    printWindow.close()
}

const materialfiltrado = computed(() =>
    material.value.filter((data) =>
        !buscar.value ||
        Object.values(data).some((valor) =>
        String(valor).toLowerCase().includes(buscar.value.toLowerCase())
        )
    )
)

const form_ini = {
    nombre: '',
    cantidad: '',
    minimo: '',
}

const form = reactive({ ...form_ini })

const reglas = {
    nombre: [{ required: true, message: 'El Nombre es obligatorio', trigger: 'blur' }],
    cantidad: [{ required: true, message: 'La Cantidad es obligatorio', trigger: 'blur' }],
    minimo: [{ required: true, message: 'El Minimo es obligatorio', trigger: 'blur' }]
}

const resetForm = () => {
    Object.assign(form, form_ini)
}

const registrar = async () => {
    formRef.value.validate(async (valid) => {
        if (valid) {
            try {
                const datos = {
                    Nombre: form.nombre,
                    cantidad: form.cantidad,
                    min: form.minimo,
                }
                await axios.post('http://127.0.0.1:8000/api/Material/', datos)
                resetForm()
                formReg.value = false
                await cargar_material()
                ElMessage.success('Se agrego correctamente')
            } catch (error) {
            if (error.response && error.response.data) {
                console.error(error.response.data)
                ElMessage.error('Error: ' + JSON.stringify(error.response.data))
            } else {
                ElMessage.error('No se pudo agregar el Material')
            }
            }
        }
    })
}

const modificar = async (material) => {
    materialAct.value = { ...material }

    formMod.value = true
}

const modificarDatos = async () => {
    formRef.value.validate(async (valid) => {
        if (valid) {
            try {
                const datos = {
                    Nombre: materialAct.value.Nombre,
                    cantidad: materialAct.value.cantidad,
                    min: materialAct.value.min,
                }
                await axios.put(`http://localhost:8000/api/Material/${materialAct.value.ID_material}/`, datos)
                resetForm()
                formMod.value = false
                await cargar_material()
                ElMessage.success('Se modificó correctamente')
            } catch (error) {
            if (error.response && error.response.data) {
                console.error(error.response.data)
                ElMessage.error('Error: ' + JSON.stringify(error.response.data))
            } else {
                ElMessage.error('No se pudo modificar el Material')
            }
            }
        }
    })
}

const cancelar = () => {
    resetForm()
    formReg.value = false
    formMod.value = false
}

const eliminar = async (row) => {
    try {
        const confirmacion = await ElMessageBox.confirm('¿Desea seguir con la eliminacion?', 'Eliminar Material', {
            confirmButtonText: 'Aceptar',
            cancelButtonText: 'Cancelar',
            type: 'warning'
        })
        if (confirmacion) {
            await axios.delete(`http://localhost:8000/api/Material/${row.ID_material}/`)
            await cargar_material()
            ElMessage.success('Material eliminado correctamente')
        }
    } catch (error) {
        console.error(error)
        ElMessage.error('Error al eliminar Material')
    }
}

const cargar_material = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/Material/')
        material.value = response.data;
    } catch (error) {
        console.error(error)
    }
}

const rowClassName = ({ row }: { row: any }) => {
    if (row.cantidad < row.min) {
        return 'low-stock';
    } else if (row.cantidad < row.min * 1.25) {
        return 'medium-stock';
    }
    return '';
}

onMounted(() => {
    cargar_material()
})

</script>

<style scoped>
/* fila entera en rojo muy suave */
::v-deep .low-stock td {
    background-color: #ffecec;
    color: #d93025;
}

/* fila entera en amarillo algo suave */
::v-deep .medium-stock td {
    background-color: #ffffc8;
    color: #d8d51e;
}
</style>