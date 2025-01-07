import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://fastapi_backend:8000', // FastAPI'nin adresini burada belirtin
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''), // /api'yi kaldırır
      },
    },
  },
})

