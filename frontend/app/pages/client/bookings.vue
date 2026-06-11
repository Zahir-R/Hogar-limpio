<template>
  <div class="bg-[#f6f6ff] text-[#272e42] min-h-screen flex font-body">
    <aside class="fixed left-0 top-0 bottom-0 z-50 flex flex-col h-screen w-72 bg-[#060e20] shadow-lg">
      <div class="p-8">
        <h1 class="text-2xl font-bold tracking-tight text-white font-manrope">Hogar Limpio</h1>
        <p class="text-slate-400 text-xs font-medium mt-1 uppercase tracking-widest">Mis Reservas</p>
      </div>
      <nav class="flex-1 mt-4 space-y-2">
        <NuxtLink to="/client-dashboard" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3">
          <span class="material-symbols-outlined">dashboard</span>
          <span class="font-medium">Buscar Trabajadores</span>
        </NuxtLink>
        <a class="bg-[#0056D2] text-white rounded-lg mx-4 py-3 px-4 shadow-lg transition-all flex items-center gap-3" href="#">
          <span class="material-symbols-outlined">book_online</span>
          <span class="font-medium">Mis Reservas</span>
        </a>
      </nav>
    </aside>

    <main class="flex-1 lg:pl-72 min-h-screen relative">
      <header class="w-full h-20 sticky top-0 flex justify-between items-center px-12 bg-white/80 backdrop-blur-xl z-40">
        <div class="flex items-center gap-3 pl-6">
          <div class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold">{{ avatarInicial }}</div>
          <div class="text-left">
            <p class="text-sm font-bold">{{ nombreUsuario }}</p>
            <p class="text-xs text-gray-500">Cliente</p>
          </div>
        </div>
      </header>

      <div class="px-12 py-10 space-y-8">
        <section>
          <h2 class="text-4xl font-extrabold text-[#272e42] font-manrope tracking-tight">Mis Reservas</h2>
          <p class="text-gray-500 mt-2 text-lg">Gestiona tus servicios agendados.</p>
        </section>

        <section class="bg-white rounded-3xl shadow-sm border border-gray-100 p-6">
          <div v-if="loading" class="text-center py-12 text-gray-400">Cargando reservas...</div>
          <div v-else-if="!reservas.length" class="text-center py-12 text-gray-400">
            No tienes reservas aún.
            <NuxtLink to="/client-dashboard" class="block mt-2 text-[#0056D2] hover:underline">Buscar trabajadores</NuxtLink>
          </div>
          <div v-else class="space-y-4">
            <div v-for="r in reservas" :key="r.id" class="rounded-3xl border border-gray-200 p-5 hover:shadow-lg transition-shadow">
              <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
                <div>
                  <p class="text-lg font-bold">{{ r.direccion || 'Dirección no especificada' }}</p>
                  <p class="text-sm text-gray-500">{{ r.fecha }} a las {{ r.hora_inicio }} — {{ r.duracion_horas }}h</p>
                  <p class="text-sm text-gray-500" v-if="r.worker_uid">Trabajador ID: {{ r.worker_uid.slice(0, 12) }}...</p>
                  <p class="text-sm text-gray-500" v-if="r.zona">Zona: {{ r.zona }}</p>
                </div>
                <div class="text-right">
                  <span :class="badgeClass(r.estado)" class="text-xs font-semibold uppercase px-3 py-1 rounded-full">{{ r.estado }}</span>
                  <p class="text-xl font-bold text-[#0053cc] mt-2">{{ formatPrice(r.precio_total) }}</p>
                  <span v-if="r.pago" :class="pagoBadgeClass(r.pago.estado)" class="text-xs font-medium px-2 py-0.5 rounded-full mt-1 inline-block">
                    Pago: {{ r.pago.estado }}
                  </span>
                </div>
              </div>
              <div class="mt-4 flex flex-wrap gap-2">
                <button v-if="r.estado === 'Confirmado'" @click="completarReserva(r)" class="px-4 py-2 rounded-full bg-emerald-600 text-white text-sm hover:bg-emerald-700">Completar</button>
                <button v-if="r.estado === 'Pendiente' || r.estado === 'Confirmado'" @click="cancelarReserva(r.id)" class="px-4 py-2 rounded-full bg-red-600 text-white text-sm hover:bg-red-700">Cancelar</button>
              </div>
            </div>
          </div>
          <p v-if="mensaje" class="mt-4 text-sm font-medium" :class="mensaje.includes('Error') ? 'text-red-600' : 'text-emerald-600'">{{ mensaje }}</p>
        </section>
      </div>
    </main>

    <!-- Review Modal -->
    <div v-if="mostrarReview" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-md overflow-hidden border border-slate-200">
        <header class="px-8 py-5 border-b border-slate-100">
          <h3 class="text-xl font-bold">Califica tu servicio</h3>
          <p class="text-sm text-gray-500">Tu opinión ayuda a mejorar la comunidad.</p>
        </header>
        <div class="p-8 space-y-5 text-center">
          <div class="flex justify-center gap-2 text-4xl">
            <button v-for="n in 5" :key="n" @click="reviewRating = n" :class="n <= reviewRating ? 'text-orange-400' : 'text-gray-300'" class="transition-colors hover:text-orange-400">
              ★
            </button>
          </div>
          <textarea v-model="reviewComment" placeholder="Escribe un comentario (opcional)" class="w-full rounded-2xl border border-gray-200 p-3 text-sm" rows="3"></textarea>
        </div>
        <footer class="px-8 py-5 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
          <button @click="mostrarReview = false" class="px-5 py-3 text-sm font-medium rounded-full border border-gray-200 text-slate-700 hover:bg-gray-50">Omitir</button>
          <button @click="enviarReview" :disabled="!reviewRating || enviando" class="px-5 py-3 text-sm font-bold rounded-full bg-[#0056D2] text-white hover:bg-[#004bb2] disabled:opacity-50">
            {{ enviando ? 'Enviando...' : 'Enviar' }}
          </button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const auth = useAuth()
