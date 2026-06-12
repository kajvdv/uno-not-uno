<script setup lang="ts">
const { color } = defineProps<{
  color: 'red' | 'green' | 'ghost'
}>()
const variant = {
  red: 'bg-(--accent-light) text-(--accent)',
  green: 'bg-(--green-light) text-(--green)',
}
</script>

<template>
  <span
    class="text-xs tracking-widest uppercase rounded-sm border py-0.5 px-1.5 border-[#e8b8ac]"
    :class="variant[color]"
    ><slot></slot
  ></span>
</template>
