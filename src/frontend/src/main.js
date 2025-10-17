import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// PrimeVue components
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import ProgressSpinner from 'primevue/progressspinner'
import Button from 'primevue/button'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Toast from 'primevue/toast'

// PrimeVue theme
// import 'primevue/resources/themes/lara-light-blue/theme.css'
// import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'

const app = createApp(App)

app.use(router)
app.use(PrimeVue)
app.use(ToastService)

// Register PrimeVue components
app.component('ProgressSpinner', ProgressSpinner)
app.component('Button', Button)
app.component('Card', Card)
app.component('InputText', InputText)
app.component('Textarea', Textarea)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('Toast', Toast)

app.mount('#app')