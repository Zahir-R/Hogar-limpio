<template>
  <div class="min-h-screen bg-[#f6f6ff] text-slate-950">
    <header class="fixed inset-x-0 top-0 z-50 border-b border-white/30 bg-white/10 backdrop-blur-xl transition-colors duration-500">
      <div class="mx-auto flex max-w-7xl items-center justify-between px-6 py-4 sm:px-8">
        <NuxtLink to="/" class="text-lg font-semibold tracking-tight text-slate-950">Hogar Limpio</NuxtLink>
        <nav class="hidden items-center gap-8 md:flex">
          <a href="#servicios" class="text-sm font-medium text-slate-700 transition hover:text-slate-950">Servicios</a>
          <a href="#como-funciona" class="text-sm font-medium text-slate-700 transition hover:text-slate-950">Cómo funciona</a>
          <NuxtLink to="/login" class="text-sm font-medium text-slate-700 transition hover:text-slate-950">Iniciar Sesión</NuxtLink>
        </nav>
        <div class="flex items-center gap-3">
          <NuxtLink to="/login" class="hidden rounded-2xl border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-950 transition hover:border-slate-400 hover:bg-slate-50 md:inline-flex">Iniciar Sesión</NuxtLink>
          <NuxtLink to="/signup" class="inline-flex rounded-2xl bg-[#135bec] px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-[#135bec]/15 transition hover:bg-[#0f4ed2]">Registrarse</NuxtLink>
          <button class="md:hidden p-2 rounded-lg hover:bg-white/20 transition-colors" @click="mobileMenuOpen = !mobileMenuOpen">
            <span class="material-symbols-outlined text-2xl text-slate-800">{{ mobileMenuOpen ? 'close' : 'menu' }}</span>
          </button>
        </div>
      </div>
      <Transition
        enter-active-class="transition-all duration-200 ease-out"
        leave-active-class="transition-all duration-150 ease-in"
        enter-from-class="opacity-0 -translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-2"
      >
        <nav v-if="mobileMenuOpen" class="md:hidden border-t border-white/20 bg-white/95 backdrop-blur-xl px-6 py-4 space-y-1" @click="mobileMenuOpen = false">
          <a href="#servicios" class="block rounded-xl px-4 py-3 text-sm font-medium text-slate-700 hover:bg-slate-100 transition">Servicios</a>
          <a href="#como-funciona" class="block rounded-xl px-4 py-3 text-sm font-medium text-slate-700 hover:bg-slate-100 transition">Cómo funciona</a>
          <NuxtLink to="/login" class="block rounded-xl px-4 py-3 text-sm font-medium text-slate-700 hover:bg-slate-100 transition">Iniciar Sesión</NuxtLink>
          <NuxtLink to="/signup" class="block rounded-xl px-4 py-3 text-sm font-medium text-[#135bec] hover:bg-blue-50 transition">Registrarse</NuxtLink>
        </nav>
      </Transition>
    </header>

    <main class="overflow-hidden pt-24">
      <section class="relative fade-in overflow-hidden px-6 pb-16 pt-20 sm:px-8 lg:px-10">
        <div class="mx-auto grid max-w-7xl gap-16 lg:grid-cols-[1.1fr_minmax(360px,0.9fr)] lg:items-center">
          <div class="space-y-8">
            <span class="inline-flex items-center gap-2 rounded-full border border-[#135bec]/15 bg-white/80 px-4 py-2 text-sm font-medium text-[#135bec] shadow-sm shadow-[#135bec]/5">Digital Concierge para limpieza profesional</span>
            <h1 class="max-w-3xl text-4xl font-semibold tracking-tight text-slate-950 sm:text-5xl lg:text-6xl">Tu hogar impecable, sin mover un dedo</h1>
            <p class="max-w-2xl text-base leading-8 text-slate-700 sm:text-lg">Conecta con profesionales de limpieza verificados, reserva en segundos y disfruta de una experiencia segura y confiable para cada visita a tu hogar.</p>
            <div class="flex flex-col gap-4 sm:flex-row">
              <NuxtLink to="/signup" class="inline-flex items-center justify-center rounded-2xl bg-[#135bec] px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-[#135bec]/20 transition duration-300 hover:-translate-y-0.5 hover:bg-[#0f4ed2]">Quiero contratar</NuxtLink>
              <NuxtLink to="/signup" class="inline-flex items-center justify-center rounded-2xl border border-slate-300 bg-white px-6 py-3 text-sm font-semibold text-slate-950 transition duration-300 hover:border-slate-400 hover:bg-slate-50">Quiero trabajar</NuxtLink>
            </div>
            <div class="grid gap-4 sm:grid-cols-3">
              <div class="rounded-2xl border border-white/70 bg-white/85 px-5 py-4 shadow-sm shadow-slate-200/50">
                <p class="text-sm font-semibold text-slate-950">Profesionales Verificados</p>
                <p class="mt-2 text-sm text-slate-600">Cada limpiador revisado para tu tranquilidad.</p>
              </div>
              <div class="rounded-2xl border border-white/70 bg-white/85 px-5 py-4 shadow-sm shadow-slate-200/50">
                <p class="text-sm font-semibold text-slate-950">Reserva en Segundos</p>
                <p class="mt-2 text-sm text-slate-600">Agenda limpieza con unos pocos clics.</p>
              </div>
              <div class="rounded-2xl border border-white/70 bg-white/85 px-5 py-4 shadow-sm shadow-slate-200/50">
                <p class="text-sm font-semibold text-slate-950">Seguridad Garantizada</p>
                <p class="mt-2 text-sm text-slate-600">Cobertura y soporte confiable en cada servicio.</p>
              </div>
            </div>
          </div>

          <div class="relative flex justify-center">
            <div class="absolute -right-12 top-10 h-40 w-40 rounded-full bg-[#135bec]/20 blur-3xl"></div>
            <div class="relative max-w-lg overflow-hidden rounded-[2rem] border border-white/80 bg-white/90 p-8 shadow-2xl shadow-slate-500/10">
              <div class="space-y-6">
                <div class="rounded-3xl border border-slate-200 bg-[#f8faff] p-5">
                  <p class="text-sm font-semibold uppercase tracking-[0.2em] text-[#135bec]">Servicio Premium</p>
                  <h2 class="mt-4 text-2xl font-semibold text-slate-950">Limpieza en menos de 24h</h2>
                  <p class="mt-3 text-sm leading-6 text-slate-600">Planes flexibles para hogares, departamentos y oficinas.</p>
                </div>
                <div class="grid gap-4 sm:grid-cols-2">
                  <div class="rounded-3xl border border-slate-200 bg-white px-5 py-4">
                    <p class="text-sm font-semibold text-slate-950">Pickup rápido</p>
                    <p class="mt-2 text-sm text-slate-600">Sin esperas.</p>
                  </div>
                  <div class="rounded-3xl border border-slate-200 bg-white px-5 py-4">
                    <p class="text-sm font-semibold text-slate-950">Pago seguro</p>
                    <p class="mt-2 text-sm text-slate-600">Confianza desde el primer clic.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="servicios" class="fade-in border-t border-slate-200/80 bg-[#f6f6ff] px-6 py-16 sm:px-8 lg:px-10">
        <div class="mx-auto max-w-7xl">
          <div class="mb-12 max-w-2xl">
            <p class="text-sm font-semibold uppercase tracking-[0.24em] text-[#135bec]">Nuestra propuesta</p>
            <h2 class="mt-4 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">Todo el cuidado del hogar con una experiencia digital impecable.</h2>
          </div>
          <div class="grid gap-6 sm:grid-cols-3">
            <div class="rounded-3xl border border-white/80 bg-white p-6 shadow-sm shadow-slate-200/40 transition duration-300 hover:-translate-y-1">
              <div class="flex h-12 w-12 items-center justify-center rounded-2xl bg-[#135bec]/10 text-[#135bec]">
                <span class="material-symbols-outlined text-2xl">verified</span>
              </div>
              <h3 class="mt-5 text-xl font-semibold text-slate-950">Profesionales Verificados</h3>
              <p class="mt-3 text-sm leading-6 text-slate-600">Solo trabajamos con limpiadores seleccionados y con historial comprobado.</p>
            </div>
            <div class="rounded-3xl border border-white/80 bg-white p-6 shadow-sm shadow-slate-200/40 transition duration-300 hover:-translate-y-1">
              <div class="flex h-12 w-12 items-center justify-center rounded-2xl bg-[#135bec]/10 text-[#135bec]">
                <span class="material-symbols-outlined text-2xl">schedule</span>
              </div>
              <h3 class="mt-5 text-xl font-semibold text-slate-950">Reserva en Segundos</h3>
              <p class="mt-3 text-sm leading-6 text-slate-600">Interfaz rápida y amigable para reservar con total tranquilidad.</p>
            </div>
            <div class="rounded-3xl border border-white/80 bg-white p-6 shadow-sm shadow-slate-200/40 transition duration-300 hover:-translate-y-1">
              <div class="flex h-12 w-12 items-center justify-center rounded-2xl bg-[#135bec]/10 text-[#135bec]">
                <span class="material-symbols-outlined text-2xl">shield</span>
              </div>
              <h3 class="mt-5 text-xl font-semibold text-slate-950">Seguridad Garantizada</h3>
              <p class="mt-3 text-sm leading-6 text-slate-600">Pagos protegidos y soporte disponible para cada reserva.</p>
            </div>
          </div>
        </div>
      </section>

      <section id="como-funciona" class="fade-in bg-[#eef2ff] px-6 py-16 sm:px-8 lg:px-10">
        <div class="mx-auto grid max-w-7xl gap-16 lg:grid-cols-2 lg:items-center">
          <div class="space-y-6 rounded-[2rem] border border-white/80 bg-white p-8 shadow-sm shadow-slate-200/40">
            <p class="text-sm font-semibold uppercase tracking-[0.24em] text-[#135bec]">Para clientes</p>
            <h2 class="text-3xl font-semibold text-slate-950 sm:text-4xl">Encuentra el servicio ideal para tu hogar</h2>
            <p class="text-sm leading-7 text-slate-600">Explora perfiles de limpiadores certificados, agenda tu visita y recibe reportes claros después de cada jornada.</p>
            <ul class="space-y-4 pt-4 text-sm text-slate-600">
              <li class="flex gap-3"><span class="material-symbols-outlined mt-1 text-[#135bec]">check_circle</span> Reservas fáciles desde cualquier dispositivo.</li>
              <li class="flex gap-3"><span class="material-symbols-outlined mt-1 text-[#135bec]">check_circle</span> Seguimiento y comunicación con tu profesional.</li>
              <li class="flex gap-3"><span class="material-symbols-outlined mt-1 text-[#135bec]">check_circle</span> Pagos seguros sin sorpresas.</li>
            </ul>
          </div>

          <div class="space-y-6 rounded-[2rem] border border-white/80 bg-[#135bec] p-8 text-white shadow-sm shadow-[#0e3c9f]/30">
            <p class="text-sm font-semibold uppercase tracking-[0.24em] text-[#c7d9ff]">Para limpiadores</p>
            <h2 class="text-3xl font-semibold sm:text-4xl">Trabaja con flexibilidad y confianza</h2>
            <p class="text-sm leading-7 text-slate-100">Recibe solicitudes verificadas, gestiona tu disponibilidad y cobra con un proceso simple y transparente.</p>
            <ul class="space-y-4 pt-4 text-sm text-slate-100">
              <li class="flex gap-3"><span class="material-symbols-outlined mt-1">check_circle</span> Pagos claros y comisiones justas.</li>
              <li class="flex gap-3"><span class="material-symbols-outlined mt-1">check_circle</span> Agenda tu horario y acepta trabajos que encajen contigo.</li>
              <li class="flex gap-3"><span class="material-symbols-outlined mt-1">check_circle</span> Soporte dedicado para tu perfil.</li>
            </ul>
          </div>
        </div>
      </section>
    </main>

    <footer class="fade-in border-t border-slate-800/10 bg-[#060e20] px-6 py-10 text-slate-200 sm:px-8 lg:px-10">
      <div class="mx-auto flex max-w-7xl flex-col gap-8 md:flex-row md:items-center md:justify-between">
        <div>
          <p class="text-lg font-semibold text-white">Hogar Limpio</p>
          <p class="mt-3 max-w-xl text-sm text-slate-300">Plataforma de conexión entre hogares y profesionales de limpieza con una experiencia digital moderna y segura.</p>
        </div>
        <div class="flex flex-wrap items-center gap-4 text-sm text-slate-300">
          <a href="#" class="transition hover:text-white">Términos</a>
          <a href="#" class="transition hover:text-white">Privacidad</a>
          <a href="#" class="transition hover:text-white">Contacto</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
const mobileMenuOpen = ref(false)
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(18px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fadeIn 0.8s ease-out forwards;
}

@media (max-width: 640px) {
  header {
    backdrop-filter: blur(18px);
  }
}
</style>
