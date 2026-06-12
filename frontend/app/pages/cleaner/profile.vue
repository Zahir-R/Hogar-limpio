<template>
  <div class="bg-[#f6f6ff] text-[#272e42] min-h-screen font-body">
    <aside class="fixed left-0 top-0 bottom-0 z-50 flex flex-col h-screen w-72 bg-[#060e20] shadow-lg hidden lg:flex">
      <div class="p-8">
        <h1 class="text-2xl font-bold tracking-tight text-white font-manrope">Hogar Limpio</h1>
        <p class="text-slate-400 text-xs mt-1 font-medium tracking-widest uppercase">Perfil</p>
      </div>
      <nav class="flex-1 mt-4 space-y-1">
        <NuxtLink to="/cleaner-dashboard" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3">
          <span class="material-symbols-outlined">inventory_2</span>
          <span class="font-medium">Mis Servicios</span>
        </NuxtLink>
        <NuxtLink to="/cleaner/profile" class="bg-[#0056D2] text-white rounded-lg mx-4 py-3 px-4 shadow-lg flex items-center gap-3">
          <span class="material-symbols-outlined">person</span>
          <span class="font-medium">Mi Perfil</span>
        </NuxtLink>
        <NuxtLink to="/cleaner/availability" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3">
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

    <MobileSidebar>
      <template #header>
        <div>
          <h1 class="text-2xl font-bold tracking-tight text-white font-manrope">Hogar Limpio</h1>
          <p class="text-slate-400 text-xs mt-1 font-medium tracking-widest uppercase">Perfil</p>
        </div>
      </template>
      <NuxtLink to="/cleaner-dashboard" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3">
        <span class="material-symbols-outlined">inventory_2</span>
        <span class="font-medium">Mis Servicios</span>
      </NuxtLink>
      <NuxtLink to="/cleaner/profile" class="bg-[#0056D2] text-white rounded-lg mx-4 py-3 px-4 shadow-lg flex items-center gap-3">
        <span class="material-symbols-outlined">person</span>
        <span class="font-medium">Mi Perfil</span>
      </NuxtLink>
      <NuxtLink to="/cleaner/availability" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3">
        <span class="material-symbols-outlined">calendar_month</span>
        <span class="font-medium">Disponibilidad</span>
      </NuxtLink>
      <NuxtLink to="/cleaner/bookings" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3">
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
          <div v-if="fotoPreview || form.profile_photo_url" class="w-10 h-10 rounded-full bg-blue-600 overflow-hidden flex items-center justify-center text-white font-bold">
            <img v-if="fotoPreview || form.profile_photo_url" :src="fotoPreview || fotoUrl" class="w-full h-full object-cover" />
            <span v-else>{{ avatarInicial }}</span>
          </div>
          <div v-else class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold">{{ avatarInicial }}</div>
        </div>
      </header>

      <main class="p-8 lg:p-12 space-y-10">
        <section>
          <h2 class="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight font-manrope">Mi Perfil</h2>
          <p v-if="esNuevo" class="text-emerald-600 mt-2 text-lg">Completa tu perfil para empezar a recibir trabajos.</p>
          <p v-else class="text-gray-500 mt-2 text-lg">Administra tu información personal y profesional.</p>
        </section>

        <div v-if="loading" class="text-center py-20 text-gray-400">Cargando perfil...</div>

        <form v-else @submit.prevent="guardarPerfil" class="max-w-2xl space-y-6">
          <div class="bg-white rounded-3xl shadow-sm border border-gray-100 p-6 space-y-5">
            <h3 class="text-xl font-bold">Información Personal</h3>

            <label class="space-y-2 text-sm font-medium text-slate-700 block">
              Nombre Completo
              <input v-model="form.displayName" type="text" class="w-full rounded-2xl border border-gray-200 p-3 text-sm focus:ring-2 focus:ring-blue-200" />
            </label>

            <div class="space-y-2">
              <p class="text-sm font-medium text-slate-700">Foto de Perfil</p>
              <div class="flex items-center gap-4">
                <div class="w-20 h-20 rounded-full bg-gray-100 border-2 border-dashed border-gray-300 overflow-hidden flex items-center justify-center text-gray-400 shrink-0">
                  <img v-if="fotoPreview" :src="fotoPreview" class="w-full h-full object-cover" />
                  <img v-else-if="form.profile_photo_url" :src="fotoUrl" class="w-full h-full object-cover" />
                  <span v-else class="material-symbols-outlined text-3xl">person</span>
                </div>
                <div class="flex-1">
                  <label class="cursor-pointer inline-block px-4 py-2 rounded-full bg-[#0056D2] text-white text-sm font-medium hover:bg-[#004bb2]">
                    Seleccionar archivo
                    <input type="file" accept="image/*" @change="onFileSelected" class="hidden" />
                  </label>
                  <p class="text-xs text-gray-400 mt-1">JPG, PNG. Máximo 2MB.</p>
                  <p v-if="subiendo" class="text-xs text-blue-600 mt-1">Subiendo...</p>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-3xl shadow-sm border border-gray-100 p-6 space-y-5">
            <h3 class="text-xl font-bold">Información Profesional</h3>

            <label class="space-y-2 text-sm font-medium text-slate-700 block">
              Zona de Trabajo
              <select v-model="form.zona" class="w-full rounded-2xl border border-gray-200 p-3 pr-8 text-sm appearance-none" style="background-image:url('data:image/svg+xml;charset=utf-8,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2212%22 height=%2212%22 viewBox=%220 0 24 24%22 fill=%22%23666%22%3E%3Cpath d=%22M7 10l5 5 5-5z%22/%3E%3C/svg%3E');background-repeat:no-repeat;background-position:right 8px center">
                <option value="">Selecciona una zona</option>
                <option v-for="z in zonas" :key="z.id" :value="z.nombre">{{ z.nombre }}</option>
              </select>
            </label>

            <label class="space-y-2 text-sm font-medium text-slate-700 block">
              Años de Experiencia
              <input v-model.number="form.experiencia_anios" type="number" min="0" step="0.5" class="w-full rounded-2xl border border-gray-200 p-3 text-sm focus:ring-2 focus:ring-blue-200" />
            </label>

            <div class="space-y-2">
              <p class="text-sm font-medium text-slate-700">Tipo de Perfil</p>
              <div class="flex gap-6">
                <label class="flex items-center gap-2 text-sm">
                  <input type="radio" v-model="form.tipo_perfil" value="independiente" />
                  Independiente
                </label>
                <label class="flex items-center gap-2 text-sm">
                  <input type="radio" v-model="form.tipo_perfil" value="dedicado" />
                  Dedicado
                </label>
              </div>
            </div>
          </div>

          <div class="flex gap-4">
            <button type="submit" :disabled="guardando" class="px-6 py-3 rounded-full bg-[#0056D2] text-white font-semibold hover:bg-[#004bb2] shadow-lg disabled:opacity-50">
              {{ guardando ? 'Guardando...' : 'Guardar Cambios' }}
            </button>
            <NuxtLink to="/cleaner-dashboard" class="px-6 py-3 rounded-full border border-gray-200 text-slate-700 font-medium hover:bg-gray-50">
              Cancelar
            </NuxtLink>
          </div>

          <p v-if="mensaje" class="text-sm font-medium" :class="mensaje.includes('Error') ? 'text-red-600' : 'text-emerald-600'">{{ mensaje }}</p>
        </form>

        <section v-if="reviews.length" class="bg-white rounded-3xl shadow-sm border border-gray-100 p-6">
          <h3 class="text-xl font-bold mb-4">Mis Reseñas</h3>
          <div class="space-y-4">
            <div v-for="r in reviews" :key="r.id" class="border-b border-gray-100 pb-4 last:border-0">
              <div class="flex items-center gap-1 text-orange-400 text-sm">
                <span v-for="n in 5" :key="n" :class="n <= r.rating ? '' : 'text-gray-300'">★</span>
                <span class="text-gray-500 ml-2 text-xs">{{ r.rating }}/5</span>
              </div>
              <p v-if="r.comment" class="text-sm text-gray-700 mt-1">{{ r.comment }}</p>
            </div>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const auth = useAuth()
