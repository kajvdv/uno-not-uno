import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import svgr from "vite-plugin-svgr";


const getProxy = (backendUrl, websocketUrl) => ({
  '^/api/.*/connect': {
    target: websocketUrl,
    rewriteWsOrigin: true,
    changeOrigin: true,
    ws: true,
    rewrite: path => path.replace(/^\/api/, '')
  },
  '/api': {
    target: backendUrl,
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, '')
  },
  '/admin': {
    target: 'http://admin:80',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/admin/, ''),
    configure: (proxy, options) => {
      // proxy will be an instance of 'http-proxy'
      proxy.on('proxyReq', function(proxyReq, req, res, options) {
        proxyReq.setHeader('X-Script-Name', 'http://localhost:5173/admin');
      });
    },
  },
})

// https://vite.dev/config/
export default defineConfig(({mode}) => {
  const env = loadEnv(mode, process.cwd(), '')
  return {
    envDir: '../',
    server: {
      // proxy: getProxy(env.BACKEND_URL, env.WEBSOCKET_URL)
      proxy: getProxy(env.BACKEND_URL, env.WEBSOCKET_URL)
    },
    preview: {
      proxy: getProxy(env.BACKEND_URL, env.WEBSOCKET_URL)
    },
    plugins: [svgr(), react()],
  }
})
