<template>
  <Teleport to="body">
    <div class="fixed top-4 right-4 z-[100] flex flex-col gap-3 pointer-events-none">
      <TransitionGroup
        enter-active-class="transition-all duration-300 ease-out"
        leave-active-class="transition-all duration-200 ease-in"
        enter-from-class="translate-x-8 opacity-0"
        enter-to-class="translate-x-0 opacity-100"
        leave-from-class="translate-x-0 opacity-100"
        leave-to-class="translate-x-8 opacity-0"
      >
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="pointer-events-auto flex items-center gap-3 min-w-[280px] sm:min-w-[320px] max-w-md px-4 py-3 rounded-xl shadow-lg border"
          :class="styles[toast.type]"
        >
          <span class="material-symbols-outlined text-xl shrink-0" :class="iconColor[toast.type]">
            {{ icons[toast.type] }}
          </span>
          <p class="flex-1 text-sm font-medium text-slate-800">{{ toast.message }}</p>
          <button
            class="shrink-0 text-slate-400 hover:text-slate-600 transition-colors"
            @click="remove(toast.id)"
          >
            <span class="material-symbols-outlined text-lg">close</span>
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
const { toasts, remove } = useToast()

const icons: Record<string, string> = {
  success: 'check_circle',
  error: 'error',
  info: 'info',
}

const iconColor: Record<string, string> = {
  success: 'text-emerald-500',
  error: 'text-red-500',
  info: 'text-blue-500',
}

const styles: Record<string, string> = {
  success: 'bg-white border-emerald-200',
  error: 'bg-white border-red-200',
  info: 'bg-white border-blue-200',
}
</script>
