import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    allowedHosts: [
      'frontend-loyiha-production.up.railway.app'
    ],
    proxy: {
      '/api': {
        target: 'https://loyihacareer-production-d107.up.railway.app',
        changeOrigin: true

      }
    }
  }
})
