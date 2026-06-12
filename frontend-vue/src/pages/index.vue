<script setup lang="ts">
import { Card, CardTitle } from '@/components/card'
import { Button } from '@/components/buttons'
import { TextInput } from '@/components/input/index.ts'

function joinLobby() {
  console.log('joining lobby')
}
</script>

<template>
  <Card>
    <CardTitle>
      <div class="text-2xl opacity-10 mb-2 text-(--ink) tracking-[0.2em]">♠ ♥ ♦ ♣</div>
      <h2 class="font-title text-3xl font-black text-(--ink) mb-1.5 uppercase">
        Stack<br />Attack
      </h2>
    </CardTitle>
    <RouterLink to="/new" v-slot="{ navigate, isActive }" custom>
      <Button class="mb-2.5" type="ink"" @click="navigate"
        >＋ &nbsp;Nieuwe lobby maken</Button
      >
    </RouterLink>
    <div class="flex gap-2.5 my-3.5 mx-0">
      <span
        class="flex flex-1 uppercase text-(--ink-dim) text-xs items-center gap-2.5 before:flex-1 before:content-[''] before:h-px before:bg-(--border) after:flex-1 after:content-[''] after:h-px after:bg-(--border)"
        >of</span
      >
    </div>
    <form @submit.prevent="joinLobby">
      <TextInput name="code" class="mb-3.5" placeholder="Code"></TextInput>
      <Button type="ghost" style="margin-bottom: 10px">→ &nbsp;Lobby joinen met code</Button>
    </form>
  </Card>
</template>
