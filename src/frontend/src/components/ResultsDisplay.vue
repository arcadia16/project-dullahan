<template>
  <div class="results-display">
    <div class="results-summary">
      <h4>Audit Summary</h4>
      <div class="summary-grid">
        <div class="summary-item">
          <span class="label">Cracked Passwords:</span>
          <span class="value">{{ results.cracked_count }}</span>
        </div>
        <div class="summary-item">
          <span class="label">Output File:</span>
          <span class="value file-path">{{ results.output_file }}</span>
        </div>
      </div>
    </div>

    <div v-if="crackedPasswords.length > 0" class="cracked-passwords">
      <h4>Cracked Passwords</h4>
      <DataTable :value="crackedPasswords" class="p-datatable-sm">
        <Column field="username" header="Username"></Column>
        <Column field="password" header="Password"></Column>
        <Column field="hash" header="NTLM Hash"></Column>
      </DataTable>
    </div>

    <div v-else class="no-results">
      <p>No passwords were cracked with the current wordlist.</p>
      <Button label="Try Different Wordlist" icon="pi pi-refresh" class="p-button-outlined" />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import api from '../services/api'

export default {
  name: 'ResultsDisplay',
  components: {
    DataTable,
    Column,
    Button,
  },
  props: {
    results: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const crackedPasswords = ref([])

    onMounted(async () => {
      // Load cracked passwords if output file exists
      if (props.results.output_file && props.results.cracked_count > 0) {
        try {
          crackedPasswords.value = await api.getCrackedPasswords(props.results.output_file)
        } catch (error) {
          console.error('Failed to load cracked passwords:', error)
        }
      }
    })

    return {
      crackedPasswords,
    }
  },
}
</script>

<style scoped>
.results-display {
  padding: 1rem 0;
}

.results-summary {
  margin-bottom: 1.5rem;
}

.results-summary h4 {
  margin-bottom: 1rem;
  color: #374151;
}

.summary-grid {
  display: grid;
  gap: 1rem;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem;
  background-color: #f8f9fa;
  border-radius: 6px;
}

.label {
  font-weight: 600;
  color: #495057;
}

.value {
  color: #6c757d;
}

.file-path {
  font-family: monospace;
  font-size: 0.875rem;
}

.cracked-passwords {
  margin-top: 1.5rem;
}

.no-results {
  text-align: center;
  padding: 2rem;
  color: #6c757d;
}

:deep(.p-datatable) {
  font-size: 0.875rem;
}
</style>
