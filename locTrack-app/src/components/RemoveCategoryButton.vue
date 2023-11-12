<template>
  <span>
 <button  v-on:click="removeCategory">  <font-awesome-icon icon="trash-alt" /></button>
    
  
</span>
</template>

<script>
  import axios from 'axios';

  export default {
      name: 'RemoveCategoryButton',
      props: [
          'categoryID'
      ],
      data: function () {
          return {
          };
      },
      methods: {
          removeCategory: function () {
              
              let context = this;
              axios.post( 'http://localhost:8000/mapVisual/remove-category/',
                          JSON.stringify( {
                              categoryID: this.categoryID,
                          }),
                          {
                              headers: {
                                  'Content-Type': 'multipart/form-data'
                              }
                          }
                        ).then(function() {
                            context.$emit('categoryRemoved');
                            console.log('Success!');
                        }).catch(function() {
                            console.log('Failure!');
                        });
          },
      },
  }
</script>

<style>

</style>
