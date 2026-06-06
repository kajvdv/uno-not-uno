<script setup lang="ts">
import { Button } from '@/components/button'
</script>

<template>
  <Button type="shimmer">
    <div class="random-btn-inner">
      <div class="rbi-top">
        <span class="dice">🎲</span>
        RANDOM LOBBY JOINEN
      </div>
      <div class="rbi-sub">Word meteen gekoppeld aan een open lobby</div>
    </div>
  </Button>
</template>

<style scoped>
.random-btn-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1px;
}
.random-btn-inner .rbi-top {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  letter-spacing: 0.12em;
}
.random-btn-inner .rbi-sub {
  font-size: 8px;
  color: var(--ink-dim);
  letter-spacing: 0.1em;
  text-transform: none;
}
</style>
