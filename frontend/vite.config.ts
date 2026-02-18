import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    allowedHosts: [
      'https://frontend-loyiha-production.up.railway.app', 
      
    ]
    // Proxy-ni olib tashlasangiz ham bo'ladi yoki shunday turaversin
  }
})

