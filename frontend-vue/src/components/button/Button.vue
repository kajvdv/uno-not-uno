<script setup lang="ts">
const { type = 'ink' } = defineProps<{
  type: 'ink' | 'ghost' | 'green'
}>()

const variant = {
  ink: 'bg-(--ink) text-white',
  ghost: 'transparent border border-(--border) text-(--ink)',
  green: 'bg-(--green) text-white',
}
</script>

<template>
  <button
    class="flex items-center w-full rounded-lg justify-center gap-2 px-4 py-3 cursor-pointer uppercase text-xs transition-opacity transition-transform"
    :class="variant[type]"
  >
    <slot></slot>
  </button>
</template>
