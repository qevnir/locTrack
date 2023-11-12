<template>
  

<div id="map" style="height: 100%; width: 100%">         <modal ref="modalName"/></div>

</template>

<script>
import L from 'leaflet';
import EventBus from '../event-bus';
import Modal from "./Modal.vue";

export default {
    name: "MapContainer",
    components: {
        Modal,

    },
    
    data() {
        
        return {
            
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            zoom: 9,
            center: [55.18, 12.0],
            geojsonLayer: null,
            mymap: null,
            latlngs: [],
            locationPolygon: null,
            locationPolygonColor: '#5186db',
            locationsLayer: null,
            locationData: null,
            opacity: this.opacityProp,
        }
    },
    

    
    methods: {
        openModal: function(modalType ) {
            console.log(modalType);
            this.$refs.modalName.openModal(modalType);
        },

        newLocation: function(newLocation) {
            
            if (newLocation) {
                this.mymap.on('click', this.addClickedLocation);
                this.locationPolygon.remove(this.mymap);

            } else {
                this.mymap.off('click');
                this.latlngs = [];
                this.locationPolygon.remove(this.mymap);

            }
        },

        changeOpacity: function(newOpacity) {
            this.opacity = newOpacity;
            this.geojsonLayer.eachLayer(function (layer) {
                layer.setStyle({opacity : newOpacity })
            });
        },
        
        changePolygonColor: function (color) {
            
            this.locationPolygonColor = color
            this.locationPolygon.setStyle({color:this.locationPolygonColor});
        },

        addClickedLocation: function (ev) {
            
            let lat = ev.latlng.lat;
            let lng = ev.latlng.lng;
            this.latlngs.push([lat,lng]);
            
            this.locationPolygon.remove(this.mymap);
            this.locationPolygon = L.polygon(this.latlngs, {color: this.locationPolygonColor,
                                                            stroke:true})
            this.locationPolygon.addTo(this.mymap)
            
            let locationPolygonJson = this.locationPolygon.toGeoJSON();

            // toGeoJson swaps coordiantes, so they are swapped back
            let locationCoords = locationPolygonJson.geometry.coordinates[0];
            let locationCoordsSwapped = (locationCoords.map(function (latlng) {
                return [latlng[1],latlng[0]];
            }));
            locationPolygonJson.geometry.coordinates[0] = locationCoordsSwapped;

            EventBus.$emit('locationPolygon',locationPolygonJson);
        },
         
        showCheckedLocations: function (locationsToShow) {

            // create new polygon layers
            let polygonLayers =  (this.locationData.map(function (location) {

                if (locationsToShow.includes(location.properties.pk) ) {
                    
                    let polygonToShow = L.polygon(location.geometry.coordinates[0],
                                            {color: location.properties.color, stroke:true});
                    return polygonToShow;
                }
            }));

            // remove old polygon layers
            let context = this.locationsLayer;
            this.locationsLayer.eachLayer(function(layer) {
                context.removeLayer(layer);
            });

            // add new polygon layers
            for(let layer of polygonLayers) {
                if (layer != null){
                    this.locationsLayer.addLayer(layer);
                }
            }
        },

        setLocationData: function (data) {
            
            this.locationData = data;
        },
        
        getData: async (date1, date2) => {
            
            let url = new URL('http://localhost:8000/mapVisual/trackpoints');
            url.search = new URLSearchParams( {start: date1, end: date2 });
            let response = await fetch(url);
            let data = await response.json();
            return data;
        },
        
        plotDates: function (dates) {
            
            this.geojsonLayer.clearLayers();
            const daysDiff = this.calcDaysDiff(dates[0],dates[1]);
            

            let date =  new Date(dates[0]);
            let options = {
                radius: 1,
                color: 'purple',
                opacity: this.opacity,
            };
            for (let i = 0; i < daysDiff; i++) {
                let formattedDate1 = date.toISOString()
                let date2 = new Date(date.setDate(date.getDate() + 1));
                let formattedDate2 = date2.toISOString();

                
                (async () => {
                    let data = await this.getData(formattedDate1, formattedDate2)
                        .then(res => res)
                        .catch(err => {console.log(err)});


                    let pointLayer = L.geoJSON(JSON.parse(data), {
                        
                        pointToLayer: function(feature,latlng){
                            let circle = new L.circleMarker(latlng,options);
                            return circle;
                        }
                    });
                    this.geojsonLayer.addLayer(pointLayer);        
                })();
            }
        },

        // Calculate number of days between two dates
        calcDaysDiff: function (date1, date2) {
            
            const _MS_PER_DAY = 1000 * 60 * 60 * 24;
            const a = new Date(date1);
            const b = new Date(date2);
            const utc1 = Date.UTC(a.getFullYear(), a.getMonth(), a.getDate());
            const utc2 = Date.UTC(b.getFullYear(), b.getMonth(), b.getDate());
            const daysDiff =  (date2 != "") ? Math.floor((utc2 - utc1) / _MS_PER_DAY) : 1;
            return daysDiff;
        },
    },

    created() {
        
        EventBus.$on('newLoc', this.newLocation);
        EventBus.$on('newLocColor', this.changePolygonColor);
        EventBus.$on('dates', this.plotDates);
        EventBus.$on('opacity', this.changeOpacity);
        EventBus.$on('checkedLocations', this.showCheckedLocations);
        EventBus.$on('locationData', this.setLocationData);
	EventBus.$on('openModal', this.openModal);
    },
    
    mounted() {
        
        this.mymap =  L.map('map', {
            preferCanvas: true,
            updateWhenZooming: false,
            updateWhenIdle: true,
        }).setView(this.center, this.zoom);
        L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            opacity: 1,

        }).addTo(this.mymap);
        this.geojsonLayer = L.geoJSON("").addTo(this.mymap);
        this.locationPolygon = L.polygon(this.latlngs, {fillColor: this.locationPolygonColor,
                                                        weight:0.1}).addTo(this.mymap);
        this.locationsLayer = new L.FeatureGroup().addTo(this.mymap);
    },
}
</script>
