import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { LobbyCreate } from '@/types/lobby'

export const useLobbyStore = defineStore('lobby', () => {
  const lobby = ref(null)
  function create(config: LobbyCreate) {}
  return { lobby, create }
})
