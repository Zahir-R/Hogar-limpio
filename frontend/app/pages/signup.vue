<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-50 p-4">
    <div class="w-full max-w-md space-y-8 rounded-xl bg-white p-8 shadow-lg">
      <h2 class="text-center text-3xl font-bold text-gray-900">Crear Cuenta</h2>

      <form @submit.prevent="handleSignup" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nombre Completo</label>
          <input v-model="displayName" type="text" placeholder="Ej: Mario Pérez" class="w-full rounded-lg border p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500" required />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Correo Electrónico</label>
          <input v-model="email" type="email" placeholder="correo@ejemplo.com" class="w-full rounded-lg border p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500" required />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
          <input v-model="password" type="password" placeholder="••••••••" class="w-full rounded-lg border p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500" required />
          <p class="text-xs text-gray-400 mt-1">Mínimo 8 caracteres.</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">¿Qué eres?</label>
          <select v-model="role" class="w-full rounded-lg border p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 appearance-none pr-8" style="background-image:url('data:image/svg+xml;charset=utf-8,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2212%22 height=%2212%22 viewBox=%220 0 24 24%22 fill=%22%23666%22%3E%3Cpath d=%22M7 10l5 5 5-5z%22/%3E%3C/svg%3E');background-repeat:no-repeat;background-position:right 8px center">
            <option value="cliente">Cliente (Busco limpieza)</option>
            <option value="personal_limpieza">Trabajador (Ofrezco limpieza)</option>
          </select>
        </div>

        <button type="submit" class="w-full rounded-lg bg-blue-600 p-3 text-white font-semibold hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed">
          Crear Cuenta
        </button>
      </form>

      <p class="text-center text-sm text-gray-600">
        ¿Ya tienes cuenta?
        <NuxtLink to="/login" class="text-blue-600 hover:underline">Inicia sesión</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
const { signup } = useAuth();
const toast = useToast();
const displayName = ref('');
const email = ref('');
const password = ref('');
const role = ref('cliente');

const router = useRouter();

const handleSignup = async () => {
  try {
    const result = await signup(email.value, password.value, displayName.value, role.value);

    if (result) {
      if (result.role === 'personal_limpieza') {
        router.push('/cleaner/profile');
      } else {
        router.push('/client-dashboard');
      }
    }
  } catch (error) {
    const msg = error?.message || '';
    if (msg.includes('EMAIL_EXISTS') || msg.includes('email-already-in-use')) {
      toast.error('Este correo ya está registrado. Intenta con otro.');
    } else {
      toast.error('Error al registrar: ' + (msg || 'Error desconocido'));
    }
  }
};
</script>
