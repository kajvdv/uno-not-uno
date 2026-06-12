<script setup lang="ts">
import { Card, CardTitle, Divider, CardFooter } from '@/components/card'
import { Button } from '@/components/button'
import RandomButton from './RandomButton.vue'
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
  <Card>
    <CardTitle>
      <div class="text-2xl opacity-10 mb-2 text-(--ink) tracking-[0.2em]">♠ ♥ ♦ ♣</div>
      <h2 class="font-title text-3xl font-black text-(--ink) mb-1.5">Uno Not Uno</h2>
    </CardTitle>
    <Button class="mb-2.5" type="ink" @click="router.push('/new')"
      >＋ &nbsp;Nieuwe lobby maken</Button
    >
    <Button type="ghost" style="margin-bottom: 10px">→ &nbsp;Lobby joinen met code</Button>
  </Card>
</template>
