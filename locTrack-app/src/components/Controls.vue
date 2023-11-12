
<template>
    <div>
     <br><br>
        <div class="large-12 medium-12 small-12 ">
          <label>File upload
            <input type="file" id="files" ref="files" multiple v-on:change="handleFileUpload()"/>
          </label>
    <button v-on:click="submitFiles">Submit</button>
    
    </div>
    <br>
    <div >
    <button v-if="!newLocation" v-on:click="createNewLocation">New location</button>
    </div>
    <div v-if="newLocation">
    <br>
    <div>
    <form>
    <label>New location
    <input type="text" id="locationName" v-model="newLocationName" placeholder="Name"/>
    <select  v-model="newLocationCategoryID" id="cattList">
    <option v-for="category in categories" v-bind:key="category.pk" v-bind:value="category.pk">
    {{category.fields.name}}
         </option>
    </select>
  <!---  <input type="text" id="locationCategory" v-model="newLocationCategory" placeholder="Category"/> --->
    <input type="text" id="locationDuration" v-model="newLocationDuration" placeholder="Duration"/>
    <input type="color"  id="locationColor" v-model="newLocationColor" v-on:change="changeLocationColor"/>
    </label>
    <br>
    <button type="button" v-on:click="addNewLocation">Add</button>
        <button type="button" v-on:click="cancelNewLocation">Cancel</button>
    </form>
    </div>
    </div>
    </div>
</template>



<script>
import axios from 'axios';
import EventBus from '../event-bus';

export default {
    name: 'Controls',

    mounted() {
        
    },
    methods: {
        createNewLocation: function () {
            this.newLocation = true;
            EventBus.$emit('newLoc', this.newLocation);
            EventBus.$on('locationPolygon', data => {this.newLocationPolygon = data});
        },
        
        cancelNewLocation: function () {
            this.newLocation = false;
            EventBus.$emit('newLoc', this.newLocation);
            EventBus.$off('locationPolygon');
            this.clearNewLocationInputFields();

        },

        addNewLocation: function () {
            let context = this;
            axios.post( 'http://localhost:8000/mapVisual/add-new-location/',
                        JSON.stringify( {
                            name: this.newLocationName,
                            categoryID: this.newLocationCategoryID,
                            timeUntilVisited: this.newLocationDuration,
                            color: this.newLocationColor,
                            polygon: this.newLocationPolygon
                        }),
                        {
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            }
                        }
                      ).then(function() {
                          EventBus.$emit('locationAdded');
                          context.cancelNewLocation();
                          console.log('Success!');
                      }).catch(function() {
                          console.log('Failure!');
                      });

        },

        clearNewLocationInputFields: function () {
            this.newLocationName = ''
            this.newLocationCategory = ''
            this.newLocationDuration = ''
            this.newLocationColor = '#5186db'
        },

        changeLocationColor: function () {
            EventBus.$emit('newLocColor', this.newLocationColor);
                
        },

        handleFileUpload: function () {
            this.files = this.$refs.files.files;	    
        },
        submitFiles: function () {
            let formData = new FormData();
            for ( let i = 0; i < this.files.length; i++ ) {
                let file = this.files[i];
                formData.append(this.files[i].name, file);
            }

            axios.post( 'http://localhost:8000/mapVisual/import-data-gpx/',
                        formData,
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
/**
        getAllCategories: function () {
            console.log("getAllCategories");
            axios.get('http://localhost:8000/mapVisual/all-categories/'
                     ).then(resp => {
                         this.categories = [];
                         let data = JSON.parse(resp.data);
                         this.categories = data;
                         
                     }).catch(function() {
                         console.log('Failure!');
                     })
        },     
*/
    },
    data() {
      return {
          files: '',
          newLocation: false,
          newLocationColor: '#5186db',
          newLocationName: '',
          newLocationDuration: '',
          newLocationCategoryID: '',
          newLocationPolygon: '',
          categories: [],
      }
    }

}
</script>

<style>
  
</style>
