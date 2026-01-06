<script setup lang="ts">
  import { ref } from 'vue'
  import axios from 'axios'

  const url = ref('')
  const titulo = ref('')
  const formato = ref('')
  const errorMsg = ref('')
 let resultado :any = ""

  const buscarCancion = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/information`,{
        params: {
          url: url.value
        }
      } )
      resultado = res.data
    }catch (error) {
      console.error(error)
      resultado.value = 'Error al buscar la canción'
    }
  }

  const descargarCancion = async () => {
    try{
      await axios.get(`http://localhost:8000/download`,{
        params: {
          url: url.value,
          formato: formato.value
        }
      })
     // alert("Descarga iniciada")
    }
    catch (error){
      console.error(error)
      alert("Error al iniciar la descarga")
    }
  }


</script>

<template>
  <h1>Bienvenido</h1>
  <h2>Comienza buscando algún video</h2>


  <input type="text" v-model="url" placeholder="URL del video" />
<button @click="buscarCancion">Buscar</button>

<p v-if="titulo">Cancion encontrada: {{ titulo }}</p>
<p v-if="errorMsg" style="color: red;">{{ errorMsg }}</p>



  <div>
    <label>Selecciona el formato</label>
    <select v-model="formato">
      <option value="mp4">MP4</option>
      <option value="mp3">MP3</option>
    </select>

    <button @click="descargarCancion">Descargar Canción</button>
  </div>


  <p>{{ resultado.title}}</p>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
