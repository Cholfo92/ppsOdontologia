<template>

    <div style="font-size: 35px;">
        Tipos de tratamientos
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
    
    <el-table :data="tipofiltado" style="width: 100%">
        <el-table-column label="Nombre" prop="nombre" />
        <el-table-column label="Cantidad" prop="cantidad" />
        <el-table-column label="Operaciones">
        <template #default="scope">
            <el-dropdown>
            <el-button type="primary">
                Operaciones
                <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </el-button>
            <template #dropdown>
                <el-dropdown-menu>
                <el-dropdown-item @click="verTratamientoTipo(scope.row)">Detalles</el-dropdown-item>
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

<el-dialog v-model="formReg" title="Registrar Nuevo Tipo de Tratamiento" width="500">
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

<el-dialog v-model="formMod" title="Modificar Tipo de Tratamiento" width="500">
    <el-form :model="tipoAct" ref="formRef" :rules="reglas">
    <el-form-item label="Nombre" prop="nombre">
        <el-input v-model="tipoAct.nombre" />
    </el-form-item>
    </el-form>
    <template #footer>
    <div class="dialog-footer">
        <el-button @click="cancelar">Cancelar</el-button>
        <el-button type="primary" @click="modificar_datos">Confirmar</el-button>
    </div>
    </template>
</el-dialog>

<el-dialog v-model="diagDetalles" title="" >
    <div style="font-size: 35px;">
        Tratamientos
        <el-space />
        <el-button @click="formRegTratamiento = true" type="primary" round>Nuevo</el-button>
    </div>
    <el-table :data="tratamientoTipo" :border="true" >
        <el-table-column label="Nombre" prop="Nombre" />
        <el-table-column label="Operaciones">
        <template #default="scope">
            <el-dropdown>
            <el-button type="primary">
                Operaciones
                <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </el-button>
            <template #dropdown>
                <el-dropdown-menu>
                <el-dropdown-item @click="detallesTratamiento(scope.row)">Detalles</el-dropdown-item>
                <el-dropdown-item @click="modificarTratamiento(scope.row)">Modificar</el-dropdown-item>
                <el-dropdown-item @click="eliminarTratamiento(scope.row)">Eliminar</el-dropdown-item>
                </el-dropdown-menu>
            </template>
            </el-dropdown>
        </template>
        </el-table-column>
    </el-table>
    <template #footer>
    <div class="dialog-footer">
        <el-button @click="exportToExcelTratamiento">📂 Exportar a Excel</el-button>
        <el-button @click="printListTratamiento">🖨️ Imprimir</el-button>
        <el-button @click="cancelar">Cancelar</el-button>
    </div>
    </template>
</el-dialog>

<el-dialog v-model="formRegTratamiento" title="Registrar Nuevo Tratamiento" width="500">
    <el-form :model="form" ref="formRef" :rules="reglas">
    <el-form-item label="Nombre" prop="nombre">
        <el-input v-model="form.nombre" />
    </el-form-item>
    </el-form>
    <template #footer>
    <div class="dialog-footer">
        <el-button @click="cancelarTratamiento">Cancelar</el-button>
        <el-button type="primary" @click="registrarTratamiento" round>
        Confirmar
        </el-button>
    </div>
    </template>
</el-dialog>

<el-dialog v-model="formModTratamiento" title="Modificar Tratamiento" width="500">
    <el-form :model="form" ref="formRef" :rules="reglas">
    <el-form-item label="Nombre" prop="nombre">
        <el-input v-model="tratamientoAct.nombre" />
    </el-form-item>
    </el-form>
    <template #footer>
    <div class="dialog-footer">
        <el-button @click="cancelarTratamiento">Cancelar</el-button>
        <el-button type="primary" @click="modificar_tratamiento" round>Confirmar</el-button>
    </div>
    </template>
</el-dialog>

<el-dialog v-model="formDetallesTratamiento" title="Detalles" width="600">
    <el-form :model="tratamientoAct" ref="formRef" :rules="reglas">
    <el-form-item label="Nombre" prop="Nombre">
        <el-input v-model="tratamientoAct.Nombre" disabled />
    </el-form-item>

    <el-form-item label="Insumos">
        <el-select v-model="materialSeleccionado" placeholder="Seleccione un material" style="width: 60%">
        <el-option
            v-for="mat in materialesDisponibles"
            :key="mat.ID_material"
            :label="mat.Nombre"
            :value="mat.ID_material"
        />
        </el-select>

        <el-input-number v-model="cantidad" :min="1" style="margin-left: 10px; width: 100px" />

        <el-button @click="agregarInsumo" type="primary" plain style="margin-left: 10px">
        Agregar
        </el-button>
    </el-form-item>

    <el-table :data="insumos" style="margin-top: 10px">
        <el-table-column prop="Nombre" label="Material" />
        <el-table-column prop="cantidad" label="Cantidad" />
        <el-table-column label="Acciones" width="100">
        <template #default="scope">
            <el-button
            type="danger"
            icon="el-icon-delete"
            size="small"
            @click="eliminarInsumo(scope.$index)"
            >Eliminar</el-button>
        </template>
        </el-table-column>
    </el-table>
    </el-form>

    <template #footer>
    <div class="dialog-footer">
        <el-button @click="formDetallesTratamiento = false">Cancelar</el-button>
        <el-button type="primary" @click="registrarInsumos" round>
        Confirmar
        </el-button>
    </div>
    </template>
