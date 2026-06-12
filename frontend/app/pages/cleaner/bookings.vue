<template>
  <div class="bg-[#f6f6ff] text-[#272e42] min-h-screen font-body">
    <aside class="fixed left-0 top-0 bottom-0 z-50 flex flex-col h-screen w-72 bg-[#060e20] shadow-lg hidden lg:flex">
      <div class="p-8">
        <h1 class="text-2xl font-bold tracking-tight text-white font-manrope">Hogar Limpio</h1>
        <p class="text-slate-400 text-xs mt-1 font-medium tracking-widest uppercase">Reservas</p>
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
        <NuxtLink to="/cleaner/availability" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3">
          <span class="material-symbols-outlined">calendar_month</span>
          <span class="font-medium">Disponibilidad</span>
        </NuxtLink>
        <NuxtLink to="/cleaner/bookings" class="bg-[#0056D2] text-white rounded-lg mx-4 py-3 px-4 shadow-lg flex items-center gap-3">
          <span class="material-symbols-outlined">book_online</span>
          <span class="font-medium">Reservas</span>
        </NuxtLink>
        <button @click="auth.logout()" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3 w-[calc(100%-2rem)] mx-4">
          <span class="material-symbols-outlined">logout</span>
          <span class="font-medium">Cerrar Sesión</span>
        </button>
      </nav>
    </aside>

    <MobileSidebar>
      <template #header>
        <div>
          <h1 class="text-2xl font-bold tracking-tight text-white font-manrope">Hogar Limpio</h1>
          <p class="text-slate-400 text-xs mt-1 font-medium tracking-widest uppercase">Reservas</p>
        </div>
      </template>
      <NuxtLink to="/cleaner-dashboard" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3">
        <span class="material-symbols-outlined">inventory_2</span>
        <span class="font-medium">Mis Servicios</span>
      </NuxtLink>
      <NuxtLink to="/cleaner/profile" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3">
        <span class="material-symbols-outlined">person</span>
        <span class="font-medium">Mi Perfil</span>
      </NuxtLink>
      <NuxtLink to="/cleaner/availability" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3">
        <span class="material-symbols-outlined">calendar_month</span>
        <span class="font-medium">Disponibilidad</span>
      </NuxtLink>
      <NuxtLink to="/cleaner/bookings" class="bg-[#0056D2] text-white rounded-lg mx-4 py-3 px-4 shadow-lg flex items-center gap-3">
        <span class="material-symbols-outlined">book_online</span>
        <span class="font-medium">Reservas</span>
      </NuxtLink>
      <button @click="auth.logout()" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3 w-[calc(100%-2rem)]">
        <span class="material-symbols-outlined">logout</span>
        <span class="font-medium">Cerrar Sesión</span>
      </button>
    </MobileSidebar>

    <div class="lg:pl-72 flex flex-col min-h-screen">
      <header class="w-full h-16 lg:h-20 sticky top-0 bg-white/80 backdrop-blur-xl flex justify-between items-center px-4 sm:px-8 lg:px-12 z-40">
        <HamburgerButton />
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
          <h2 class="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight font-manrope">Mis Reservas</h2>
          <p class="text-gray-500 mt-2 text-lg">Gestiona las reservas asignadas a ti.</p>
        </section>

        <section class="bg-white rounded-3xl shadow-sm border border-gray-100 p-6">
          <div v-if="!reservas.length" class="text-center py-12 text-gray-400">No tienes reservas asignadas.</div>
          <div v-else class="space-y-4">
            <div v-for="r in reservas" :key="r.id" class="rounded-3xl border border-gray-200 p-5">
              <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start gap-3">
                <div>
                  <p class="text-lg font-bold">{{ r.direccion || 'Dirección no especificada' }}</p>
                  <p class="text-sm text-gray-500">{{ r.fecha }} a las {{ r.hora_inicio }} — {{ r.duracion_horas }}h</p>
                  <p class="text-sm text-gray-500">Zona: {{ r.zona || 'N/A' }}</p>
                  <p class="text-lg font-bold mt-2 text-[#0056D2]">{{ formatPrice(r.precio_total) }}</p>
                  <span v-if="r.pago" :class="pagoBadgeClass(r.pago.estado)" class="text-xs font-medium px-2 py-0.5 rounded-full mt-1 inline-block">
                    Pago: {{ r.pago.estado }}
                  </span>
                </div>
                <span :class="badgeClass(r.estado)" class="text-xs font-semibold uppercase px-3 py-1 rounded-full">{{ r.estado }}</span>
              </div>
              <div class="mt-4 flex flex-wrap gap-2">
                <button v-if="r.estado === 'Pendiente'" @click="confirmarReserva(r.id)" class="px-4 py-2 rounded-full bg-emerald-600 text-white text-sm hover:bg-emerald-700">Confirmar</button>
                <button v-if="r.estado === 'Confirmado' || r.estado === 'Pendiente'" @click="cancelarReserva(r.id)" class="px-4 py-2 rounded-full bg-red-600 text-white text-sm hover:bg-red-700">Cancelar</button>
              </div>
            </div>
          </div>
          <p v-if="mensaje" class="mt-4 text-sm font-medium" :class="mensaje.includes('Error') ? 'text-red-600' : 'text-emerald-600'">{{ mensaje }}</p>
        </section>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const auth = useAuth()
