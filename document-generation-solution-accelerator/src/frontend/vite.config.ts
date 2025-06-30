import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../static',
    emptyOutDir: true,
    sourcemap: true
  },
  server: {
    proxy: {
      '/ask': 'http://localhost:50505',
      '/chat': 'http://localhost:50505',
      '/conversation': 'http://localhost:50505',
      '/history': 'http://localhost:50505',
      '/section': 'http://localhost:50505',
      '/document': 'http://localhost:50505',
      '/frontend_settings': 'http://localhost:50505',
      '/health': 'http://localhost:50505',
      '/debug': 'http://localhost:50505'
    }
  }
})
