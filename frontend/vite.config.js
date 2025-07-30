import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import svgr from "vite-plugin-svgr";


// https://vite.dev/config/
export default defineConfig({
  server: {
    proxy: {
      '^/api/.*/connect': {
        target: "ws://127.0.0.1:8000",
        rewriteWsOrigin: true,
        changeOrigin: true,
        ws: true,
        rewrite: path => path.replace(/^\/api/, '')
      },
      '/api': {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
    }
  },
  preview: {
    proxy: {
      '^/api/.*/connect': {
        target: "ws://127.0.0.1:8000",
        rewriteWsOrigin: true,
        changeOrigin: true,
        ws: true,
        rewrite: path => path.replace(/^\/api/, '')
      },
      '/api': {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
    }
  },
  plugins: [svgr(), react()],
})
