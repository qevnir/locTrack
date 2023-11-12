<template>
  <span>
 <button v-if="!addingNewCategory" v-on:click="newCategory">Add</button>
    
    <div v-if="addingNewCategory">
    <br>
    <div>
      <form>
          <input type="text" id="categoryName" v-model="newCategoryName" placeholder="Name"/>
          <input type="color"  id="categoryColor" v-model="newCategoryColor"/> 
      <br>
      <button type="button" v-on:click="addCategory">Add</button>
    <button type="button" v-on:click="cancelNewCategory">Cancel</button> 
      </form>
    </div>
    </div>
</span>
</template>

<script>
  import axios from 'axios';

  export default {
      name: 'NewCategory',
      props: [
          'parentID'
      ],
      data: function () {
          return {
              addingNewCategory: false,
              newCategoryName: '',
              newCategoryColor: '#a46fe2',

          };
      },
      methods: {

        newCategory: function (){
            this.addingNewCategory = true;
        },

          addCategory: function () {
            axios.post( 'http://localhost:8000/mapVisual/new-category/',
                        JSON.stringify( {
                            name: this.newCategoryName,
                            color: this.newCategoryColor,
                            parent: this.parentID,
                        }),
                        {
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            }
                        }
                      ).then(function() {

                          console.log('Success!');
                      }).catch(function() {
                          console.log('Failure!');
                      });
        },
        cancelNewCategory: function () {
            this.addingNewCategory = false;
            
        },

  
          
      },
  }
</script>

<style>

</style>
