<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition-opacity duration-200 ease-out"
      leave-active-class="transition-opacity duration-150 ease-in"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="state.visible"
        class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center z-[110] p-4"
        @click.self="cancel"
      >
        <div class="bg-white rounded-3xl shadow-2xl w-full max-w-md overflow-hidden">
          <header class="px-6 pt-6 pb-2 flex items-center gap-3">
            <span class="material-symbols-outlined text-2xl text-amber-500">warning</span>
            <h3 class="text-lg font-bold text-slate-800">{{ state.title }}</h3>
          </header>
          <div class="px-6 py-4">
            <p class="text-slate-600">{{ state.message }}</p>
          </div>
          <footer class="px-6 pb-6 flex justify-end gap-3">
            <button
              class="px-5 py-2.5 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-50 font-medium transition-colors"
              @click="cancel"
            >
              Cancelar
            </button>
            <button
              class="px-5 py-2.5 rounded-xl bg-red-500 text-white hover:bg-red-600 font-medium transition-colors"
              @click="accept"
            >
              Confirmar
            </button>
          </footer>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
const { state, accept, cancel } = useConfirm()
</script>