</el-dialog>


<!-- Contenido para imprimir (oculto) -->
<div ref="printArea" style="display: none;">
<h2>Lista de Tipos de Tratamientos</h2>
<table border="1" cellspacing="0" cellpadding="5" style="width: 100%; text-align: left;">
<thead>
    <tr>
    <th>Nombre</th>
    <th>Cantidad de Tratamientos</th>
    </tr>
</thead>
<tbody>
    <tr v-for="p in tipofiltado" :key="p.id">
    <td>{{ p.nombre }}</td>
    <td>{{ p.cantidad }}</td>
    </tr>
</tbody>
</table>
</div>

<div ref="printAreaTipos" style="display: none;">
<h2>Lista de Tipos de Tratamientos</h2>
<table border="1" cellspacing="0" cellpadding="5" style="width: 100%; text-align: left;">
<thead>
    <tr>
    <th>Nombre</th>
    <th>Asociados</th>
    </tr>
</thead>
<tbody>
    <tr v-for="p in tipofiltado" :key="p.id">
    <td>{{ p.nombre }}</td>
    <td>{{ p.asociados }}</td>
    </tr>
</tbody>
</table>
</div>

<div ref="printAreaTratamiento" style="display: none;">
<h2>Lista de Tratamientos</h2>
<table border="1" cellspacing="0" cellpadding="5" style="width: 100%; text-align: left;">
<thead>
    <tr>
    <th>Nombre</th>
    </tr>
</thead>
<tbody>
    <tr v-for="p in tratamientoTipo" :key="p.id">
    <td>{{ p.Nombre }}</td>
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

const tipo = ref([])
const tipoAct = ref({})
const buscar = ref('')
const formRef = ref(null)
const formReg = ref(false)
const formRegTratamiento = ref(false)
const formMod = ref(false)
const formModTratamiento = ref(false)
const diagDetalles = ref(false)
const tratamientoTipo = ref([])
const tipoSeleccionada = ref(null)
const formDetallesTratamiento = ref(false)
const   tratamientoAct = ref({})
const materialesDisponibles = ref([])
const materialSeleccionado = ref(null)
const cantidad = ref(1)
const insumos = ref([])
const printArea = ref(null)
const printAreaTratamiento = ref(null)

const exportToExcel = () => {
    const worksheet = XLSX.utils.json_to_sheet(tratamientoTipo.value)
    const workbook = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(workbook, worksheet, "Tipos de Tratamientos")
    XLSX.writeFile(workbook, "Tipos de Tratamientos.xlsx")
}

const printList = async () => {
    await nextTick() // asegurarse que el DOM esté actualizado
    const content = printAreaTratamiento.value.innerHTML

    const printWindow = window.open('', '', 'height=600,width=800')
    printWindow.document.write('<html><head><title>Lista de Tipos de Tratamientos</title></head><body>')
    printWindow.document.write(content)
    printWindow.document.write('</body></html>')
    printWindow.document.close()
    printWindow.focus()
    printWindow.print()
    printWindow.close()
}

const exportToExcelTratamiento = () => {
    const dataToExport = tratamientoTipo.value.map(t => ({
        ID: t.ID_tratamiento,
        Nombre: t.Nombre,
    }))
    const worksheet = XLSX.utils.json_to_sheet(dataToExport)
    const workbook = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(workbook, worksheet, "Tratamientos")
    XLSX.writeFile(workbook, "Tratamientos.xlsx")
}

const printListTratamiento = async () => {
    await nextTick() // asegurarse que el DOM esté actualizado
    const content = printAreaTratamiento.value.innerHTML

    const printWindow = window.open('', '', 'height=600,width=800')
    printWindow.document.write('<html><head><title>Lista Tratamientos</title></head><body>')
    printWindow.document.write(content)
    printWindow.document.write('</body></html>')
    printWindow.document.close()
    printWindow.focus()
    printWindow.print()
    printWindow.close()
}

