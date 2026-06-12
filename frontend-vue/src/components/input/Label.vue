<script setup lang="ts"></script>

<template>
  <label class="label"><slot></slot></label>
</template>

<style scoped>
.label {
  display: block;
  font-size: 9px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--ink-mid);
  margin-bottom: 6px;
}
</style>
