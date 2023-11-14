<template>
    <span>
        <div>
            <span class="subbutton" @click="toggleChildren">
                <div class="itemTextArrow" >
                <span  v-if="showChildren" class="arrow-icon"> <font-awesome-icon icon="chevron-down" /></span>
                <span  v-else class="arrow-icon"> <font-awesome-icon icon="chevron-right" /></span>
                {{ categoryName  }}
                
                <div class="editButton" v-on:click="editCategory">

                    <font-awesome-icon icon="edit" />
                </div>
                </div>

            </span>
            

        </div>
        <div v-if="showChildren">
            <!--   <div style="float:right">
                 <remove-category-button  @categoryRemoved="getChildCategories(categoryID)"  v-bind:categoryID="categoryID"/>
                 </div> -->

  
            
            <div style="text-align: center">
                <button  @click="openModal('category')" >
                    <font-awesome-icon icon="plus" /> New Subcategory
                </button>    
            </div>
            <div v-for="category in categories" :key="category.pk" >
                <category-item v-bind:categoryID="category.pk"  v-bind:categoryName="category.fields.name"/>

            </div>

        </div>

    </span>
</template>

<script>

 import axios from 'axios';
 //import RemoveCategoryButton from './RemoveCategoryButton.vue'
 import EventBus from '../event-bus';

 export default {
     name: 'CategoryItem',
     components: {
         // 'remove-category-button': RemoveCategoryButton,

     },
     props: [
         'categoryID', 'categoryName' 
     ],
     data: function () {
         return {
             categories : [],
             showChildren: false,
         };
     },

     mounted() {
         this.getChildCategories(this.categoryID);
     },

     
     methods: {

         getChildCategories: function (id) {
             console.log("getchilds");
             this.categories = [];
             axios.get('http://localhost:8000/mapVisual/child-categories', {params: {  categoryID: id }}
             ).then(resp => {
                 let data = JSON.parse(resp.data);
                 this.categories = data;                           
             }).catch(function() {
                 console.log('Failure!');
             });
         },
         
         toggleChildren() {
             this.showChildren = !this.showChildren;
         },

         openModal: function (modaltype) {
             if (modaltype === 'category') {
                 console.log("item: ", this.categoryID);
                 EventBus.$emit('categoryID', this.categoryID);
             }
             EventBus.$emit('openModal', modaltype);
         },
         editCategory: function () {
             event.stopPropagation();
         },
         
     },
 }
</script>

<style>



 .subbutton {
     display: flex;
     align-items: center; 
 }

 .itemTextArrow {
     display: flex;
     align-items: center; 
 }




</style>
