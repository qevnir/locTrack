    <template>

<div>
    <h1>LocTrack</h1>


    <div class="button" @click="toggleDateRange">
        <h3>

            <span v-if="showDateRange" class="arrow-icon">
                <font-awesome-icon icon="chevron-down" />
            </span>
            <span v-else class="arrow-icon">
                <font-awesome-icon icon="chevron-right" />
            </span>
            Date range
            <div style="float:right">

            </div>
        </h3>

    </div>
    <div v-if="showDateRange">



        <h3>Show dates</h3>
        <p>From:</p>
        <input type="date" v-model="fromDate">
        <p>To:</p>
        <input type="date" v-model="toDate">
        <button v-on:click="getDate">Go</button>
        <button v-on:click="prevDate">Previous</button>
        <button v-on:click="nextDate">Next</button>
    </div>







    <div class="button" @click="toggleLocations">
        <h3>
            <span v-if="showLocations" class="arrow-icon">
                <font-awesome-icon icon="chevron-down" />
            </span>
            <span v-else class="arrow-icon">
                <font-awesome-icon icon="chevron-right" />
            </span>
            Locations
            <div style="float:right">
               <!---- <new-location />----->

            </div>
        </h3>

    </div>
    <div v-if="showLocations">
        <table>
            <tr v-for="location in locations" :key="location.properties.pk">
                <td>
                    {{ location.properties.name }}
                </td>
                <td>
                    <input type="checkbox" :value=location.properties.pk v-model="checkedLocations">
                </td>
                <td>
                    <button v-on:click="editLocation">
                        <font-awesome-icon icon="edit" />
                    </button>

                </td>
            </tr>
        </table>

    </div>
    <div class="button" @click="toggleCategories">
        <h3>
            <span v-if="showCategories" class="arrow-icon">
                <font-awesome-icon icon="chevron-down" />
            </span>
            <span v-else class="arrow-icon">
                <font-awesome-icon icon="chevron-right" />
            </span>
            Categories
            <div style="float:right">

   
  
            </div>

        </h3>

    </div>
    <div v-if="showCategories">
        <div v-for="category in categories" :key="category.pk">
    <category-item v-bind:categoryID="category.pk" v-bind:categoryName="category.fields.name" />
      <button  @click="openModal('category')" >
                    <font-awesome-icon icon="plus" />
                </button>

        </div>
       <button  @click="openModal('category')" >
                    <font-awesome-icon icon="plus" />
                </button>
    </div>

    <div class="button" @click="toggleOptions">
        <h3>
            <span v-if="showOptions" class="arrow-icon">
                <font-awesome-icon icon="chevron-down" />
            </span>
            <span v-else class="arrow-icon">
                <font-awesome-icon icon="chevron-right" />
            </span>
            Options
            <div style="float:right">
            </div>
        </h3>
    </div>

    <div v-if="showOptions">
        <h3>Opacity</h3>
        <div>
            <input type="range" min="1" max="10" value="opacity" class="slider" id="opacityRange" ref="sliderValue"
                v-on:change="changeOpacity()">
        </div>

        <h3>File upload</h3>
        <input type="file" id="files" ref="files" accept=".gpx" multiple v-on:change="handleFileUpload()" />
        <br><button v-on:click="submitFiles">Submit</button>

</div>
        
    <button  @click="openModal('location')">
                    <font-awesome-icon icon="plus" />
                </button>
