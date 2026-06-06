<script setup lang="ts">
const { type = 'ink' } = defineProps<{
  type: 'ink' | 'ghost' | 'shimmer'
}>()
</script>

<template>
  <button :class="['btn', `btn-${type}`]"><slot></slot></button>
</template>

<style scoped>
.btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 13px 16px;
  border-radius: 8px;
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  cursor: pointer;
  border: none;
  transition:
    opacity 0.15s,
    transform 0.1s;
}

.btn-ink {
  background: var(--ink);
  color: var(--cream);
}
.btn-ghost {
  background: transparent;
  color: var(--ink-mid);
  border: 1.5px solid var(--border);
}
.btn-shimmer {
  background: var(--cream);
  color: var(--ink);
  border: 1.5px solid var(--border);
  position: relative;
  overflow: hidden;
}
.btn-shimmer::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.5) 50%,
    transparent 100%
  );
  transform: translateX(-100%);
  transition: none;
}
.btn-shimmer:hover::after {
  animation: shimmer 0.6s ease forwards;
}
@keyframes shimmer {
  to {
    transform: translateX(100%);
  }
}
.btn:active {
  transform: scale(0.98);
}
</style>
