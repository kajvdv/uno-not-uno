<template>
    <div class="card-title">
        <slot></slot>
    </div>
</template>

<style scoped>
.card-title {
    text-align: center;
    padding: 16px 0 22px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 22px;
}

.card-title :deep(h2) {
    font-family: 'Playfair Display', serif;
    font-size: 26px; font-weight: 900; color: var(--ink);
    line-height: 1.1; margin-bottom: 6px;
}

.card-title :deep(p) {
    font-size: 10px; color: var(--ink-dim); letter-spacing: 0.12em;
}
</style>