</div>
    </template>
        
    <script>
    import EventBus from '../event-bus';
    import axios from 'axios';
    import CategoryItem from './CategoryItem.vue'
   // import AddCategoryButton from './AddCategoryButton.vue'
  //  import NewLocation from './NewLocation.vue'


    export default {

        name: 'Options',
        components: {
            'category-item': CategoryItem,
     //    'add-category-button': AddCategoryButton,
     //       'new-location': NewLocation,
        },
        data: function() {
            
            return {
                fromDate: '',
                toDate: '',
                locations: [],
                checkedLocations: [],
                categoryID: null,
                categories: [],
                files: '',
                showCategories: false,
                showLocations: false,
                showOptions: false,
                showDateRange: true,
                opacity: 5,
            };
        },

        watch: {
            checkedLocations: function () {
                EventBus.$emit('checkedLocations', this.checkedLocations);
            },
            
        },
        mounted() {
            this.getAllLocations();
            this.getChildCategories(null);
        },
        methods: {
            changeOpacity: function () {
                this.opacity = this.$refs.sliderValue.value;
                EventBus.$emit('opacity', this.opacity / 10);
            },
            getDate: function () {
                EventBus.$emit('dates', [this.fromDate,this.toDate]);
            },
            openModal: function (modaltype) {
                if (modaltype === 'category') {
                    EventBus.$emit('categoryID', this.categoryID);
                }
                EventBus.$emit('openModal', modaltype);
            },
            getAllLocations: function () {
                
                axios.get( 'http://localhost:8000/mapVisual/all-locations/'
                        ).then(resp =>  {
                            this.locations = [];
                            let data = JSON.parse(resp.data);              
                            this.locations = data.features;
                            EventBus.$emit('locationData', this.locations);
                        }).catch(function() {
                            console.log('Failure!');
                        })
            },

            getChildCategories: function (id) {
            axios.get('http://localhost:8000/mapVisual/child-categories', {params: {  categoryID: id }}
                        ).then(resp => {
                            let data = JSON.parse(resp.data);
                            this.categories = data;                           
                        }).catch(function() {
                            console.log('Failure!');
                        });
        },
            
            editLocation: function () {
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

            nextDate: function () {
                let splitDate = this.fromDate.split('-');
    

                let tempDate = new Date(splitDate[0], splitDate[1], splitDate[2]);
                tempDate.setDate(tempDate.getDate() + 1);
                this.fromDate =  tempDate.getFullYear() + '-'
                    + ('0' + (tempDate.getMonth())).slice(-2) + '-'
                    + ('0' + tempDate.getDate()).slice(-2);

                tempDate.setDate(tempDate.getDate() + 1);
                this.toDate =  tempDate.getFullYear() + '-'
                    + ('0' + (tempDate.getMonth())).slice(-2) + '-'
                    + ('0' + tempDate.getDate()).slice(-2);
    
                this.getDate()
                
            },

            prevDate: function () {
                let splitDate = this.fromDate.split('-');
    

                let tempDate = new Date(splitDate[0], splitDate[1], splitDate[2]);
                tempDate.setDate(tempDate.getDate() - 1);
                this.fromDate =  tempDate.getFullYear() + '-'
                    + ('0' + (tempDate.getMonth())).slice(-2) + '-'
                    + ('0' + tempDate.getDate()).slice(-2);

                tempDate.setDate(tempDate.getDate() + 1);
                this.toDate =  tempDate.getFullYear() + '-'
                    + ('0' + (tempDate.getMonth())).slice(-2) + '-'
                    + ('0' + tempDate.getDate()).slice(-2);

                this.getDate()
                
            },


            toggleCategories() {
                this.showCategories = !this.showCategories;
                
            },
            toggleLocations() {
                this.showLocations = !this.showLocations;
                
            },
            toggleOptions() {
                this.showOptions = !this.showOptions;
                
            },
            toggleDateRange() {
                this.showDateRange = !this.showDateRange;
                
            }



            
        },
        
        created() {
            
            EventBus.$on('locationAdded', this.getAllLocations);
            EventBus.$on('categoryAdded', this.getChildCategories);
            
            
        },
    }

    </script>

    <style>
        .button {
        background-color: #4CAF50; /* Green */
        border: solid;
        width: 100%;
        border-width: 1px;
            border-color: lightgrey;

        color: white;
        text-align: left;
        
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        padding-left:10px;
                    padding: 10px;

        box-sizing:border-box;
        cursor: pointer;
        }

        .subbutton {
        background-color: darkgrey; /* Green */
            border: solid;
            border-width: 1px;
            border-color: lightgrey;
            border-left:none;
            border-right:none;
            width: 100%;
            color: white;
            text-align: left;
            
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            padding: 10px;
            padding-left:10px;

            box-sizing:border-box;
            cursor: pointer;
        }
        .arrow-icon {
            vertical-align: middle;
        margin-right: 8px;
        }
    
        .add-button {
            vertical-align: middle;
        margin-right: 8p;
        }
    </style>

