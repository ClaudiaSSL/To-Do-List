import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from "pinia";

import router from './router'
import 'bootstrap/dist/css/bootstrap.css'


const app = createApp(App)

app.use(router)
// create pinia instance
const pinia = createPinia();

// apply pinia to app
app.use(pinia);

app.mount('#app')
