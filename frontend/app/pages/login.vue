<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-50 p-4">
    <div class="w-full max-w-md space-y-8 rounded-xl bg-white p-8 shadow-lg">
      <h2 class="text-center text-3xl font-bold text-gray-900">Iniciar Sesión</h2>
      
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input 
            v-model="email" 
            type="email" 
            placeholder="tu@email.com" 
            class="w-full rounded-lg border p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
            required 
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
          <input 
            v-model="password" 
            type="password" 
            placeholder="••••••••" 
            class="w-full rounded-lg border p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500" 
            required 
          />
        </div>

        <button 
          type="submit" 
          class="w-full rounded-lg bg-blue-600 p-3 text-white font-semibold hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed"
          :disabled="loading"
        >
          {{ loading ? 'Iniciando...' : 'Iniciar Sesión' }}
        </button>
      </form>
      
      <p class="text-center text-sm text-gray-600">
        ¿No tienes cuenta? 
        <NuxtLink to="/signup" class="text-blue-600 hover:underline">
          Regístrate
        </NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { getAuth } from "firebase/auth"; // Añadimos esto

const { login } = useAuth()
const router = useRouter()

const email = ref('')
const password = ref('')
const loading = ref(false)

const handleLogin = async () => {
  loading.value = true
  try {
    const result = await login(email.value, password.value)
    
    if (!result) throw new Error('Login failed')

    // --- ESTO ES LO QUE ARREGLA TU PROBLEMA ---
    const auth = getAuth();
    const user = auth.currentUser;
    if (user) {
      const token = await user.getIdToken();
      localStorage.setItem('auth_token', token); // Guardamos la "llave"
      console.log("Token guardado correctamente en LocalStorage");
    }
    // -----------------------------------------

    // Redirección según el rol
    if (result.role === 'admin') {
      await router.push('/admin/dashboard')
    } else if (result.role === 'personal_limpieza') {
      await router.push('/cleaner-dashboard')
    } else {
      await router.push('/client-dashboard')
    }
  } catch (err: any) {
    console.error('Login error:', err)
    alert(err.message || 'Error al iniciar sesión')
  } finally {
    loading.value = false
  }
}
</script>