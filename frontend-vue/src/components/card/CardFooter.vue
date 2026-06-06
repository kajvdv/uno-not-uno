<script setup lang="ts"></script>

<template>
  <div class="card-footer">
    <slot></slot>
  </div>
</template>

<style scoped>
.card-footer {
  text-align: center;
  font-size: 9px;
  color: var(--ink-dim);
  margin-top: 18px;
  letter-spacing: 0.08em;
  padding-top: 14px;
  border-top: 1px dashed var(--border);
  line-height: 1.6;
}
</style>
