<template>
  <span>

    
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
      name: 'AddCategoryButton',
      props: [
          'categoryID'
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
              let context = this;

            axios.post( 'http://localhost:8000/mapVisual/new-category/',
                        JSON.stringify( {
                            name: this.newCategoryName,
                            color: this.newCategoryColor,
                            parent: this.categoryID,
                        }),
                        {
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            }
                        }
                      ).then(function() {
                          context.$emit('categoryAdded');

                          console.log('Success!');
                      }).catch(function() {

                          console.log('Failure!1');
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
