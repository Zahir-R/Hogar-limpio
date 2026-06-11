<template>
  <div class="bg-[#f6f6ff] text-[#272e42] min-h-screen flex font-body">
    <aside class="fixed left-0 top-0 bottom-0 z-50 flex flex-col h-screen w-72 bg-[#060e20] shadow-lg">
      <div class="p-8">
        <h1 class="text-2xl font-bold tracking-tight text-white font-manrope">Hogar Limpio</h1>
        <p class="text-slate-400 text-xs font-medium mt-1 uppercase tracking-widest">Digital Concierge</p>
      </div>
      <nav class="flex-1 mt-4 space-y-2">
        <a class="bg-[#0056D2] text-white rounded-lg mx-4 py-3 px-4 shadow-lg transition-all flex items-center gap-3" href="#">
          <span class="material-symbols-outlined">dashboard</span>
          <span class="font-medium">Buscar Trabajadores</span>
        </a>
        <NuxtLink to="/client/bookings" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3">
          <span class="material-symbols-outlined">book_online</span>
          <span class="font-medium">Mis Reservas</span>
        </NuxtLink>
      </nav>
      <div class="p-6">
        <NuxtLink to="/client/bookings" class="block w-full bg-gradient-to-r from-[#0053cc] to-[#779dff] text-white py-4 rounded-xl font-bold flex items-center justify-center gap-2 shadow-lg">
          <span class="material-symbols-outlined">add</span> Nueva Solicitud
        </NuxtLink>
      </div>
    </aside>

    <main class="flex-1 lg:pl-72 min-h-screen relative">
      <header class="w-full h-20 sticky top-0 flex justify-between items-center px-12 bg-white/80 backdrop-blur-xl z-40">
        <div class="flex-1 max-w-xl flex items-center gap-4">
          <div class="relative group flex-1">
            <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">search</span>
            <input v-model="filtroBusqueda" class="w-full pl-12 pr-4 py-3 bg-gray-100 border-none rounded-full focus:ring-2 focus:ring-blue-500/20 text-gray-700" placeholder="Buscar especialistas..." type="text"/>
          </div>
          <select v-model="filtroZona" @change="cargarTrabajadores" class="bg-gray-100 border-none rounded-full py-3 pl-4 pr-8 text-sm focus:ring-2 focus:ring-blue-500/20 appearance-none" style="background-image:url('data:image/svg+xml;charset=utf-8,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2212%22 height=%2212%22 viewBox=%220 0 24 24%22 fill=%22%23666%22%3E%3Cpath d=%22M7 10l5 5 5-5z%22/%3E%3C/svg%3E');background-repeat:no-repeat;background-position:right 8px center">
            <option value="">Todas las zonas</option>
            <option v-for="z in zonas" :key="z.id" :value="z.nombre">{{ z.nombre }}</option>
          </select>
        </div>
        <div class="flex items-center gap-6 ml-8">
          <div class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold">{{ avatarInicial }}</div>
        </div>
      </header>

      <div class="px-12 py-10 space-y-12">
        <section class="flex justify-between items-end">
          <div>
            <h2 class="text-4xl font-extrabold text-[#272e42] font-manrope tracking-tight">Hola, {{ nombreUsuario }}</h2>
            <p class="text-gray-500 mt-2 text-lg">Tu hogar está en excelentes manos hoy.</p>
          </div>
        </section>

        <div>
          <h3 class="text-sm font-bold text-gray-400 uppercase tracking-widest mb-6">Trabajadores Disponibles</h3>
          <div v-if="loading" class="text-center py-12 text-gray-400">Cargando trabajadores...</div>
          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="w in filteredWorkers" :key="w.uid" class="bg-white p-5 rounded-xl shadow-sm border border-transparent hover:border-blue-500/20 transition-all flex flex-col h-full">
              <div class="flex items-start justify-between">
                <div class="flex gap-4">
                  <div class="w-14 h-14 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold text-xl overflow-hidden shrink-0">
                    <img v-if="w.profile_photo_url" :src="fotoUrl(w.profile_photo_url)" class="w-full h-full object-cover" />
                    <span v-else>{{ (w.displayName || 'T')[0].toUpperCase() }}</span>
                  </div>
                  <div>
                    <h4 class="font-bold text-[#272e42]">{{ w.displayName || 'Sin nombre' }}</h4>
                    <button @click="abrirReviews(w)" class="flex items-center gap-1 text-orange-500 hover:text-orange-600 mt-0.5">
                      <span class="material-symbols-outlined text-sm">star</span>
                      <span class="text-xs font-bold">{{ w.rating_avg || 0 }}</span>
                      <span class="text-xs text-gray-400">({{ w.rating_count || 0 }} Reseñas)</span>
                    </button>
                    <div v-if="w.documents_verified" class="flex items-center gap-1 text-emerald-600 text-xs mt-1">
                      <span class="material-symbols-outlined text-xs">verified</span>
                      <span>Verificado</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="mt-3 text-sm text-gray-500 space-y-1 flex-1">
                <p v-if="w.zona"><strong>Zona:</strong> {{ w.zona }}</p>
                <p v-if="w.experiencia_anios"><strong>Experiencia:</strong> {{ w.experiencia_anios }} años</p>
                <div v-if="w.servicios?.length" class="mt-2">
                  <p class="text-xs font-semibold text-gray-400 uppercase mb-1">Servicios:</p>
                  <div class="flex flex-wrap gap-1">
                    <span v-for="s in w.servicios" :key="s.id" class="bg-blue-50 text-blue-700 text-xs px-2 py-0.5 rounded-full">
                      {{ s.titulo }} · {{ s.precio }} BOB
                    </span>
                  </div>
                </div>
              </div>
              <button @click="abrirModal(w)" class="w-full mt-4 bg-gray-100 text-[#0053cc] py-3 rounded-lg font-bold hover:bg-[#0053cc] hover:text-white transition-all text-sm">
                Agendar
              </button>
            </div>
            <div v-if="!filteredWorkers.length && !loading" class="col-span-3 text-center py-12 text-gray-400">
              No se encontraron trabajadores disponibles.
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Booking Modal -->
    <div v-if="mostrarModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-lg overflow-hidden border border-slate-200">
        <header class="flex items-center justify-between px-8 py-5 border-b border-slate-100">
          <div>
            <h3 class="text-xl font-bold">Agendar con {{ workerSeleccionado?.displayName || 'Trabajador' }}</h3>
            <p class="text-sm text-gray-500">{{ workerSeleccionado?.zona }}</p>
          </div>
          <button @click="cerrarModal" class="text-gray-500 hover:text-gray-800">Cerrar</button>
        </header>

        <div class="p-8 space-y-5 overflow-y-auto max-h-[60vh]">
          <div class="grid grid-cols-1 gap-5">
            <div class="space-y-2">
              <p class="text-sm font-medium text-slate-700">Servicios</p>
              <div v-if="!workerSeleccionado?.servicios?.length" class="text-sm text-gray-400">Este trabajador no tiene servicios aprobados.</div>
              <label v-for="s in workerSeleccionado?.servicios || []" :key="s.id" class="flex items-center gap-3 p-3 rounded-xl border border-gray-200 cursor-pointer hover:border-blue-300 transition-colors" :class="selectedServicioIds.includes(s.id) ? 'border-blue-500 bg-blue-50' : ''">
                <input type="checkbox" :value="s.id" v-model="selectedServicioIds" class="rounded accent-[#0056D2]" />
                <div class="flex-1">
                  <p class="text-sm font-medium">{{ s.titulo }}</p>
                  <p class="text-xs text-gray-500">{{ s.descripcion?.slice(0, 60) || '' }}</p>
                </div>
                <span class="text-sm font-bold text-[#0053cc]">{{ s.precio }} BOB</span>
              </label>
            </div>
            <label class="space-y-2 text-sm font-medium text-slate-700">
              Fecha
              <input v-model="bookingForm.fecha" type="date" :min="fechaMin" class="w-full rounded-2xl border border-gray-200 p-3 pr-8 text-sm" />
            </label>
            <label class="space-y-2 text-sm font-medium text-slate-700">
              Hora de inicio
              <input v-model="bookingForm.hora_inicio" type="time" class="w-full rounded-2xl border border-gray-200 p-3 pr-8 text-sm" />
            </label>
            <label class="space-y-2 text-sm font-medium text-slate-700">
              Duración
              <select v-model.number="bookingForm.duracion_horas" class="w-full rounded-2xl border border-gray-200 p-3 pr-8 text-sm appearance-none" style="background-image:url('data:image/svg+xml;charset=utf-8,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2212%22 height=%2212%22 viewBox=%220 0 24 24%22 fill=%22%23666%22%3E%3Cpath d=%22M7 10l5 5 5-5z%22/%3E%3C/svg%3E');background-repeat:no-repeat;background-position:right 8px center">
                <option :value="1">1 hora</option>
                <option :value="2">2 horas</option>
                <option :value="3">3 horas</option>
                <option :value="4">4 horas</option>
              </select>
            </label>
            <label class="space-y-2 text-sm font-medium text-slate-700">
              Dirección
              <input v-model="bookingForm.direccion" type="text" class="w-full rounded-2xl border border-gray-200 p-3 pr-8 text-sm" placeholder="Calle, número, edificio..." />
            </label>
            <div class="grid grid-cols-2 gap-4">
              <label class="space-y-2 text-sm font-medium text-slate-700">
                Habitaciones
                <input v-model.number="bookingForm.rooms" type="number" min="1" @input="calcularPrecio" class="w-full rounded-2xl border border-gray-200 p-3 pr-8 text-sm" />
              </label>
              <label class="space-y-2 text-sm font-medium text-slate-700">
                Metros²
                <input v-model.number="bookingForm.sqm" type="number" min="10" @input="calcularPrecio" class="w-full rounded-2xl border border-gray-200 p-3 pr-8 text-sm" />
              </label>
            </div>
            <div class="text-lg font-bold text-[#0053cc]">
              Total estimado: {{ precioEstimado ? `${precioEstimado} BOB` : '—' }}
            </div>
          </div>
        </div>

        <footer class="px-8 py-5 bg-slate-50 border-t border-slate-100 flex flex-col sm:flex-row gap-3 justify-end">
          <button @click="cerrarModal" class="px-5 py-3 text-sm font-medium rounded-full border border-gray-200 text-slate-700 hover:bg-gray-50">Cancelar</button>
          <button @click="confirmarReserva" :disabled="creando || !selectedServicioIds.length" class="px-5 py-3 text-sm font-bold rounded-full bg-[#0056D2] text-white hover:bg-[#004bb2] disabled:opacity-50">
            {{ creando ? 'Creando...' : 'Confirmar Reserva' }}
          </button>
        </footer>
        <p v-if="mensajeModal" class="px-8 pb-5 text-sm font-medium" :class="mensajeModal.includes('Error') ? 'text-red-600' : 'text-emerald-600'">{{ mensajeModal }}</p>
      </div>
    </div>

    <!-- Reviews Modal -->
    <div v-if="mostrarReviews" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-lg overflow-hidden border border-slate-200">
        <header class="flex items-center justify-between px-8 py-5 border-b border-slate-100">
          <div>
            <h3 class="text-xl font-bold">Reseñas de {{ workerReviews?.displayName || 'Trabajador' }}</h3>
            <p class="text-sm text-gray-500">{{ workerReviews?.rating_avg || 0 }} ★ ({{ workerReviews?.rating_count || 0 }} reseñas)</p>
          </div>
          <button @click="cerrarReviews" class="text-gray-500 hover:text-gray-800">Cerrar</button>
        </header>
        <div class="p-8 space-y-4 max-h-96 overflow-y-auto">
          <div v-if="cargandoReviews" class="text-center text-gray-400">Cargando...</div>
          <div v-else-if="!reviewsList.length" class="text-center text-gray-400 py-8">Aún no hay reseñas para este trabajador.</div>
          <div v-for="r in reviewsList" :key="r.id" class="border-b border-gray-100 pb-4 last:border-0">
            <p class="text-sm font-semibold text-gray-800">{{ r.clientName || 'Cliente' }}</p>
            <div class="flex items-center gap-1 text-orange-400 text-sm mt-1">
              <span v-for="n in 5" :key="n" :class="n <= r.rating ? '' : 'text-gray-300'">★</span>
              <span class="text-gray-500 ml-2 text-xs">{{ r.rating }}/5</span>
            </div>
            <p v-if="r.comment" class="text-sm text-gray-700 mt-2">{{ r.comment }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const auth = useAuth()
const trabajadores = ref([])
const zonas = ref([])
const loading = ref(true)
const filtroBusqueda = ref('')
const filtroZona = ref('')

// Booking modal
const mostrarModal = ref(false)
const workerSeleccionado = ref(null)
const selectedServicioIds = ref([])
const creando = ref(false)
const mensajeModal = ref('')
const precioEstimado = ref(null)

const bookingForm = ref({
  fecha: '',
  hora_inicio: '09:00',
  duracion_horas: 2,
  direccion: '',
  rooms: 2,
  sqm: 60
})

// Reviews modal
const mostrarReviews = ref(false)
const workerReviews = ref(null)
const reviewsList = ref([])
const cargandoReviews = ref(false)

const fotoUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `http://localhost:8000${url}`
}

