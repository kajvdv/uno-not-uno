import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { LobbyCreate, LobbyResponse } from '@/types/lobby'
import { useApi } from '@/plugins/client'

export const useLobbyStore = defineStore('lobby', () => {
  const lobby = ref(null)
  const api = useApi()
  async function create(config: LobbyCreate) {
    const response: LobbyResponse = await api.lobby.createLobby(config)
    lobby.value = response
  }
  return { lobby, create }
})
