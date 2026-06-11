<template>
  <div class="bg-[#f6f6ff] text-[#272e42] min-h-screen font-body">
    <aside class="fixed left-0 top-0 bottom-0 z-50 flex flex-col h-screen w-72 bg-[#060e20] shadow-lg hidden lg:flex">
      <div class="p-8">
        <h1 class="text-2xl font-bold tracking-tight text-white font-manrope">Hogar Limpio</h1>
        <p class="text-slate-400 text-xs mt-1 font-medium tracking-widest uppercase">Disponibilidad</p>
      </div>
      <nav class="flex-1 mt-4 space-y-1">
        <NuxtLink to="/cleaner-dashboard" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3">
          <span class="material-symbols-outlined">inventory_2</span>
          <span class="font-medium">Mis Servicios</span>
        </NuxtLink>
        <NuxtLink to="/cleaner/profile" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3">
          <span class="material-symbols-outlined">person</span>
          <span class="font-medium">Mi Perfil</span>
        </NuxtLink>
        <NuxtLink to="/cleaner/availability" class="bg-[#0056D2] text-white rounded-lg mx-4 py-3 px-4 shadow-lg flex items-center gap-3">
          <span class="material-symbols-outlined">calendar_month</span>
          <span class="font-medium">Disponibilidad</span>
        </NuxtLink>
        <NuxtLink to="/cleaner/bookings" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3">
          <span class="material-symbols-outlined">book_online</span>
          <span class="font-medium">Reservas</span>
        </NuxtLink>
        <button @click="auth.logout()" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3 w-[calc(100%-2rem)] mx-4">
          <span class="material-symbols-outlined">logout</span>
          <span class="font-medium">Cerrar Sesión</span>
        </button>
      </nav>
    </aside>

    <div class="lg:pl-72 flex flex-col min-h-screen">
      <header class="w-full h-20 sticky top-0 bg-white/80 backdrop-blur-xl flex justify-between items-center px-12 z-40">
        <div class="flex items-center flex-1 max-w-xl">
          <div class="relative w-full">
            <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">search</span>
            <input class="w-full bg-gray-100 border-none rounded-full py-2.5 pl-12 pr-4" placeholder="Buscar..." type="text" disabled />
          </div>
        </div>
        <div class="flex items-center gap-3 pl-6">
          <div class="text-right">
            <p class="text-sm font-bold">{{ nombreTrabajador }}</p>
            <p class="text-xs text-gray-500">Personal de Limpieza</p>
          </div>
          <div class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold">{{ avatarInicial }}</div>
        </div>
      </header>

      <main class="p-8 lg:p-12 space-y-10">
        <section>
          <h2 class="text-4xl font-extrabold tracking-tight font-manrope">Disponibilidad</h2>
          <p class="text-gray-500 mt-2 text-lg">Define tu horario semanal habitual.</p>
        </section>

        <div v-if="loading" class="text-center py-4 text-gray-400">Cargando...</div>

        <div v-else class="max-w-3xl space-y-6">
          <div v-for="(dayLabel, key) in diasSemana" :key="key" class="bg-white rounded-3xl shadow-sm border border-gray-100 p-6">
            <h3 class="text-lg font-bold mb-4 capitalize">{{ dayLabel }}</h3>
            <div v-for="(slot, i) in weekdays[key]" :key="i" class="flex items-center gap-4 mb-3">
              <label class="space-y-1">
                <span class="text-xs text-gray-500">Inicio</span>
                <input v-model="slot.start" type="time" class="border border-gray-200 rounded-lg p-2 text-sm" />
              </label>
              <label class="space-y-1">
                <span class="text-xs text-gray-500">Fin</span>
                <input v-model="slot.end" type="time" class="border border-gray-200 rounded-lg p-2 text-sm" />
              </label>
              <button @click="removerSlot(key, i)" class="mt-5 text-red-500 hover:text-red-700 text-sm">Eliminar</button>
            </div>
            <button @click="agregarSlot(key)" class="mt-2 text-sm text-[#0056D2] hover:underline">+ Añadir horario</button>
          </div>

          <div class="flex gap-4">
            <button @click="guardarTemplate" :disabled="guardando" class="px-6 py-3 rounded-full bg-[#0056D2] text-white font-semibold hover:bg-[#004bb2] shadow-lg disabled:opacity-50">
              {{ guardando ? 'Guardando...' : 'Guardar Disponibilidad' }}
            </button>
            <NuxtLink to="/cleaner-dashboard" class="px-6 py-3 rounded-full border border-gray-200 text-slate-700 font-medium hover:bg-gray-50">
              Cancelar
            </NuxtLink>
          </div>

          <p v-if="mensaje" class="text-sm font-medium" :class="mensaje.includes('Error') ? 'text-red-600' : 'text-emerald-600'">{{ mensaje }}</p>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const auth = useAuth()
const loading = ref(true)
const guardando = ref(false)
const mensaje = ref('')

const diasSemana = {
  monday: 'Lunes',
  tuesday: 'Martes',
  wednesday: 'Miércoles',
  thursday: 'Jueves',
  friday: 'Viernes',
  saturday: 'Sábado',
  sunday: 'Domingo'
}

// Use ref with a plain object instead of reactive for simpler reactivity
const weekdays = ref({
  monday: [],
  tuesday: [],
  wednesday: [],
  thursday: [],
  friday: [],
  saturday: [],
  sunday: []
})

const nombreTrabajador = computed(() => {
  return auth.user.value?.displayName || auth.user.value?.email?.split('@')[0] || 'Trabajador'
})

const avatarInicial = computed(() => {
  return (auth.user.value?.displayName || auth.user.value?.email || 'T')[0].toUpperCase()
})

const agregarSlot = (day) => {
  weekdays.value[day].push({ start: '09:00', end: '17:00' })
}

const removerSlot = (day, index) => {
  weekdays.value[day].splice(index, 1)
}

const cargarTemplate = async () => {
  try {
    const token = await auth.getToken(true)
    const uid = auth.user.value?.uid
    if (!uid) return

    const data = await $fetch(`http://localhost:8000/api/availability/${uid}`, {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` }
    })
    console.log('[DEBUG] Availability API response:', JSON.stringify(data))

    // data.template may contain weekdays at top level or nested
    const src = data.template?.weekdays || data.template || {}
    for (const day of Object.keys(diasSemana)) {
      if (Array.isArray(src[day])) {
        weekdays.value[day] = src[day].map(s => ({ start: s.start || '', end: s.end || '' }))
      } else {
        weekdays.value[day] = []
      }
    }
    console.log('[DEBUG] Parsed weekdays:', JSON.stringify(weekdays.value))
  } catch (e) {
    console.error('Error cargando disponibilidad:', e)
  } finally {
    loading.value = false
  }
}

const guardarTemplate = async () => {
  guardando.value = true
  mensaje.value = ''
  try {
    const token = await auth.getToken(true)
    const payload = { weekdays: weekdays.value }
    console.log('[DEBUG] Saving availability payload:', JSON.stringify(payload))

    await $fetch('http://localhost:8000/api/availability', {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: payload
    })
    mensaje.value = 'Disponibilidad guardada correctamente.'
  } catch (e) {
    console.error('Error guardando disponibilidad:', e.data || e)
    mensaje.value = 'Error al guardar la disponibilidad.'
  } finally {
    guardando.value = false
  }
}

onMounted(cargarTemplate)
</script>