const fechaMin = computed(() => {
  const d = new Date()
  return d.toISOString().split('T')[0]
})

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

const filteredWorkers = computed(() => {
  let result = trabajadores.value
  if (filtroBusqueda.value) {
    const q = filtroBusqueda.value.toLowerCase()
    result = result.filter(w => (w.displayName || '').toLowerCase().includes(q) || (w.zona || '').toLowerCase().includes(q))
  }
  return result
})

const cargarTrabajadores = async () => {
  try {
    const token = await auth.getToken(true)
    const params = filtroZona.value ? { zona: filtroZona.value } : {}
    trabajadores.value = await $fetch('http://localhost:8000/api/workers', {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` },
      params
    })
  } catch (e) {
    console.error('Error cargando trabajadores:', e)
    trabajadores.value = []
  }
}

const cargarZonas = async () => {
  try {
    zonas.value = await $fetch('http://localhost:8000/api/zonas')
  } catch (e) {
    console.error('Error cargando zonas:', e)
  }
}

const abrirModal = (worker) => {
  workerSeleccionado.value = worker
  selectedServicioIds.value = worker.servicios?.length ? [worker.servicios[0].id] : []
  bookingForm.value = {
    fecha: fechaMin.value,
    hora_inicio: '09:00',
    duracion_horas: 2,
    direccion: '',
    rooms: 2,
    sqm: 60
  }
  precioEstimado.value = null
  mensajeModal.value = ''
  mostrarModal.value = true
  setTimeout(calcularPrecio, 100)
}

const cerrarModal = () => {
  mostrarModal.value = false
  workerSeleccionado.value = null
}

const calcularPrecio = async () => {
  if (!bookingForm.value.rooms || !bookingForm.value.sqm) return
  try {
    const token = await auth.getToken(true)
    const result = await $fetch('http://localhost:8000/api/pricing/calcular', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: {
        rooms: bookingForm.value.rooms,
        sqm: bookingForm.value.sqm,
        zona: workerSeleccionado.value?.zona || null
      }
    })
    precioEstimado.value = result.total
  } catch (e) {
    console.error('Error calculando precio:', e)
  }
}

const confirmarReserva = async () => {
  if (!selectedServicioIds.value.length) {
    mensajeModal.value = 'Selecciona al menos un servicio.'
    return
  }
  creando.value = true
  mensajeModal.value = ''
  try {
    const token = await auth.getToken(true)
    const worker = workerSeleccionado.value

    const result = await $fetch('http://localhost:8000/api/reservas', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: {
        worker_uid: worker.uid,
        servicio_ids: selectedServicioIds.value,
        fecha: bookingForm.value.fecha,
        hora_inicio: bookingForm.value.hora_inicio,
        duracion_horas: bookingForm.value.duracion_horas,
        direccion: bookingForm.value.direccion,
        zona: worker.zona || '',
        rooms: bookingForm.value.rooms,
        sqm: bookingForm.value.sqm
      }
    })
    mensajeModal.value = `Reserva creada exitosamente. Total: ${result.precio_total} BOB`
    setTimeout(() => {
      cerrarModal()
      navigateTo('/client/bookings')
    }, 1500)
  } catch (e) {
    console.error('Error creando reserva:', e.data || e)
    mensajeModal.value = 'Error al crear la reserva: ' + (e.data?.detail || 'Error de red')
  } finally {
    creando.value = false
  }
}

const abrirReviews = async (worker) => {
  workerReviews.value = worker
  mostrarReviews.value = true
  cargandoReviews.value = true
  reviewsList.value = []
  try {
    const token = await auth.getToken(true)
    reviewsList.value = await $fetch(`http://localhost:8000/api/reviews/${worker.uid}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
  } catch (e) {
    console.error('Error cargando reviews:', e)
  } finally {
    cargandoReviews.value = false
  }
}

const cerrarReviews = () => {
  mostrarReviews.value = false
  workerReviews.value = null
  reviewsList.value = []
}

useHead({
  link: [
    { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined' }
  ]
})

onMounted(async () => {
  await Promise.all([cargarTrabajadores(), cargarZonas()])
  loading.value = false
})
</script>
