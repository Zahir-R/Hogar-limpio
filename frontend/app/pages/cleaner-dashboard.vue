<template>
  <div class="bg-[#f6f6ff] text-[#272e42] min-h-screen font-body">
    <aside class="fixed left-0 top-0 bottom-0 z-50 flex flex-col h-screen w-72 bg-[#060e20] shadow-lg hidden lg:flex">
      <div class="p-8">
        <h1 class="text-2xl font-bold tracking-tight text-white font-manrope">Hogar Limpio</h1>
        <p class="text-slate-400 text-xs mt-1 font-medium tracking-widest uppercase">Digital Concierge</p>
      </div>
      <nav class="flex-1 mt-4 space-y-1">
        <a class="bg-[#0056D2] text-white rounded-lg mx-4 py-3 px-4 shadow-lg flex items-center gap-3" href="#">
          <span class="material-symbols-outlined">dashboard</span>
          <span class="font-medium">Panel de Control</span>
        </a>
        </nav>
    </aside>

    <div class="lg:pl-72 flex flex-col min-h-screen">
      <header class="w-full h-20 sticky top-0 bg-white/80 backdrop-blur-xl flex justify-between items-center px-12 z-40">
        <div class="flex items-center flex-1 max-w-xl">
          <div class="relative w-full">
            <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">search</span>
            <input class="w-full bg-gray-100 border-none rounded-full py-2.5 pl-12 pr-4" placeholder="Buscar servicios..." type="text"/>
          </div>
        </div>
        <div class="flex items-center gap-3 pl-6">
          <div class="text-right">
            <p class="text-sm font-bold">{{ nombreUsuario }}</p>
            <p class="text-xs text-gray-500">Especialista Senior</p>
          </div>
          <div class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold">B</div>
        </div>
      </header>

      <main class="p-8 lg:p-12 space-y-12">
        <section class="flex flex-col md:flex-row justify-between items-start gap-6">
          <div>
            <h2 class="text-4xl font-extrabold tracking-tight font-manrope">¡Buen día, {{ nombreUsuario }}!</h2>
            <p class="text-gray-500 mt-2 text-lg">Tienes {{ trabajosHoy.length }} limpiezas programadas para hoy.</p>
          </div>
          <div class="flex items-center gap-4 bg-white p-2 pr-6 rounded-full shadow-sm border border-gray-100">
            <div class="flex items-center gap-2 px-4 py-2 bg-green-100 text-green-700 rounded-full">
              <div class="w-2.5 h-2.5 bg-green-500 rounded-full animate-ping"></div>
              <span class="text-sm font-bold">Disponible</span>
            </div>
          </div>
        </section>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div class="lg:col-span-8 space-y-8">
            <div class="bg-white rounded-xl p-8 shadow-sm">
              <h3 class="text-xl font-bold font-manrope mb-6">Trabajos de hoy</h3>
              <div class="space-y-6">
                <div v-for="job in trabajosHoy" :key="job.id" class="flex items-start gap-6 p-6 rounded-xl hover:bg-gray-50 transition-colors border-l-4 border-blue-500">
                  <div class="min-w-[60px] text-center">
                    <span class="text-2xl font-bold">{{ job.hora }}</span>
                  </div>
                  <div class="flex-1">
                    <h4 class="font-bold text-lg">{{ job.tipo }}</h4>
                    <p class="text-sm text-gray-500">{{ job.direccion }}</p>
                  </div>
                  <button @click="confirmar(job.id)" class="bg-green-600 text-white px-6 py-2.5 rounded-lg font-bold text-sm">Finalizar</button>
                </div>
              </div>
            </div>
          </div>

          <div class="lg:col-span-4 space-y-8">
            <div class="bg-[#060e20] text-white rounded-xl p-8 shadow-xl">
              <h3 class="text-slate-400 text-sm font-bold uppercase mb-2">Mis Ganancias</h3>
              <p class="text-4xl font-extrabold">$1,240.50</p>
              <button class="mt-8 w-full border border-white/20 py-3 rounded-lg text-sm font-bold">Ver detalle</button>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
const auth = useAuth();

// Detectar tu nombre real (Brayan)
const nombreUsuario = computed(() => {
  return auth.user.value?.displayName || "Brayan";
});

const trabajosHoy = [
  { id: 1, hora: "09:00", tipo: "Limpieza Profunda", direccion: "Calle de la Luna, 45", cliente: "Elena R." },
  { id: 2, hora: "14:30", tipo: "Mantenimiento Oficina", direccion: "Av. Central 890", cliente: "TechSolutions" }
];

const confirmar = (id) => {
  alert(`Trabajo ${id} marcado como finalizado. ¡Buen trabajo!`);
};

useHead({
  link: [
    { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined' },
    { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Manrope:wght@400;700;800&family=Inter:wght@400;600&display=swap' }
  ]
})
</script>