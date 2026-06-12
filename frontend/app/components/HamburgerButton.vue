<template>
  <button class="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors" @click="toggle">
    <span class="material-symbols-outlined text-2xl text-slate-700">menu</span>
  </button>
</template>

<script setup>
const { toggle } = useSidebar()
</script>
