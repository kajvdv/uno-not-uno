<template>
  <input class="field-input text-center uppercase placeholder:text-center" />
</template>

<style scoped>
.field-input {
  width: 100%;
  border: 1.5px solid var(--border);
  box-sizing: border-box;
  border-radius: 7px;
  padding: 10px 12px;
  font-family: 'DM Mono', monospace;
  font-size: 13px;
  color: var(--ink);
  background: var(--cream);
  outline: none;
  transition:
    border-color 0.15s,
    background 0.15s;
}

.field-input:focus {
  border-color: var(--border-focus);
}
</style>
