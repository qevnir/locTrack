<template>
    
    <span>

        <div class="modal-overlay">
            <div class="modal">
                
                <br>
                <div>
                    <form>
                        <input type="text" id="categoryName" v-model="newCategoryName" placeholder="Name"/>
                        <input type="color"  id="categoryColor" v-model="newCategoryColor"/> 
                        <br>
                        <button type="button" v-on:click="addCategory">Add</button>
                        <button @click="closeModal()">Cancel</button>

                    </form>
                </div>
            </div>
            <div class="close">
            </div>
        </div>


    </span>
</template>

<script>
 import axios from 'axios';
 import EventBus from '../event-bus';
 
 export default {
     name: 'AddCategoryModal',

     data: function () {
         return {
             addingNewCategory: false,
             newCategoryName: '',
             newCategoryColor: '#a46fe2',
             categoryID: null,


         };
     },
     methods: {

          closeModal: function () {
              this.$emit('close');
          },

          newCategory: function () {
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
      created() {
          
          EventBus.$on('categoryID',  (catID) => {
              console.log('event received!', catID);
              this.categoryID = catID;
          });
      },
  }
</script>

<style>

 .modal-overlay {
     position: fixed;
     z-index:10000; 
     top: 0;
     bottom: 0;
     left: 0;
     right: 0;
     display: flex;
     justify-content: center;
     background-color: #000000da;
 }

 .modal {
     text-align: center;
     background-color: white;
     height: 500px;
     width: 500px;
     margin-top: 10%;
     padding: 60px 0;
     border-radius: 20px;
 }
 .close {
     margin: 10% 0 0 16px;
     cursor: pointer;
 }

 .close-img {
     width: 25px;
 }

 .check {
     width: 150px;
 }

 h6 {
     font-weight: 500;
     font-size: 28px;
     margin: 20px 0;
 }

 p {
     font-size: 16px;
     margin: 20px 0;
 }

 button {
     background-color: #4CAF50; /* Green */
     width: 150px;
     height: 40px;
     color: white;
     font-size: 14px;
     border-radius: 5px;
     border: solid;
     border-color: lightgrey;

     margin-top: 50px;
 }
</style>