const { public: { apiBase } } = useRuntimeConfig()
const zonas = ref([])
const loading = ref(true)
const guardando = ref(false)
const mensaje = ref('')
const reviews = ref([])
const fotoPreview = ref('')
const subiendo = ref(false)

const esNuevo = computed(() => {
  return !form.value.zona && !form.value.profile_photo_url && form.value.experiencia_anios === 0
})

const fotoUrl = computed(() => {
  const url = form.value.profile_photo_url
  if (!url) return ''
  if (url.startsWith('http') || url.startsWith('data:')) return url
  return `${apiBase}${url}`
})

const form = ref({
  displayName: '',
  profile_photo_url: '',
  zona: '',
  experiencia_anios: 0,
  tipo_perfil: 'independiente'
})

const nombreTrabajador = computed(() => {
  return auth.user.value?.displayName || auth.user.value?.email?.split('@')[0] || 'Trabajador'
})

const avatarInicial = computed(() => {
  return (auth.user.value?.displayName || auth.user.value?.email || 'T')[0].toUpperCase()
})

const onFileSelected = async (e) => {
  const file = e.target.files?.[0]
  if (!file) return

  fotoPreview.value = URL.createObjectURL(file)
  subiendo.value = true

  try {
    const token = await auth.getToken(true)
    const formData = new FormData()
    formData.append('file', file)

    const result = await $fetch(`${apiBase}/api/users/profile/photo`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: formData
    })
    form.value.profile_photo_url = result.url
  } catch (e) {
    console.error('Error subiendo foto:', e)
    mensaje.value = 'Error al subir la foto.'
    fotoPreview.value = ''
  } finally {
    subiendo.value = false
  }
}