const { public: { apiBase } } = useRuntimeConfig()
const { confirm: confirmar } = useConfirm()
const reservas = ref([])
const mensaje = ref('')

const nombreTrabajador = computed(() => {
  return auth.user.value?.displayName || auth.user.value?.email?.split('@')[0] || 'Trabajador'
})

const avatarInicial = computed(() => {
  return (auth.user.value?.displayName || auth.user.value?.email || 'T')[0].toUpperCase()
})

const formatPrice = (value) => {
  return new Intl.NumberFormat('es-BO', { style: 'currency', currency: 'BOB' }).format(value || 0)
}

const badgeClass = (estado) => {
  if (estado === 'Completado') return 'bg-emerald-100 text-emerald-700'
  if (estado === 'Cancelado') return 'bg-red-100 text-red-700'
  if (estado === 'Confirmado') return 'bg-blue-100 text-blue-700'
  if (estado === 'En_curso') return 'bg-purple-100 text-purple-700'
  return 'bg-yellow-100 text-yellow-700'
}

const pagoBadgeClass = (estado) => {
  if (estado === 'Liberado') return 'bg-emerald-100 text-emerald-700'
  if (estado === 'Reembolsado') return 'bg-red-100 text-red-700'
  if (estado === 'Retenido') return 'bg-blue-100 text-blue-700'
  return 'bg-gray-100 text-gray-500'
}

const cargarReservas = async () => {
  try {
    const token = await auth.getToken(true)
    const data = await $fetch(`${apiBase}/api/reservas`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    for (const r of data) {
      try {
        r.pago = await $fetch(`${apiBase}/api/payments/${r.id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
      } catch {
        r.pago = null
      }
    }
    reservas.value = data
  } catch (e) {
    console.error('Error cargando reservas:', e)
  }
}

const confirmarReserva = async (id) => {
  try {
    const token = await auth.getToken(true)
    await $fetch(`${apiBase}/api/reservas/${id}/confirmar`, {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${token}` }
    })
    mensaje.value = 'Reserva confirmada.'
    await cargarReservas()
  } catch (e) {
    console.error('Error confirmando reserva:', e)
    mensaje.value = 'Error al confirmar.'
  }
}

const cancelarReserva = async (id) => {
  if (!await confirmar('¿Cancelar esta reserva?')) return
  try {
    const token = await auth.getToken(true)
    await $fetch(`${apiBase}/api/reservas/${id}/cancelar`, {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${token}` }
    })
    mensaje.value = 'Reserva cancelada.'
    await cargarReservas()
  } catch (e) {
    console.error('Error cancelando reserva:', e)
    mensaje.value = 'Error al cancelar.'
  }
}

onMounted(cargarReservas)
</script>