const tipofiltado = computed(() =>
    tipo.value.filter((data) =>
        !buscar.value ||
        Object.values(data).some((valor) =>
        String(valor).toLowerCase().includes(buscar.value.toLowerCase())
        )
    )
)

const form_ini = {
    nombre: ''
}

const reglas = {
    nombre: [{ required: true, message: 'El Nombre es obligatorio', trigger: 'blur' }]
}

const resetForm = () => {
    Object.assign(form, form_ini)
}

const form = reactive({ ...form_ini })

const registrar = async () => {
    formRef.value.validate(async (valid) => {
        if (valid) {
            try {
                const datos = {
                    nombre: form.nombre,
                }
                await axios.post('http://127.0.0.1:8000/api/Tipo/', datos)
                resetForm()
                formReg.value = false
                await cargar_tipos()
                ElMessage.success('Se agrego correctamente')
            } catch (error) {
            if (error.response && error.response.data) {
                console.error(error.response.data)
                ElMessage.error('Error: ' + JSON.stringify(error.response.data))
            } else {
                ElMessage.error('No se pudo agregar el Tipo de Tratamiento')
            }
            }
        }
    })
}

const registrarTratamiento = async () => {
    formRef.value.validate(async (valid) => {
        if (valid) {
            try {
                const datos = {
                    ID_tipo: tipoSeleccionada.value.ID_tipo,
                    Nombre: form.nombre,

                }
                console.log(datos)
                await axios.post('http://127.0.0.1:8000/api/Tratamiento/', datos)
                resetForm()
                formRegTratamiento.value = false
                ElMessage.success('Se agrego correctamente')
                await verTratamientoTipo(tipoSeleccionada.value)
                await cargar_tipos()
            } catch (error) {
            if (error.response && error.response.data) {
                console.error(error.response.data)
                ElMessage.error('Error: ' + JSON.stringify(error.response.data))
            } else {
                ElMessage.error('No se pudo agregar el Tratamiento')
            }
            }
        }
    })
}

const modificar = async (tipo) => {
    tipoAct.value = { ...tipo }

    form.nombre = tipoAct.value.nombre

    formMod.value = true
}

const modificarTratamiento = async (tratamiento) => {
    tratamientoAct.value = { ...tratamiento }

    form.nombre = tratamientoAct.value.nombre

    formModTratamiento.value = true
}

const detallesTratamiento = async (tratamiento) => {
    tratamientoAct.value = tratamiento
    materialSeleccionado.value = null
    cantidad.value = 1
    await obtenerInsumosPorTratamiento(tratamiento.ID_tratamiento)
    formDetallesTratamiento.value = true
}

const modificar_datos = async () => {
    formRef.value.validate(async (valid) => {
        if (valid) {
            try {
                const datos = {
                    nombre: tipo.value.nombre,
                }
                await axios.put(`http://127.0.0.1:8000/api/Tipo/${tipoAct.value.id}/`, datos)
                resetForm()
                formMod.value = false
                await cargar_tipos()
                ElMessage.success('Se modificó correctamente')
            } catch (error) {
            if (error.response && error.response.data) {
                console.error(error.response.data)
                ElMessage.error('Error: ' + JSON.stringify(error.response.data))
            } else {
                ElMessage.error('No se pudo modificar el Tipo de Tratamiento')
            }
            }
        }
    })
}

const modificar_tratamiento = async () => {
    formRef.value.validate(async (valid) => {
        if (valid) {
            try {
                const datos = {
                    tipo: tratamientoAct.value.tipo,
                    nombre: tratamientoAct.value.nombre,
                }
                await axios.put(`http://127.0.0.1:8000/api/Tratamiento/${tratamientoAct.value.id}/`, datos)
                resetForm()
                formModTratamiento.value = false
                await verTratamientoTipo(tipoSeleccionada.value)
                ElMessage.success('Se modificó correctamente')
            } catch (error) {
            if (error.response && error.response.data) {
                console.error(error.response.data)
                ElMessage.error('Error: ' + JSON.stringify(error.response.data))
            } else {
                ElMessage.error('No se pudo modificar el Tipo de Tratamiento')
            }
            }
        }
    })
}

const cancelar = () => {
    resetForm()
    formMod.value = false
    formReg.value = false
    diagDetalles.value = false
}

const cancelarTratamiento = () => {
    resetForm()
    formRegTratamiento.value = false
    formDetallesTratamiento.value = false
    formModTratamiento.value = false
}

