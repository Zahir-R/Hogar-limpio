<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-50 p-4">
    <div class="w-full max-w-md space-y-8 rounded-xl bg-white p-8 shadow-lg">
      <h2 class="text-center text-3xl font-bold text-gray-900">Crear Cuenta</h2>
      <form @submit.prevent="handleSignup" class="space-y-6">
        <input v-model="email" type="email" placeholder="Email" class="w-full rounded-lg border p-3" required />
        <input v-model="password" type="password" placeholder="Contraseña" class="w-full rounded-lg border p-3" required />
        <button type="submit" class="w-full rounded-lg bg-blue-600 p-3 text-white font-semibold hover:bg-blue-700">
          Registrarse
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
const { signup } = useAuth()
const email = ref('')
const password = ref('')

const handleSignup = async () => {
  try {
    await signup(email.value, password.value)
    navigateTo('/login')
  } catch (err) {
    alert(err.message)
  }
}
</script>