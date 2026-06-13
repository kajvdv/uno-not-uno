import type { Api } from '@/types/api'

import { inject, type App } from 'vue'

const clientKey = Symbol('client')

export const createApi = (client: Api) => ({
  install: (app: App) => {
    app.provide(clientKey, client)
  },
})

export function useApi(): Api {
  const client = inject(clientKey) as Api
  if (!client) {
    throw Error('Client was not installed')
  } else {
    return client
  }
}