const eliminar = async (row) => {
    try {
        const confirmacion = await ElMessageBox.confirm('¿Desea seguir con la eliminacion?', 'Eliminar Tipo de Tratamiento', {
            confirmButtonText: 'Aceptar',
            cancelButtonText: 'Cancelar',
            type: 'warning'
        })
        if (confirmacion) {
            await axios.delete(`http://127.0.0.1:8000/api/Tipo/${row.id}/`)
            await cargar_tipos()
            ElMessage.success('Tipo de tratamiento eliminado correctamente')
        }
    } catch (error) {
        console.error(error)
        ElMessage.error('Error al eliminar el Tipo de Tratamiento')
    }
}

const eliminarTratamiento = async (row) => {
    try {
        const confirmacion = await ElMessageBox.confirm('¿Desea seguir con la eliminacion?', 'Eliminar Tratamiento', {
            confirmButtonText: 'Aceptar',
            cancelButtonText: 'Cancelar',
            type: 'warning'
        })
        if (confirmacion) {
            await axios.delete(`http://127.0.0.1:8000/api/Tratamiento/${row.id}/`)
            await verTratamientoTipo(tipoSeleccionada.value)
            await cargar_tipos()
            ElMessage.success('Tratamiento eliminado correctamente')
        }
    } catch (error) {
        console.error(error)
        ElMessage.error('Error al eliminar el Tratamiento')
    }
}

const verTratamientoTipo = async (tipo) => {
    tipoSeleccionada.value = tipo

    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/Tipo/${tipo.ID_tipo}/tratamientos/`)
        tratamientoTipo.value = response.data
        diagDetalles.value = true
    } catch (error) {
        console.error('Error al obtener los Tratamientos:', error)
        ElMessage.error('No se pudieron cargar los Tratamientos')
    }
}

const cargar_tipos = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/Tipo/')
        tipo.value = response.data
    } catch (error) {
        console.error(error)
    }
}

function agregarInsumo() {
    const mat = materialesDisponibles.value.find(m => m.ID_material === materialSeleccionado.value);
    if (!mat) return;

    const yaExiste = insumos.value.some(i => i.ID_material === mat.ID_material);
    if (yaExiste) {
        ElMessage.warning('Este material ya fue agregado');
        return;
    }

    insumos.value.push({
        ID_material: mat.ID_material,
        Nombre: mat.Nombre,
        cantidad: cantidad.value,
        existente: false // Este es nuevo
    });
    materialSeleccionado.value = null;
    cantidad.value = 1;
}

async function eliminarInsumo(index) {
    const insumo = insumos.value[index]

    // Si el insumo ya fue guardado en el backend (tiene ID), lo eliminamos también desde el backend
    if (insumo.ID_insumo) {
        try {
        await axios.delete(`http://127.0.0.1:8000/api/Insumos/${insumo.ID_insumo}/`)
        ElMessage.success('Insumo eliminado del tratamiento')
        } catch (error) {
        console.error(error)
        ElMessage.error('No se pudo eliminar el insumo de la base de datos')
        return // no lo elimines localmente si falló el DELETE
        }
    }

    // Eliminación local
    insumos.value.splice(index, 1)
}

const registrarInsumos = async () => {
    formRef.value.validate(async (valid) => {
        if (!valid) return;
        try {
            for (const insumo of insumos.value) {
                if (insumo.existente) continue; // No agregues los ya existentes

                await axios.post('http://127.0.0.1:8000/api/Insumos/', {
                    ID_tratamiento: tratamientoAct.value.ID_tratamiento,
                    ID_material: insumo.ID_material,
                    Cantidad: insumo.cantidad,
                });
            }

            formDetallesTratamiento.value = false;
            await obtenerInsumosPorTratamiento(tratamientoAct.value.ID_tratamiento);
            ElMessage.success('Insumos procesados correctamente');

        } catch (error) {
            console.error(error);
            ElMessage.error('Error al registrar los insumos');
        }
    })
}

const cargarMateriales = async () => {
    try {
        const res = await axios.get('http://127.0.0.1:8000/api/Material/')
        materialesDisponibles.value = res.data
    } catch (err) {
        console.error('Error al obtener materiales', err)
        ElMessage.error('Error al obtener materiales')
    }
}

const obtenerInsumosPorTratamiento = async (tratamientoId) => {
    try {
        const res = await axios.get(`http://127.0.0.1:8000/api/Insumos/?tratamiento=${tratamientoId}`);
        insumos.value = res.data.map(i => ({
            ID_insumo:   i.ID_insumo,
            ID_material: i.ID_material,
            Nombre:      materialesDisponibles.value
                            .find(m => m.ID_material === i.ID_material)
                            ?.Nombre || '–',
            cantidad:    i.Cantidad,
            existente:   true
        }));
    } catch (err) {
        console.error('Error al obtener insumos:', err);
        ElMessage.error('No se pudieron obtener los insumos');
    }
}


onMounted(() => {
    cargar_tipos()
    cargarMateriales()
})

</script>
