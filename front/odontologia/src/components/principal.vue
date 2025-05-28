<template>
  <el-table :data="resumen" style="width: 100%">
    <el-table-column label="Pacientes" prop="pacientes" />
    <el-table-column label="Obra Social" prop="obras_sociales" />
    <el-table-column label="Tratamientos" prop="tratamientos" />
  </el-table>


  <el-divider />

  <h2><center>Bajo Stock</center></h2>

  <el-table :data="materialBajo" :row-class-name="rowClassName" style="width: 100%">
    <el-table-column label="Nombre" prop="Nombre" />
    <el-table-column label="Cantidad" prop="cantidad" />
    <el-table-column label="Minimo" prop="min" />
  </el-table>

</template>

<script lang="ts" setup>
import axios from 'axios';
import { computed, onMounted, ref } from 'vue';

const resumen = ref([])
const material = ref([])

const cargar_resumen = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/Resumen/')
    resumen.value = [response.data] // Lo metemos en un array para que el <el-table> lo renderice
  } catch (error) {
    console.error('Error al cargar el resumen:', error)
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

const materialBajo = computed(() => {
  return material.value.filter(m => m.cantidad < m.min*1.25)
})

const rowClassName = ({ row }: { row: any }) => {
    if (row.cantidad < row.min) {
        return 'low-stock';
    } else if (row.cantidad < row.min * 1.25) {
        return 'medium-stock';
    }
    return '';
}

onMounted(() => {
  cargar_resumen()
  cargar_material()
})
</script>

<style scoped>
/* fila entera en rojo muy suave */
::v-deep .low-stock td {
    background-color: #ffecec;
    color: #d93025;
}

::v-deep .medium-stock td {
    background-color: #ffffc8;
    color: #d8d51e;
}

</style>