const cargarPerfil = async () => {
  try {
    const token = await auth.getToken(true)
    const perfil = await $fetch(`${apiBase}/api/users/profile`, {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` }
    })
    form.value.displayName = perfil.displayName || ''
    form.value.profile_photo_url = perfil.profile_photo_url || ''
    form.value.zona = perfil.zona || ''
    form.value.experiencia_anios = perfil.experiencia_anios || 0
    form.value.tipo_perfil = perfil.tipo_perfil || 'independiente'
  } catch (e) {
    console.error('Error cargando perfil:', e)
  }
}

const cargarZonas = async () => {
  try {
    zonas.value = await $fetch(`${apiBase}/api/zonas`)
  } catch (e) {
    console.error('Error cargando zonas:', e)
  }
}

const cargarReviews = async () => {
  const uid = auth.user.value?.uid
  if (!uid) return
  try {
    const token = await auth.getToken(true)
    reviews.value = await $fetch(`${apiBase}/api/reviews/${uid}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
  } catch (e) {
    console.error('Error cargando reviews:', e)
  }
}

const guardarPerfil = async () => {
  guardando.value = true
  mensaje.value = ''
  try {
    const token = await auth.getToken(true)
    await $fetch(`${apiBase}/api/users/profile`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: {
        displayName: form.value.displayName || undefined,
        profile_photo_url: form.value.profile_photo_url || undefined,
        zona: form.value.zona || undefined,
        experiencia_anios: form.value.experiencia_anios || undefined,
        tipo_perfil: form.value.tipo_perfil || undefined
      }
    })
    mensaje.value = 'Perfil actualizado correctamente.'
  } catch (e) {
    console.error('Error guardando perfil:', e)
    mensaje.value = 'Error al guardar el perfil.'
  } finally {
    guardando.value = false
  }
}

onMounted(async () => {
  await Promise.all([cargarPerfil(), cargarZonas(), cargarReviews()])
  loading.value = false
})
</script>
