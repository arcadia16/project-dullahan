<template>
  <div class="audit-container">
    <h2>NTLM Audit Tool</h2>

    <div class="file-group">
      <label>NTDS.dit file:</label>
      <input type="file" @change="dit = $event.target.files?.[0] ?? null" />
    </div>

    <div class="file-group">
      <label>SYSTEM hive:</label>
      <input type="file" @change="sys = $event.target.files?.[0] ?? null" />
    </div>

    <button @click="upload" :disabled="!dit || !sys || isLoading" class="upload-btn">
      <span v-if="isLoading" class="spinner"></span>
      <span>{{ isLoading ? 'Uploading...' : 'Start Audit' }}</span>
    </button>

    <div v-if="jobId" class="job-status">
      <p>
        <strong>Job ID:</strong> {{ jobId }} – Status:
        <span :class="statusClass">{{ status }}</span>
      </p>

      <div v-if="status === 'done' && potfile" class="results">
        <h3>Cracked Hashes</h3>
        <pre class="potfile-output">{{ potfile }}</pre>
        <p><strong>Statistics:</strong> {{ crackedCount }} hash(es) cracked</p>
      </div>

      <button v-if="status === 'running'" @click="kill" class="kill-btn">Kill Job</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue'

const dit = ref<File | null>(null)
const sys = ref<File | null>(null)
const isLoading = ref(false)
const jobId = ref<string | null>(null)
const status = ref('')
const potfile = ref('')
let interval: number | null = null

const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

async function upload() {
  if (!dit.value || !sys.value) return

  isLoading.value = true
  const fd = new FormData()
  fd.append('dit_file', dit.value)
  fd.append('system_file', sys.value)

  try {
    const res = await fetch(`${API}/upload`, { method: 'POST', body: fd })
    if (!res.ok) throw new Error(`Upload failed: ${res.status}`)
    const data = (await res.json()) as { job_id: string }
    jobId.value = data.job_id
    startPolling()
  } catch (err) {
    console.error(err)
    status.value = 'failed'
  } finally {
    isLoading.value = false
  }
}

function startPolling() {
  if (interval) clearInterval(interval)
  interval = window.setInterval(async () => {
    if (!jobId.value) return
    try {
      const r = await fetch(`${API}/status/${jobId.value}`)
      if (!r.ok) throw new Error(`Status error: ${r.status}`)
      const d = (await r.json()) as { status: string; potfile_ready: boolean }
      status.value = d.status
      if (d.status === 'done' && d.potfile_ready) {
        clearInterval(interval!)
        await fetchPotfile()
      } else if (d.status === 'failed') {
        clearInterval(interval!)
      }
    } catch (err) {
      console.error(err)
      clearInterval(interval!)
    }
  }, 2000)
}

async function fetchPotfile() {
  if (!jobId.value) return
  const res = await fetch(`${API}/results/${jobId.value}`)
  const data = (await res.json()) as { potfile: string }
  potfile.value = data.potfile
}

async function kill() {
  if (!jobId.value) return
  await fetch(`${API}/kill/${jobId.value}`, { method: 'POST' })
  if (interval) clearInterval(interval)
}

const statusClass = computed(() => {
  switch (status.value) {
    case 'running':
      return 'status-running'
    case 'done':
      return 'status-done'
    case 'failed':
      return 'status-failed'
    default:
      return ''
  }
})

const crackedCount = computed(() => {
  if (!potfile.value) return 0
  return potfile.value
    .trim()
    .split('\n')
    .filter((l) => l.includes(':')).length
})

onUnmounted(() => {
  if (interval) clearInterval(interval)
})
</script>

<style scoped>
.audit-container {
  background: #000000;
  color: #ffffff;
  max-width: 900px;
  margin: 2rem auto;
  padding: 1.5rem;
  border-radius: 8px;
  font-family: system-ui, 'Segoe UI', sans-serif;
}

h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  font-weight: 500;
  border-bottom: 1px solid #333;
  padding-bottom: 0.5rem;
}

.file-group {
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}

label {
  font-weight: bold;
  min-width: 110px;
  color: #ffffff;
}

input[type='file'] {
  background: #1e1e1e;
  color: #ffffff;
  border: 1px solid #333;
  padding: 6px 8px;
  border-radius: 4px;
  flex: 1;
  font-size: 0.9rem;
}

input[type='file']::file-selector-button {
  background: #333;
  color: white;
  border: none;
  padding: 4px 12px;
  border-radius: 4px;
  margin-right: 8px;
  cursor: pointer;
}

.upload-btn {
  background: #ffc60e;
  color: #000000;
  border: none;
  padding: 8px 20px;
  border-radius: 4px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
  margin-top: 0.5rem;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.upload-btn:hover:not(:disabled) {
  background: #e5b200;
}

.upload-btn:disabled {
  background: #555;
  color: #999;
  cursor: not-allowed;
}

.kill-btn {
  background: #dc2626;
  color: white;
  margin-left: 0;
  margin-top: 1rem;
  border: none;
  padding: 6px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.kill-btn:hover {
  background: #b91c1c;
}

.job-status {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #333;
}

.results {
  margin-top: 1rem;
}

h3 {
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.potfile-output {
  background: #0a0a0a;
  color: #d4d4d4;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  border: 1px solid #2a2a2a;
  max-height: 400px;
  white-space: pre-wrap;
  word-break: break-all;
}

.status-running {
  color: #ffc60e;
  font-weight: bold;
}

.status-done {
  color: #4ade80;
  font-weight: bold;
}

.status-failed {
  color: #f87171;
  font-weight: bold;
}

/* Spinner animation */
.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(0, 0, 0, 0.3);
  border-radius: 50%;
  border-top-color: #000000;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 600px) {
  .audit-container {
    margin: 1rem;
    padding: 1rem;
  }
  .file-group {
    flex-direction: column;
    align-items: flex-start;
  }
  label {
    min-width: auto;
  }
  input[type='file'] {
    width: 100%;
  }
}
</style>
