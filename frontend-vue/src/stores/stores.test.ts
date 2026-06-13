import { describe, test, beforeEach, expect } from 'vitest'
import { useLobbyStore } from './lobby'
import { createApp } from 'vue'
import { createPinia, setActivePinia } from 'pinia'
import { createApi } from '@/plugins/client'
import api from '@/api/mock'

beforeEach(() => {
  const app = createApp({})
  const pinia = createPinia()
  app.use(pinia)
  app.use(createApi(api))
  setActivePinia(pinia)
})

describe('Lobby store', () => {
  let store: ReturnType<typeof useLobbyStore>
  beforeEach(() => {
    store = useLobbyStore()
  })

  test('creates new lobby.', async () => {
    await store.create({ size: 2, creator: 'player 1' })
    expect(store.lobby).toBeTruthy()
  })
})
