<template>
  <div class="audit-form">
    <form @submit.prevent="submitForm">
      <div class="field">
        <label for="domain">Target domain</label>
        <InputText
          id="domain"
          v-model="formData.domain"
          placeholder="example.com"
          required
          class="w-full"
        />
      </div>

      <div class="field">
        <label for="username">Admin username</label>
        <InputText
          id="username"
          v-model="formData.username"
          placeholder="AdminUser"
          required
          class="w-full"
        />
      </div>

      <div class="field">
        <label for="password">Hash</label>
        <InputText
          id="hash"
          v-model="formData.password"
          placeholder="Admin hash"
          required
          class="w-full"
        />
      </div>

      <div class="field">
        <label for="wordlist">Choose wordlists</label>
        <InputText
          id="wordlist"
          v-model="formData.wordlist_path"
          placeholder="/path/to/wordlist.dict"
          required
          class="w-full"
        />
        <small class="text-sm text-gray-600">make drop list later</small>
      </div>

      <Button
        type="submit"
        label="Start the crack!"
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
    Button,
  },
  emits: ['audit-started'],
  setup(props, { emit }) {
    const toast = useToast()
    const loading = ref(false)

    const formData = ref({
      domain: '',
      username: '',
      hash: '',
      wordlist_path: '',
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
          hash: '',
          wordlist_path: '',
        }
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Audit Failed',
          detail: error.response?.data?.detail || 'Failed to start audit',
          life: 5000,
        })
      } finally {
        loading.value = false
      }
    }

    return {
      formData,
      loading,
      submitForm,
    }
  },
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
