<script setup lang="ts">
import { Card } from '@/components/card'
</script>

<template>
  <Card>
    <div class="flex justify-between items-center gap-8">
      <div class="font-title text-3xl font-black tracking-widest text-(--ink)">HX41</div>
      <div
        class="flex-1 text-center max-w-20 tracking-widest text-xs rounded-lg border border-(--border) p-2"
      >
        📋
      </div>
    </div>
    <div class="text-xs text-(--ink-dim) uppercase mt-1">Lobby code — deel met vrienden</div>
    <div class="flex items-center gap-1.5 text-xs text-(--ink-dim) tracking-widest mb-3.5">
      <div class="w-1.5 h-1.5 bg-green-600 rounded-full shrink-0 animate-pulse"></div>
      Wachten op spelers…
    </div>
    <div class="bg-(--warm) border border-(--border) rounded-xl overflow-hidden mb-3.5">
      <div class="flex justify-between py-2 px-3.5 border-b border-(--border) bg-(--cream)">
        <span class="text-xs tracking-widest uppercase text-(--ink-dim)">Spelers</span>
        <span class="text-xs tracking-widest uppercase text-(--ink-dim)">3 / 4</span>
      </div>
      <div class="flex items-center gap-2.5 py-2.5 px-3.5 border-b border-(--border)">
        <div
          class="w-7 h-7 rounded-full bg-(--ink) text-(--cream) flex items-center justify-center text-title text-xs font-bold shrink-0"
        >
          S
        </div>
        <div class="flex-1">
          <div class="text-xs text-(--ink) tracking-wide">Sander</div>
          <div class="text-xs text-(--ink-dim) tracking-widest uppercase">Jij</div>
        </div>
        <span
          class="text-xs tracking-widest uppercase bg-(--accent-light) text-(--accent) rounded-sm border border-[#e8b8ac] py-0.5 px-1.5"
          >Host</span
        >
      </div>
      <div class="flex items-center gap-2.5 py-2.5 px-3.5 border-b border-(--border)">
        <div
          class="w-7 h-7 rounded-full bg-(--ink) text-(--cream) flex items-center justify-center text-title text-xs font-bold shrink-0"
        >
          S
        </div>
        <div class="flex-1">
          <div class="text-xs text-(--ink) tracking-wide">Sander</div>
          <div class="text-xs text-(--ink-dim) tracking-widest uppercase">Jij</div>
        </div>
        <span
          class="text-xs tracking-widest uppercase bg-(--accent-light) text-(--accent) rounded-sm border border-[#e8b8ac] py-0.5 px-1.5"
          >Host</span
        >
      </div>
      <div class="flex items-center gap-2.5 py-2.5 px-3.5 border-b border-(--border)">
        <div
          class="w-7 h-7 rounded-full bg-(--ink) text-(--cream) flex items-center justify-center text-title text-xs font-bold shrink-0"
        >
          S
        </div>
        <div class="flex-1">
          <div class="text-xs text-(--ink) tracking-wide">Sander</div>
          <div class="text-xs text-(--ink-dim) tracking-widest uppercase">Jij</div>
        </div>
        <span
          class="text-xs tracking-widest uppercase bg-(--accent-light) text-(--accent) rounded-sm border border-[#e8b8ac] py-0.5 px-1.5"
          >Host</span
        >
      </div>
      <!-- Laatste child heeft geen border -->
      <div class="flex items-center gap-2.5 py-2.5 px-3.5">
        <div
          class="w-7 h-7 rounded-full bg-transparent border-2 border-dashed border-(--border) text-(--ink-dim) flex items-center justify-center text-title text-sm font-bold shrink-0 animate-spin"
        ></div>
        <div class="flex-1">
          <div class="text-xs text-(--ink-dim) tracking-wide italic">Open plek</div>
          <div class="text-xs text-(--ink-dim) tracking-widest uppercase">Wacht op speler 4</div>
        </div>
      </div>
    </div>
    <div class="text-xs text-(--ink-dim) text-center tracking-widest italic pt-2.5 pb-1">
      Even gedult…<br />
      Het spel begint zodra de lobby vol is.
    </div>
  </Card>
</template>
