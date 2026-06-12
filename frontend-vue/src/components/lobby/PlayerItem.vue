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
      class="w-7 h-7 rounded-full bg-(--ink) text-(--cream) flex items-center justify-center text-title text-xs font-bold shrink-0"
    >
      {{ title.at(0)?.toUpperCase() }}
    </div>
    <div class="flex-1">
      <div class="text-xs text-(--ink) tracking-wide">{{ title }}</div>
      <div class="text-xs text-(--ink-dim) tracking-widest uppercase">{{ description }}</div>
    </div>
    <slot></slot>
  </div>
</template>
