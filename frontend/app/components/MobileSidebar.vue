<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition-opacity duration-300 ease-out"
      leave-active-class="transition-opacity duration-200 ease-in"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isOpen"
        class="fixed inset-0 bg-black/50 backdrop-blur-sm z-[200] lg:hidden"
        @click="close"
      />
    </Transition>
    <Transition
      enter-active-class="transition-transform duration-300 ease-out"
      leave-active-class="transition-transform duration-200 ease-in"
      enter-from-class="-translate-x-full"
      enter-to-class="translate-x-0"
      leave-from-class="translate-x-0"
      leave-to-class="-translate-x-full"
    >
      <aside
        v-if="isOpen"
        class="fixed left-0 top-0 bottom-0 z-[210] flex flex-col h-screen w-72 bg-[#060e20] shadow-lg lg:hidden"
      >
        <div class="flex items-center justify-between p-6">
          <slot name="header" />
          <button class="text-slate-400 hover:text-white transition-colors" @click="close">
            <span class="material-symbols-outlined text-2xl">close</span>
          </button>
        </div>
        <nav class="flex-1 mt-2 space-y-1 overflow-y-auto" @click="close">
          <slot />
        </nav>
      </aside>
    </Transition>
  </Teleport>
</template>

<script setup>
const { isOpen, close } = useSidebar()
</script>
