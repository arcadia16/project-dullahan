import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

export default {
  // Start a new audit job
  async startAudit(auditData) {
    console.log(auditData)
    const response = await apiClient.post('/start/', auditData)
    return response.data
  },

  // Check audit job status
  async getAuditStatus(jobId) {
    const response = await apiClient.get('/status/${jobId}')
    return response.data
  },

  // Get cracked passwords (if any)
  async getCrackedPasswords(outputFile) {
    // This would need a new endpoint in your FastAPI to serve the results
    const response = await apiClient.get('/api/v1/audit/results/${outputFile}')
    return response.data
  }
}