const reservas = ref([])
const loading = ref(true)
const mensaje = ref('')

// Review modal
const mostrarReview = ref(false)
const reviewReserva = ref(null)
const reviewRating = ref(0)
const reviewComment = ref('')
const enviando = ref(false)

const nombreUsuario = computed(() => {
  const user = auth.user.value
  if (!user) return 'Invitado'
  if (user.displayName) return user.displayName
  if (user.email) return user.email.split('@')[0].charAt(0).toUpperCase() + user.email.split('@')[0].slice(1)
  return 'Usuario'
})

const avatarInicial = computed(() => {
  const u = auth.user.value
  return (u?.displayName || u?.email || 'U')[0].toUpperCase()
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

const getToken = async () => await auth.getToken(true)

const cargarReservas = async () => {
  try {
    const token = await getToken()
    const data = await $fetch('http://localhost:8000/api/reservas', {
      headers: { Authorization: `Bearer ${token}` }
    })
    for (const r of data) {
      try {
        r.pago = await $fetch(`http://localhost:8000/api/payments/${r.id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
      } catch {
        r.pago = null
      }
    }
    reservas.value = data
  } catch (e) {
    console.error('Error cargando reservas:', e)
  } finally {
    loading.value = false
  }
}

const completarReserva = async (r) => {
  try {
    const token = await getToken()
    await $fetch(`http://localhost:8000/api/reservas/${r.id}/completar`, {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${token}` }
    })
    mensaje.value = 'Servicio marcado como completado.'
    reviewReserva.value = r
    reviewRating.value = 0
    reviewComment.value = ''
    mostrarReview.value = true
    await cargarReservas()
  } catch (e) {
    console.error('Error completando reserva:', e)
    mensaje.value = 'Error al completar.'
  }
}

const cancelarReserva = async (id) => {
  if (!confirm('¿Cancelar esta reserva?')) return
  try {
    const token = await getToken()
    await $fetch(`http://localhost:8000/api/reservas/${id}/cancelar`, {
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

const enviarReview = async () => {
  if (!reviewRating.value) return
  enviando.value = true
  try {
    const token = await getToken()
    await $fetch('http://localhost:8000/api/reviews', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: {
        servicio_id: reviewReserva.value.servicio_id,
        worker_uid: reviewReserva.value.worker_uid,
        rating: reviewRating.value,
        comment: reviewComment.value
      }
    })
    mostrarReview.value = false
    reviewReserva.value = null
    alert('¡Gracias por tu calificación!')
  } catch (e) {
    console.error('Error enviando review:', e.data || e)
    alert('Error al enviar la calificación.')
  } finally {
    enviando.value = false
  }
}

onMounted(cargarReservas)
</script>
