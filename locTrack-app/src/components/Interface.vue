

<template>
  
<div id="interface">

        <div class=" cell-map">
          <map-container/>  
        

        </div>
        <div class=" cell-edit">
            <options/>

        </div>
        
    </div>
</template>



<script>
import  MapContainer  from './MapContainer.vue'
import Options from './Options.vue'

export default {
    name: 'Interface',
    components: {
        MapContainer,
        Options,
	
    },
    
    data: function() {
        return {
        };
    },
    
    methods: {

    },

 }
</script>

<style>

 #interface {
     font-family: Avenir, Helvetica, Arial, sans-serif;
     height: 100%;
     display: grid;
     grid-gap: 1rem;
    grid-template-columns: 75% 25% ;

     grid-auto-rows: 1fr;
     padding: 1rem;
     box-sizing: border-box;
     
 }


 .cell-map {

     grid-column: 1;
     border-radius: 2px;
     background-color: lightgrey
 }

 .cell-edit {
     grid-column: 2;
     border-radius: 2px;
     background-color: lightgrey;}

</style>
