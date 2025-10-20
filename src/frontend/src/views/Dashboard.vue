<template>
  <div class="dashboard">
    <div class="grid">
      <Celty></Celty>
      <div class="col-12 md:col-6">
        <Card class="audit-form-card">
          <template #title>📊 Audit params</template>
          <template #content>
            <AuditForm @audit-started="handleAuditStarted" />
          </template>
        </Card>
      </div>
      <div class="col-12 md:col-6">
        <Card class="status-card">
          <template #title>📊 Audit status</template>
          <template #content>
            <JobStatus
              v-if="currentJobId"
              :jobId="currentJobId"
              @job-completed="handleJobCompleted"
            />
            <div v-else class="no-job">
              <p>No active jobs.</p>
            </div>
          </template>
        </Card>

        <Card v-if="results" class="results-card">
          <template #title>✅ Audit Results</template>
          <template #content>
            <ResultsDisplay :results="results" />
          </template>
        </Card>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import Card from 'primevue/card'
import AuditForm from '../components/AuditForm.vue'
import JobStatus from '../components/JobStatus.vue'
import ResultsDisplay from '../components/ResultsDisplay.vue'
import Celty from '@/components/Celty.vue'

export default {
  name: 'Dashboard',
  components: {
    Card,
    AuditForm,
    JobStatus,
    ResultsDisplay,
    Celty,
  },
  setup() {
    const toast = useToast()
    const currentJobId = ref(null)
    const results = ref(null)

    const handleAuditStarted = (jobId) => {
      currentJobId.value = jobId
      results.value = null
      toast.add({
        severity: 'success',
        summary: 'Audit Started',
        detail: `Job ID: ${jobId}`,
        life: 3000,
      })
    }

    const handleJobCompleted = (jobResults) => {
      results.value = jobResults
      toast.add({
        severity: 'info',
        summary: 'Audit Completed',
        detail: `Found ${jobResults.cracked_count} cracked passwords`,
        life: 5000,
      })
    }

    return {
      currentJobId,
      results,
      handleAuditStarted,
      handleJobCompleted,
    }
  },
}
</script>

<style scoped>
.dashboard {
  padding: 1rem 0;
}

.grid {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -1rem;
}

.col-12 {
  padding: 1rem;
  flex: 0 0 100%;
}

@media (min-width: 768px) {
  .md\:col-6 {
    flex: 0 0 50%;
  }
}

.audit-form-card,
.status-card,
.results-card {
  height: 100%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.no-job {
  text-align: center;
  padding: 2rem;
  color: #6c757d;
}
</style>
