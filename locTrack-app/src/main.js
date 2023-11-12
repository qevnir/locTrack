import Vue from 'vue'
import App from './App.vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faUserSecret,
         faPlus,
         faTrashAlt,
         faEdit,
         faChevronRight,
         faChevronDown
       } from '@fortawesome/free-solid-svg-icons'



library.add(faUserSecret,
            faPlus,
            faTrashAlt,
            faEdit,
            faChevronRight,
            faChevronDown
           );

Vue.component('font-awesome-icon', FontAwesomeIcon)


Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')



