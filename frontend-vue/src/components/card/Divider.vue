<script setup lang="ts"></script>

<template>
  <div class="divider-or">
    <span><slot></slot></span>
  </div>
</template>

<style scoped>
.divider-or {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 10px 0;
}

.divider-or::before,
.divider-or::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}

.divider-or span {
  font-size: 9px;
  color: var(--ink-dim);
  letter-spacing: 0.2em;
  text-transform: uppercase;
}
</style>
