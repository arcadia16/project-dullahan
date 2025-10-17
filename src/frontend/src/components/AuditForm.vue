<template>
  <div class="audit-form">
    <form @submit.prevent="submitForm">
      <div class="field">
        <label for="domain">Domain</label>
        <InputText 
          id="domain"
          v-model="formData.domain" 
          placeholder="example.com" 
          required
          class="w-full"
        />
      </div>
      
      <div class="field">
        <label for="username">Username</label>
        <InputText 
          id="username"
          v-model="formData.username" 
          placeholder="AdminUser" 
          required
          class="w-full"
        />
      </div>
      
      <div class="field">
        <label for="password">Password</label>
        <InputText 
          id="password"
          v-model="formData.password" 
          type="password" 
          placeholder="Privileged account password" 
          required
          class="w-full"
        />
      </div>
      
      <div class="field">
        <label for="wordlist">Wordlist Path</label>
        <InputText 
          id="wordlist"
          v-model="formData.wordlist_path" 
          placeholder="/path/to/wordlist.dict" 
          required
          class="w-full"
        />
        <small class="text-sm text-gray-600">Path to wordlist file on the server</small>
      </div>
      
      <div class="field-checkbox">
        <label>
          <input type="checkbox" v-model="formData.agree_terms" required />
          I have authorization to audit this domain
        </label>
      </div>
      
      <Button 
        type="submit" 
        label="Start Security Audit" 
        icon="pi pi-shield"
        :loading="loading"
        class="w-full"
      />
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import api from '../services/api'

export default {
  name: 'AuditForm',
  components: {
    InputText,
    Button
  },
  emits: ['audit-started'],
  setup(props, { emit }) {
    const toast = useToast()
    const loading = ref(false)
    
    const formData = ref({
      domain: '',
      username: '',
      password: '',
      wordlist_path: '',
      agree_terms: false
    })

    const submitForm = async () => {
      loading.value = true
      
      try {
        const response = await api.startAudit(formData.value)
        emit('audit-started', response.job_id)
        
        // Reset form
        formData.value = {
          domain: '',
          username: '',
          password: '',
          wordlist_path: '',
          agree_terms: false
        }
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Audit Failed',
          detail: error.response?.data?.detail || 'Failed to start audit',
          life: 5000
        })
      } finally {
        loading.value = false
      }
    }

    return {
      formData,
      loading,
      submitForm
    }
  }
}
</script>

<style scoped>
.audit-form {
  padding: 1rem 0;
}

.field {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #374151;
}

.field-checkbox {
  margin: 2rem 0;
}

.field-checkbox label {
  display: flex;
  align-items: center;
  font-weight: normal;
}

.field-checkbox input {
  margin-right: 0.5rem;
}

.text-sm {
  font-size: 0.875rem;
}

.text-gray-600 {
  color: #6b7280;
}

.w-full {
  width: 100%;
}
</style>