<template>
  <div id="app">
      <interface/>
  </div>
</template>

<script>
import Interface from './components/Interface.vue'
import 'leaflet/dist/leaflet.css';

export default {
  name: 'App',
  components: {
    
     Interface,
  },
  }
</script>

<style>
  html, body {
      height: 100%;
      width: 100%;
     margin: 0;
  }

  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    height: 100%;
    display: grid-inline;
    grid-template-columns: auto ;
    grid-auto-rows: 1fr;
    padding: 1rem;
    box-sizing: border-box;
  }

  
</style>
