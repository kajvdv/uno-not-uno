import { createApp } from 'vue'
import { createPinia } from 'pinia'

import '@/assets/styles.css'

import App from './App.vue'
import router from './router'
import { createApi } from './plugins/client.ts'
import api from '@/api'

const app = createApp(App)

app.use(createPinia())
app.use(createApi(api))
app.use(router)

app.mount('#app')
