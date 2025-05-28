<script lang="ts" setup>
import type { TabsInstance } from 'element-plus';
import { ref } from 'vue';
import Materiales from './components/Materiales.vue';
import Obras_sociales from './components/Obras_sociales.vue';
import Pacientes from './components/Pacientes.vue';
import principal from './components/principal.vue';
import Tratamientos from './components/Tratamientos.vue';
import Turnos from './components/Turnos.vue';
import { Moon, Sunny } from '@element-plus/icons-vue'

const Home = ref('first'); // Estado para la pestaña activa
const tabPosition = ref<TabsInstance['tabPosition']>('left') // Posición de las pestañas
const modo = ref(false) // para modo nocturno

const activa = (Home: { name: string }) => {
  Home.value = Home.name
}

</script>

<template>

<div :class= "{'modo' : modo}">

<el-container>
      <el-header style="text-align: right; font-size: 12px">
        <div class="toolbar">
          <el-switch
            v-model="modo"
            :active-action-icon="Moon"
            :inactive-action-icon="Sunny"
          />
        </div>
    </el-header>
  </el-container>

  <div style="text-align: center;"><h1>Consultorio Odontológico del DR. ABCD</h1></div>

  <el-tabs v-model="Home" :tab-position="tabPosition" type="border-card" @tab-click="activa">
    <el-tab-pane label="Inicio" name="first">
      <principal v-if = "Home === 'first'" />
    </el-tab-pane>

    <el-tab-pane label="Pacientes" name="second">
      <Pacientes v-if="Home === 'second'" />
    </el-tab-pane>

    <el-tab-pane label="Turnos" name="third">
      <Turnos v-if="Home === 'third'" />
    </el-tab-pane>

    <el-tab-pane label="Obra Social" name="fourth">
      <Obras_sociales v-if="Home === 'fourth'" />
    </el-tab-pane>

    <el-tab-pane label="Tratamientos" name="fifth">
      <Tratamientos v-if="Home === 'fifth'" />
    </el-tab-pane>

    <el-tab-pane label="Materiales" name="sixth">
      <Materiales v-if="Home === 'sixth'" />
    </el-tab-pane>
  </el-tabs>

</div>
</template>

<style scoped>

::v-deep .modo {
  background: #222;
  color: #fff
}


</style>
