<template>
  <main class="max-w-4xl mx-auto p-4 md:p-8 font-sans">
    <nav class="mb-6 flex items-center text-sm text-gray-500">
      <NuxtLink to="/" class="hover:text-[#135bec] transition-colors">Inicio</NuxtLink>
      <span class="mx-2 text-gray-400">/</span>
      <span class="font-medium text-gray-900">Registro de Usuario</span>
    </nav>

    <section class="bg-white shadow-sm border border-gray-200 rounded-[8px] overflow-hidden">
      <header class="px-6 py-4 border-b border-gray-100 bg-gray-50/50">
        <h1 class="text-xl font-semibold text-gray-800">Detalles del Usuario</h1>
        <p class="text-sm text-gray-500 mt-1">Complete la información para crear su cuenta en Hogar Limpio.</p>
      </header>

      <form @submit.prevent="handleSignup" class="p-6 md:p-8 space-y-8">
        <div class="flex flex-col items-center md:flex-row md:items-start gap-6">
          <div class="w-32 h-32 rounded-full bg-gray-100 border-2 border-dashed border-gray-300 flex items-center justify-center overflow-hidden">
            <span class="material-symbols-outlined text-4xl text-gray-400">person</span>
          </div>
          <div class="flex-1 space-y-1 pt-2">
            <h3 class="text-sm font-medium text-gray-700">Foto de Perfil</h3>
            <p class="text-xs text-gray-500">JPG, PNG. Máximo 2MB.</p>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-6">
          <div class="space-y-1">
            <label class="block text-sm font-medium text-gray-700">Nombre Completo</label>
            <input v-model="displayName" type="text" placeholder="Ej: Mario Pérez" class="block w-full rounded-[8px] border-gray-300 shadow-sm focus:ring-[#135bec] focus:border-[#135bec] sm:text-sm" required />
          </div>

          <div class="space-y-1">
            <label class="block text-sm font-medium text-gray-700">Correo Electrónico</label>
            <input v-model="email" type="email" placeholder="correo@ejemplo.com" class="block w-full rounded-[8px] border-gray-300 shadow-sm focus:ring-[#135bec] focus:border-[#135bec] sm:text-sm" required />
          </div>

          <div class="space-y-1">
            <label class="block text-sm font-medium text-gray-700">Contraseña</label>
            <input v-model="password" type="password" placeholder="••••••••" class="block w-full rounded-[8px] border-gray-300 shadow-sm focus:ring-[#135bec] focus:border-[#135bec] sm:text-sm" required />
            <p class="text-[10px] text-gray-400">Mínimo 8 caracteres.</p>
          </div>

          <div class="space-y-1">
            <label class="block text-sm font-medium text-gray-700">¿Qué eres?</label>
            <select v-model="role" class="block w-full rounded-[8px] border-gray-300 shadow-sm focus:ring-[#135bec] focus:border-[#135bec] sm:text-sm">
              <option value="cliente">Cliente (Busco limpieza)</option>
              <option value="personal_limpieza">Trabajador (Ofrezco limpieza)</option>
            </select>
          </div>
        </div>

        <div class="pt-6 border-t border-gray-100 flex items-center justify-end gap-3">
          <button type="button" @click="$router.push('/')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-[8px] hover:bg-gray-50">
            Cancelar
          </button>
          <button type="submit" class="bg-[#135bec] hover:bg-[#0f48ba] px-6 py-2 text-sm font-medium text-white rounded-[8px] shadow-sm transition-all">
            Crear Cuenta
          </button>
        </div>
      </form>
    </section>
  </main>
</template>

<script setup>
const { signup } = useAuth(); // Usando tu lógica de auth
const displayName = ref('');
const email = ref('');
const password = ref('');
const role = ref('cliente');

const handleSignup = async () => {
  try {
    // Registramos en Firebase con el nombre y el rol elegido
    await signup(email.value, password.value, displayName.value, role.value);
    alert("¡Cuenta creada con éxito!");
  } catch (error) {
    alert("Error al registrar: " + error.message);
  }
};
</script>