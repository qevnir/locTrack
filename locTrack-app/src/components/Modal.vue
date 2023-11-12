<template>
<div class="modal" v-if="show">
  <div class="modal-overlay">
    <div class="modal">
        <div v-if="modalType == 'category'">
          <add-category-modal @close="closeModal"/>
        </div>
        <div v-else-if="modalType == 'location'">
          <add-location-modal @close="closeModal"/>
        </div>
 
    </div>
  </div>
  <div class="close">
  </div>
</div>
</template>

<script>

import AddCategoryModal from './AddCategoryModal.vue'
import AddLocationModal from './AddLocationModal.vue'

export default {
    name: "Modal",
    components: {
        'add-category-modal': AddCategoryModal,
        'add-location-modal': AddLocationModal,
        },
  data() {
      return {
      modalType: '',
          show: false,
    };
  },
  methods: {
    closeModal() {
        this.show = false;
        this.modalType = '';
      document.querySelector("body").classList.remove("overflow-hidden");
    },
      openModal(modalType) {
          console.log("open: ", modalType);
      this.modalType = modalType;
      this.show = true;
      document.querySelector("body").classList.add("overflow-hidden");
    }
  }
};
</script>


<style scoped>

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


