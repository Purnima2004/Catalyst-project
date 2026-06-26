import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
})

export const uploadResume = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  const { data } = await api.post('/api/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export const startAssessment = async (payload) => {
  const { data } = await api.post('/api/start', payload)
  return data
}

export const sendChat = async (payload) => {
  const { data } = await api.post('/api/chat', payload)
  return data
}

export default api
