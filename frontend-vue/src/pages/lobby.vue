<script setup lang="ts">
import { Card } from '@/components/card'
import { LobbyBadge } from '@/components/badges'
import { PlayerList, PlayerItem, PendingItem } from '@/components/lobby'

const players = [
  { name: 'Jaap' },
  { name: 'Sander' },
  { name: 'Lisa' },
  // { name: 'Lisa' },
  // { name: 'Karen' },
]
</script>

<template>
  <Card>
    <div class="flex justify-between items-center gap-8">
      <div class="font-title text-3xl font-black tracking-widest text-(--ink)">HX41</div>
      <div
        class="flex-1 text-center max-w-20 tracking-widest text-xs rounded-lg border border-(--border) p-2"
      >
        📋
      </div>
    </div>
    <div class="text-xs text-(--ink-dim) uppercase mt-1">Lobby code — deel met vrienden</div>
    <div class="flex items-center gap-1.5 text-xs text-(--ink-dim) tracking-widest mb-3.5">
      <div class="w-1.5 h-1.5 bg-green-600 rounded-full shrink-0 animate-pulse"></div>
      Wachten op spelers…
    </div>
    <PlayerList :data="players" :max-players="4"></PlayerList>
    <div class="text-xs text-(--ink-dim) text-center tracking-widest italic pt-2.5 pb-1">
      Even gedult…<br />
      Het spel begint zodra de lobby vol is.
    </div>
  </Card>
</template>
