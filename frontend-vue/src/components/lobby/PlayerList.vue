<script setup lang="ts">
import { LobbyBadge } from '../badges'
import { PlayerItem, PendingItem } from '.'
import type { LobbyPlayer } from '@/types/lobby'

const { data, maxPlayers } = defineProps<{
  data: LobbyPlayer[]
  maxPlayers: number
}>()
</script>

<template>
  <div class="bg-(--warm) border border-(--border) rounded-xl overflow-hidden mb-3.5">
    <div class="flex justify-between py-2 px-3.5 border-b border-(--border) bg-(--cream)">
      <span class="text-xs tracking-widest uppercase text-(--ink-dim)">Spelers</span>
      <span class="text-xs tracking-widest uppercase text-(--ink-dim)">3 / {{ maxPlayers }}</span>
    </div>
    <PlayerItem
      v-for="(player, index) in data"
      :title="player.name"
      description="is gejoint"
      :border="index < maxPlayers - 1"
    >
      <LobbyBadge color="green">Klaar</LobbyBadge>
    </PlayerItem>
    <PendingItem
      v-for="(index, player) in maxPlayers - data.length"
      title="Open plek"
      :description="'Wacht op speler ' + (index + data.length)"
      :border="index < maxPlayers - data.length"
    ></PendingItem>
  </div>
</template>
