<template>
  <div class="job-status">
    <div class="status-header">
      <h3>Job: {{ jobId }}</h3>
      <Button
        icon="pi pi-refresh"
        @click="checkStatus"
        :loading="loading"
        class="p-button-rounded p-button-outlined"
      />
    </div>

    <div class="status-content">
      <div v-if="statusData" class="status-info">
        <div class="status-badge" :class="statusClass">
          {{ statusData.status.toUpperCase() }}
        </div>

        <p class="status-message">{{ statusData.message }}</p>

        <ProgressSpinner v-if="statusData.status === 'running'" style="width: 50px; height: 50px" />

        <div v-if="statusData.results" class="results-preview">
          <p><strong>Cracked Passwords:</strong> {{ statusData.results.cracked_count }}</p>
          <p><strong>Output File:</strong> {{ statusData.results.output_file }}</p>
        </div>
      </div>

      <div v-else class="loading-status">
        <ProgressSpinner />
        <p>Loading status...</p>
      </div>
    </div>

    <div class="status-actions">
      <Button
        label="Check Status"
        @click="checkStatus"
        :loading="loading"
        class="p-button-outlined"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import ProgressSpinner from 'primevue/progressspinner'
import api from '../services/api'

export default {
  name: 'JobStatus',
  components: {
    Button,
    ProgressSpinner,
  },
  props: {
    jobId: {
      type: String,
      required: true,
    },
  },
  emits: ['job-completed'],
  setup(props, { emit }) {
    const toast = useToast()
    const loading = ref(false)
    const statusData = ref(null)
    let pollInterval = null

    const checkStatus = async () => {
      loading.value = true
      try {
        statusData.value = await api.getAuditStatus(props.jobId)

        // Emit event if job is completed
        if (statusData.value.status === 'completed' && statusData.value.results) {
          emit('job-completed', statusData.value.results)
          stopPolling()
        }
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Status Check Failed',
          detail: error.response?.data?.detail || 'Failed to check status',
          life: 3000,
        })
      } finally {
        loading.value = false
      }
    }

    const startPolling = () => {
      pollInterval = setInterval(checkStatus, 5000) // Poll every 5 seconds
    }

    const stopPolling = () => {
      if (pollInterval) {
        clearInterval(pollInterval)
        pollInterval = null
      }
    }

    onMounted(() => {
      checkStatus()
      startPolling()
    })

    onUnmounted(() => {
      stopPolling()
    })

    const statusClass = computed(() => {
      if (!statusData.value) return ''
      switch (statusData.value.status) {
        case 'running':
          return 'status-running'
        case 'completed':
          return 'status-completed'
        case 'error':
          return 'status-error'
        default:
          return ''
      }
    })

    return {
      loading,
      statusData,
      checkStatus,
      statusClass,
    }
  },
}
</script>

<style scoped>
.job-status {
  padding: 1rem 0;
}

.status-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.status-header h3 {
  margin: 0;
  color: #374151;
  font-size: 1.1rem;
}

.status-content {
  text-align: center;
  padding: 1rem 0;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.status-running {
  background-color: #dbeafe;
  color: #1e40af;
}

.status-completed {
  background-color: #d1fae5;
  color: #065f46;
}

.status-error {
  background-color: #fee2e2;
  color: #dc2626;
}

.status-message {
  margin: 1rem 0;
  color: #6b7280;
}

.results-preview {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f9fafb;
  border-radius: 6px;
  text-align: left;
}

.loading-status {
  padding: 2rem;
}

.status-actions {
  margin-top: 1rem;
  text-align: center;
}
</style>
