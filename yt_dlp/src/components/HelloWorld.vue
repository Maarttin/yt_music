<script setup lang="ts">
  import { ref } from 'vue'
  import axios from 'axios'

  const url = ref('')
  const formato = ref('mp3')
  const errorMsg = ref('')
  const resultado = ref<any>(null)  
 


  const buscarCancion = async () => {
    try {
      const res = await axios.get(`https://ytmusic-production.up.railway.app/information`,{
        params: {
          url: url.value
        }
      } )
      resultado.value = res.data
    }catch (error) {
      console.error(error)
      resultado.value = 'Error al buscar la canción'
    }
  }

  const descargarCancion = async () => {
    try{
      const response =await axios.get(`https://ytmusic-production.up.railway.app/download`,{
        params: {
          url: url.value,
          formato: formato.value
        }
      })
      const blob = new Blob([response.data], { type: "audio/mpeg" }); const link = document.createElement("a"); link.href = URL.createObjectURL(blob); link.download = "musica.mp3"; // nombre sugerido document.body.appendChild(link); link.click(); document.body.removeChild(link);
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
  <h2>Comienza buscando algún video por nombre o URL</h2>


  <input type="text" v-model="url" placeholder="URL del video" />
<button @click="buscarCancion">Buscar</button>

<p v-if="resultado">Cancion encontrada: {{ resultado['title'] }}</p>
<p v-if="errorMsg" style="color: red;">{{ errorMsg }}</p>



  <div>
    <label>Selecciona el formato</label>
    <select v-model="formato">
      <option value="mp4">MP4</option>
      <option value="mp3">MP3</option>
    </select>

    <button @click="descargarCancion">Descargar Canción</button>
  </div>


 
</template>




<style scoped>
.read-the-docs {
  color: #888;
}
</style>
