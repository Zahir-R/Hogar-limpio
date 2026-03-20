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
          <span class="font-medium">Panel de Control</span>
        </a>
        <a class="text-slate-400 hover:text-white hover:bg-white/5 rounded-lg mx-4 py-3 px-4 transition-all flex items-center gap-3" href="#">
          <span class="material-symbols-outlined">cleaning_services</span>
          <span class="font-medium">Limpieza</span>
        </a>
      </nav>
      <div class="p-6">
        <button class="w-full bg-gradient-to-r from-[#0053cc] to-[#779dff] text-white py-4 rounded-xl font-bold flex items-center justify-center gap-2 shadow-lg">
          <span class="material-symbols-outlined">add</span> Nueva Solicitud
        </button>
      </div>
    </aside>

    <main class="flex-1 lg:pl-72 min-h-screen relative">
      <header class="w-full h-20 sticky top-0 flex justify-between items-center px-12 bg-white/80 backdrop-blur-xl z-40">
        <div class="flex-1 max-w-xl">
          <div class="relative group">
            <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">search</span>
            <input class="w-full pl-12 pr-4 py-3 bg-gray-100 border-none rounded-full focus:ring-2 focus:ring-blue-500/20 text-gray-700" placeholder="Buscar especialistas..." type="text"/>
          </div>
        </div>
        <div class="flex items-center gap-6 ml-8">
          <div class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold">S</div>
        </div>
      </header>

      <div class="px-12 py-10 space-y-12">
        <section class="flex justify-between items-end">
          <div>
            <h2 class="text-4xl font-extrabold text-[#272e42] font-manrope tracking-tight"> Hola, {{ nombreUsuario }}</h2>
            <p class="text-gray-500 mt-2 text-lg">Tu hogar está en excelentes manos hoy.</p>
          </div>
          <div class="text-right">
            <span class="text-xs font-bold text-gray-400 uppercase tracking-widest block">Saldo Disponible</span>
            <span class="text-2xl font-bold text-[#0053cc]">$420.00</span>
          </div>
        </section>

        <div class="grid grid-cols-12 gap-8">
          <div class="col-span-12 lg:col-span-8 space-y-6">
            <h3 class="text-sm font-bold text-gray-400 uppercase tracking-widest">Trabajadores Disponibles</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div v-for="t in trabajadores" :key="t.id" class="bg-white p-5 rounded-xl shadow-sm border border-transparent hover:border-blue-500/20 transition-all">
                <div class="flex items-start justify-between">
                  <div class="flex gap-4">
                    <div class="w-14 h-14 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold text-xl">
                      {{ t.nombre.charAt(0) }}
                    </div>
                    <div>
                      <h4 class="font-bold text-[#272e42]">{{ t.nombre }}</h4>
                      <div class="flex items-center gap-1 text-orange-500">
                        <span class="material-symbols-outlined text-sm">star</span>
                        <span class="text-xs font-bold">{{ t.calificacion }}</span>
                      </div>
                    </div>
                  </div>
                  <div class="text-right">
                    <span class="text-lg font-bold text-[#0053cc]">${{ t.precio }}</span>
                  </div>
                </div>
                <p class="text-gray-500 text-sm mt-4">Especialista en zona {{ t.zona }}.</p>
                <button @click="agendar(t.nombre)" class="w-full mt-5 bg-gray-100 text-[#0053cc] py-3 rounded-lg font-bold hover:bg-[#0053cc] hover:text-white transition-all">
                  Agendar
                </button>
              </div>
            </div>
          </div>

          <div class="col-span-12 lg:col-span-4">
            <div class="bg-white rounded-2xl p-8 shadow-sm space-y-6">
              <h3 class="text-lg font-bold">Realizar Pago</h3>
              <div class="space-y-4">
                <input class="w-full bg-gray-50 border-none rounded-xl py-4 px-4 font-semibold" type="text" value="**** **** **** 4590"/>
                <button class="w-full bg-gradient-to-r from-[#0053cc] to-[#779dff] text-white py-4 rounded-xl font-bold shadow-lg">
                  Confirmar Pago $45.00
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
// 1. Usamos el composable de autenticación que ya tienen (useAuth.ts)
const auth = useAuth(); 

// 2. Creamos el nombre reactivo
// Si el usuario está logueado, traerá su nombre. Si no, dirá "Mario" por ahora.
const nombreUsuario = computed(() => {
  return auth.user.value?.displayName || "Mario";
});

// 3. Traemos los trabajadores (Esto podrías traerlo de tu API de Python luego)
const trabajadores = [
  {id: "1", nombre: "Juan Perez", precio: 50.0, calificacion: 4.8, zona: "Norte"},
  {id: "2", nombre: "Maria Lopez", precio: 45.0, calificacion: 4.9, zona: "Sur"}
];

// 4. Configurar iconos y fuentes
useHead({
  link: [
    { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined' }
  ]
})
</script>