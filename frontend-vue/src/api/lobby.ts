import type { LobbyCreate } from '@/types/lobby'

export async function createLobby({ creator, size }: LobbyCreate) {
  const response = await fetch('/api/lobbies', {
    method: 'post',
    body: JSON.stringify({ creator, size }),
    headers: {
      'Content-Type': 'application/json',
    },
  })
  return await response.json()
}
