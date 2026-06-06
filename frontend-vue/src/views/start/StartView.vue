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
      <div class="suit-row">♠ ♥ ♦ ♣</div>
      <h2>Speel mee.<br />Geen account.</h2>
      <p>2 – 6 spelers &nbsp;·&nbsp; gratis &nbsp;·&nbsp; direct</p>
    </CardTitle>
    <Button @click="router.push('/new')" type="ink" style="margin-bottom: 10px"
      >＋ &nbsp;Nieuwe lobby maken</Button
    >
    <Button type="ghost" style="margin-bottom: 10px">→ &nbsp;Lobby joinen met code</Button>
    <Divider>of</Divider>
    <RandomButton />
    <CardFooter>
      <strong>Geen account nodig.</strong><br />
      Je naam kies je per spel.
    </CardFooter>
  </Card>
</template>

<style scoped>
.suit-row {
  font-size: 24px;
  letter-spacing: 0.2em;
  color: var(--ink);
  opacity: 0.1;
  margin-bottom: 8px;
}
</style>
