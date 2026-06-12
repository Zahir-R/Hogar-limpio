<template>
  <div class="bg-[#f6f6ff] text-[#272e42] min-h-screen flex font-body">
    <aside class="fixed left-0 top-0 bottom-0 z-50 flex flex-col h-screen w-72 bg-[#060e20] shadow-lg hidden lg:flex">
      <div class="p-8">
        <h1 class="text-2xl font-bold tracking-tight text-white font-manrope">Hogar Limpio</h1>
        <p class="text-slate-400 text-xs font-medium mt-1 uppercase tracking-widest">Mi Perfil</p>
      </div>
      <nav class="flex-1 mt-4 space-y-2">
        <NuxtLink to="/client-dashboard" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3">
          <span class="material-symbols-outlined">dashboard</span>
          <span class="font-medium">Buscar Trabajadores</span>
        </NuxtLink>
        <NuxtLink to="/client/bookings" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3">
          <span class="material-symbols-outlined">book_online</span>
          <span class="font-medium">Mis Reservas</span>
        </NuxtLink>
        <a class="bg-[#0056D2] text-white rounded-lg mx-4 py-3 px-4 shadow-lg transition-all flex items-center gap-3" href="#">
          <span class="material-symbols-outlined">person</span>
          <span class="font-medium">Mi Perfil</span>
        </a>
        <button @click="auth.logout()" class="mt-auto text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3 w-[calc(100%-2rem)] mx-4">
          <span class="material-symbols-outlined">logout</span>
          <span class="font-medium">Cerrar Sesión</span>
        </button>
      </nav>
    </aside>

    <MobileSidebar>
      <template #header>
        <div>
          <h1 class="text-2xl font-bold tracking-tight text-white font-manrope">Hogar Limpio</h1>
          <p class="text-slate-400 text-xs font-medium mt-1 uppercase tracking-widest">Mi Perfil</p>
        </div>
      </template>
      <NuxtLink to="/client-dashboard" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3">
        <span class="material-symbols-outlined">dashboard</span>
        <span class="font-medium">Buscar Trabajadores</span>
      </NuxtLink>
      <NuxtLink to="/client/bookings" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3">
        <span class="material-symbols-outlined">book_online</span>
        <span class="font-medium">Mis Reservas</span>
      </NuxtLink>
      <NuxtLink to="/client/profile" class="bg-[#0056D2] text-white rounded-lg mx-4 py-3 px-4 shadow-lg flex items-center gap-3">
        <span class="material-symbols-outlined">person</span>
        <span class="font-medium">Mi Perfil</span>
      </NuxtLink>
      <button @click="auth.logout()" class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3 w-[calc(100%-2rem)]">
        <span class="material-symbols-outlined">logout</span>
        <span class="font-medium">Cerrar Sesión</span>
      </button>
    </MobileSidebar>

    <main class="flex-1 lg:pl-72 min-h-screen relative">
      <header class="w-full h-16 lg:h-20 sticky top-0 flex justify-between items-center px-4 sm:px-8 lg:px-12 bg-white/80 backdrop-blur-xl z-40">
        <HamburgerButton />
        <div class="flex items-center gap-3 pl-2 sm:pl-6">
          <div class="w-10 h-10 rounded-full bg-blue-600 overflow-hidden flex items-center justify-center text-white font-bold">
            <img v-if="profilePhotoUrl" :src="fotoPerfil" class="w-full h-full object-cover" />
            <span v-else>{{ avatarInicial }}</span>
          </div>
          <div class="text-left">
            <p class="text-sm font-bold">{{ nombreUsuario }}</p>
            <p class="text-xs text-gray-500">Cliente</p>
          </div>
        </div>
      </header>

      <div class="px-4 sm:px-8 lg:px-12 py-6 sm:py-10 space-y-8">
        <section>
          <h2 class="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-[#272e42] font-manrope tracking-tight">Mi Perfil</h2>
          <p class="text-gray-500 mt-2 text-lg">Administra tu información personal.</p>
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
                  <img v-else-if="form.profile_photo_url" :src="fotoUrlComputed" class="w-full h-full object-cover" />
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

          <div class="flex gap-4">
            <button type="submit" :disabled="guardando" class="px-6 py-3 rounded-full bg-[#0056D2] text-white font-semibold hover:bg-[#004bb2] shadow-lg disabled:opacity-50">
              {{ guardando ? 'Guardando...' : 'Guardar Cambios' }}
            </button>
            <NuxtLink to="/client-dashboard" class="px-6 py-3 rounded-full border border-gray-200 text-slate-700 font-medium hover:bg-gray-50">
              Cancelar
            </NuxtLink>
          </div>

          <p v-if="mensaje" class="text-sm font-medium" :class="mensaje.includes('Error') ? 'text-red-600' : 'text-emerald-600'">{{ mensaje }}</p>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const auth = useAuth()
const { public: { apiBase } } = useRuntimeConfig()
const loading = ref(true)
const guardando = ref(false)
const mensaje = ref('')
const fotoPreview = ref('')
const subiendo = ref(false)
const profilePhotoUrl = ref('')

const fotoUrlComputed = computed(() => {
  const url = form.value.profile_photo_url
  if (!url) return ''
  if (url.startsWith('http') || url.startsWith('data:')) return url
  return `${apiBase}${url}`
})

const fotoPerfil = computed(() => {
  if (fotoPreview.value) return fotoPreview.value
  if (profilePhotoUrl.value) {
    const url = profilePhotoUrl.value
    if (url.startsWith('http') || url.startsWith('data:')) return url
    return `${apiBase}${url}`
  }
  return ''
})

const form = ref({
  displayName: '',
  profile_photo_url: ''
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
    profilePhotoUrl.value = result.url
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
    profilePhotoUrl.value = perfil.profile_photo_url || ''
  } catch (e) {
    console.error('Error cargando perfil:', e)
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
        profile_photo_url: form.value.profile_photo_url || undefined
      }
    })
    if (auth.user.value) {
      auth.user.value.displayName = form.value.displayName
    }
    mensaje.value = 'Perfil actualizado correctamente.'
  } catch (e) {
    console.error('Error guardando perfil:', e)
    mensaje.value = 'Error al guardar el perfil.'
  } finally {
    guardando.value = false
  }
}

useHead({
  link: [
    { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined' }
  ]
})

onMounted(async () => {
  await cargarPerfil()
  loading.value = false
})
</script>
