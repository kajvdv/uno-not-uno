import { describe, test, beforeEach } from 'vitest'
import { useLobbyStore } from './lobby'
import { createApp } from 'vue'
import { createPinia, setActivePinia } from 'pinia'

const app = createApp({})
beforeEach(() => {
  const pinia = createPinia()
  app.use(pinia)
  setActivePinia(pinia)
})

describe('Lobby store', () => {
  let store: ReturnType<typeof useLobbyStore>
  beforeEach(() => {
    store = useLobbyStore()
  })

  test('creates new lobby.', () => {
    store.create({ size: 2, creator: 'player 1' })
  })
})
