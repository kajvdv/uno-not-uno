<script setup lang="ts">
import { Card, CardTitle } from '@/components/card';
</script>

<template>
    <Card>
        <CardTitle>
            <div class="suit-row">♠ ♥ ♦ ♣</div>
            <h2>Speel mee.<br>Geen account.</h2>
            <p>2 – 6 spelers &nbsp;·&nbsp; gratis &nbsp;·&nbsp; direct</p>
        </CardTitle>
    </Card>
</template>

<style scoped>
.suit-row {
    font-size: 24px; letter-spacing: 0.2em;
    color: var(--ink); opacity: 0.1; margin-bottom: 8px;
}
</style>
