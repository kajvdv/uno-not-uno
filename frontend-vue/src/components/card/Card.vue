<template>
    <div class="card" style="max-width: 300px;">
        <slot></slot>
    </div>
</template>

<style scoped>
.card {
    margin: 0 auto;
    background: #fff;
    width: 100%;
    border: 1px solid var(--border);
    border-radius: 20px;
    box-shadow: var(--shadow);
    padding: 22px 20px 28px;
}
</style>