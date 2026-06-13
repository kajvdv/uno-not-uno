import createLobbyResponse from '@/../data/create_response.json'
import type { Api } from '@/types/api'

const api: Api = {
  lobby: {
    async createLobby() {
      return createLobbyResponse
    },
  },
}

export default api
