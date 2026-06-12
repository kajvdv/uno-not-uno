<script setup lang="ts">
const {
  title,
  description,
  border = true,
} = defineProps<{
  title: string
  description: string
  border?: boolean
}>()
</script>

<template>
  <div
    class="flex items-center gap-2.5 py-2.5 px-3.5"
    :class="{ 'border-b border-(--border)': border }"
  >
    <div
      class="w-7 h-7 rounded-full bg-transparent border-2 border-dashed border-(--border) text-(--ink-dim) flex items-center justify-center text-title text-sm font-bold shrink-0 animate-spin"
    ></div>
    <div class="flex-1">
      <div class="text-xs text-(--ink-dim) tracking-wide italic">{{ title }}</div>
      <div class="text-xs text-(--ink-dim) tracking-widest uppercase">{{ description }}</div>
    </div>
  </div>
</template>
