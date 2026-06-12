<script setup lang="ts">
import { Card } from '@/components/card'
import { InputGroup, TextInput, Label, Select } from '@/components/input'
</script>

<template>
  <Card>
    <RouterLink class="back-link" to="/">← Terug</RouterLink>
    <div class="title">Lobby aanmaken</div>
    <div class="sub-title">Kies een naam en stel de regels in.</div>
    <InputGroup>
      <Label>Jouw naam in dit spel</Label>
      <TextInput placeholder="bijv. Sander" />
      <div class="hint">Zo zien andere spelers jou in de lobby.</div>
    </InputGroup>
    <InputGroup>
      <Label>Max. aantal spelers</Label>
      <Select>
        <option>2 spelers</option>
        <option>3 spelers</option>
        <option selected>4 spelers</option>
        <option>5 spelers</option>
        <option>6 spelers</option>
      </Select>
    </InputGroup>
  </Card>
</template>

<style scoped>
.back-link {
  font-size: 9px;
  color: var(--ink-dim);
  letter-spacing: 0.15em;
  text-transform: uppercase;
  margin-bottom: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
}

.title {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  font-weight: 700;
  color: var(--ink);
  line-height: 1.15;
  margin-bottom: 3px;
}

.sub-title {
  font-size: 9px;
  color: var(--ink-dim);
  letter-spacing: 0.12em;
  margin-bottom: 22px;
}
.hint {
  font-size: 8px;
  color: var(--ink-dim);
  letter-spacing: 0.08em;
  margin-top: 4px;
  font-style: italic;
}
</style>
