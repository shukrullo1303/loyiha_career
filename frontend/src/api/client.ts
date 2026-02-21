/// <reference types="vite/client" />

import axios from 'axios'
import { useAuthStore } from '../store/authStore'


const API_URL = import.meta.env.VITE_API_URL


const apiClient = axios.create({
  baseURL: API_URL.endsWith('/') ? API_URL : `${API_URL}/`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Location endpoints:
// GET /locations/ - barcha locationlar
// POST /locations/ - location qo'shish
// PUT /locations/{id}/ - location tahrirlash
// DELETE /locations/{id}/ - location o'chirish
// GET /locations/{id}/cameras/ - locationga biriktirilgan kameralar
// POST /locations/{id}/cameras/ - locationga kamera biriktirish
// DELETE /locations/{id}/cameras/{camera_id}/ - locationdan kamerani ajratish

// Camera endpoints:
// GET /cameras/ - barcha kameralar
// POST /cameras/ - kamera qo'shish
// PUT /cameras/{id}/ - kamera tahrirlash
// DELETE /cameras/{id}/ - kamera o'chirish

export default apiClient
