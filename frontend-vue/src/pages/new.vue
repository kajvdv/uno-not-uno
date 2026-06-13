<script setup lang="ts">
import { Button } from '@/components/buttons'
import { Card } from '@/components/card'
import { useLobbyStore } from '@/stores/lobby'
import type { LobbyCreate } from '@/types/lobby'
import { ref } from 'vue'

const lobbyStore = useLobbyStore()

const username = ref('')
const size = ref(4)

function createLobby() {
  lobbyStore.create({ creator: username.value, size: size.value })
  console.log('Creating lobby')
}
</script>

<template>
  <Card>
    <RouterLink v-slot="{ navigate, isActive }" to="/" custom>
      <div class="mb-5">
        <a
          @click="navigate"
          class="text-xs hover:underline cursor-pointer text-(--ink-dim) uppercase"
          >← Terug</a
        >
      </div>
    </RouterLink>
    <div class="font-title text-lg font-bold text-(--ink) mb-1">Lobby aanmaken</div>
    <div class="text-xs text-(--ink-mid) mb-5">Kies een naam en stel de regels in.</div>
    <form @submit.prevent="createLobby">
      <div class="mb-4">
        <label class="block mb-1.5 text-xs text-(--ink-mid)" for="username"
          >Jouw naam in dit spel</label
        >
        <input
          v-model="username"
          class="w-full border box-border rounded-md py-2.5 px-3 text-sm text-(--ink) bg-(--cream) border-(--border) focus:border-(--border-focus) outline-0"
          name="username"
          type="text"
          placeholder="bijv. Sander"
          required
        />
        <div class="text-xs text-(--ink-dim) mt-1 italic">Zo zien andere jou in de lobby.</div>
      </div>
      <div>
        <label class="block mb-1.5 text-xs text-(--ink-mid)" for="playerCount"
          >Aantal spelers</label
        >
        <select
          v-model="size"
          name="playerCount"
          class="w-full border box-border rounded-md py-2.5 px-3 text-sm text-(--ink) bg-(--cream) border-(--border) focus:border-(--border-focus) outline-0"
        >
          <option value="2">2 spelers</option>
          <option value="3">3 spelers</option>
          <option value="4">4 spelers</option>
          <option value="5">5 spelers</option>
          <option value="6">6 spelers</option>
        </select>
        <div class="text-xs text-(--ink-dim) mt-1 italic">2 – 6 spelers toegestaan.</div>
        <RouterLink to="/lobby" v-slot="{ navigate }" custom>
          <Button
            @click="
              () => {
                createLobby()
                navigate()
              }
            "
            type="green"
            class="mt-4"
            >Maak lobby aan →</Button
          >
        </RouterLink>
      </div>
    </form>
  </Card>
</template>
