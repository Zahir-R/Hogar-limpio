<template>
  <div class="flex h-screen overflow-hidden bg-gray-50 font-sans">
    <aside class="w-64 bg-white border-r border-gray-200 hidden md:flex flex-col">
      <div class="p-6 flex items-center gap-3">
        <div class="w-8 h-8 bg-[#135bec] rounded-lg flex items-center justify-center text-white font-bold">H</div>
        <span class="font-bold text-xl tracking-tight">HogarLimpio</span>
      </div>
      <nav class="flex-1 px-4 space-y-1">
        <a class="flex items-center gap-3 px-3 py-2 text-sm font-medium bg-blue-50 text-[#135bec] rounded-lg" href="#">
          <span class="material-symbols-outlined">group</span> Usuarios
        </a>
      </nav>
    </aside>

    <main class="flex-1 flex flex-col min-w-0 overflow-hidden">
      <header class="bg-white border-b border-gray-200 h-16 flex items-center justify-between px-6">
        <div class="max-w-md w-full">
          <input class="w-full pl-4 pr-3 py-2 border border-gray-200 rounded-lg bg-gray-50 text-sm" placeholder="Buscar usuarios..." type="text"/>
        </div>
        <div class="flex items-center gap-3">
          <span class="text-sm font-semibold">Brayan (Admin)</span>
          <div class="w-8 h-8 bg-gray-200 rounded-full text-center leading-8 text-xs font-bold">B</div>
        </div>
      </header>

      <div class="flex-1 overflow-y-auto p-6">
        <div class="flex justify-between items-center mb-8">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Gestión de Usuarios</h1>
            <p class="text-sm text-gray-500">Administra cuentas de clientes y colaboradores.</p>
          </div>
          <button @click="irARegistro" class="px-4 py-2 bg-[#135bec] text-white rounded-lg text-sm font-medium hover:bg-[#0f4abf]">
            + Adicionar Usuario
          </button>
        </div>

        <div class="bg-white shadow-sm border border-gray-200 rounded-lg overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Usuario</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rol</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Acciones</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="user in usuarios" :key="user.uid">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold">
                      {{ user.displayName?.charAt(0).toUpperCase() || 'U' }}
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900">{{ user.displayName || 'Sin nombre' }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ user.email }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {{ user.role }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button @click="modificarUsuario(user)" class="text-[#135bec] hover:underline mr-3">Editar</button>
                  <button @click="eliminarUsuario(user.uid)" class="text-red-600 hover:underline">Eliminar</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-if="mostrarModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-md overflow-hidden border border-slate-200">
          <header class="bg-slate-50 px-6 py-4 border-b border-slate-100">
            <h3 class="font-bold text-lg text-slate-800">Editar Usuario</h3>
            <p class="text-xs text-slate-500">{{ usuarioAEditar.email }}</p>
          </header>
          
          <div class="p-6 space-y-4">
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Nombre Completo</label>
              <input v-model="usuarioAEditar.displayName" class="w-full border border-slate-200 rounded-lg p-2 text-sm focus:ring-blue-500 focus:border-blue-500" type="text" />
            </div>
            
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Asignar Rol</label>
              <select v-model="usuarioAEditar.role" class="w-full border border-slate-200 rounded-lg p-2 text-sm focus:ring-blue-500">
                <option value="admin">Administrador</option>
                <option value="cliente">Cliente</option>
                <option value="personal_limpieza">Personal de Limpieza</option>
              </select>
            </div>
          </div>

          <footer class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
            <button @click="mostrarModal = false" class="px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 rounded-lg">
              Cancelar
            </button>
            <button @click="guardarCambios" class="px-6 py-2 text-sm font-bold text-white bg-[#135bec] hover:bg-[#0f4abf] rounded-lg shadow-md">
              Guardar Cambios
            </button>
          </footer>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const usuarios = ref([]);
const mostrarModal = ref(false);
const usuarioAEditar = ref({ uid: '', displayName: '', role: '' });

const cargarUsuarios = async () => {
  try {
    const response = await $fetch('http://localhost:8000/admin/users', {
      method: 'GET',
      headers: { 
        'Authorization': `Bearer ${localStorage.getItem('auth_token') || ''}` 
      }
    });
    usuarios.value = response;
  } catch (e) {
    console.error("Error al conectar con FastAPI:", e);
  }
};

const eliminarUsuario = async (uid) => {
  if (confirm("¿Estás seguro de eliminar este usuario?")) {
    try {
      await $fetch(`http://localhost:8000/admin/users/${uid}`, { 
        method: 'DELETE' 
      });
      usuarios.value = usuarios.value.filter(u => u.uid !== uid);
      alert("Usuario eliminado con éxito");
    } catch (e) {
      console.error(e);
      alert("Error al eliminar");
    }
  }
};

const modificarUsuario = (user) => {
  usuarioAEditar.value = { ...user }; 
  mostrarModal.value = true;
};

const guardarCambios = async () => {
  const token = localStorage.getItem('auth_token');

  try {
    // Enviamos el nuevo nombre (displayName) y el nuevo rol
    await $fetch(`http://localhost:8000/admin/users/${usuarioAEditar.value.uid}/update`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: { 
        new_name: usuarioAEditar.value.displayName, // El nuevo nombre "Jose"
        new_role: usuarioAEditar.value.role 
      }
    });
    
    alert("¡Usuario actualizado con éxito!");
    mostrarModal.value = false;
    await cargarUsuarios(); // Esto refrescará la tabla y ahora dirá Jose
    
  } catch (e) {
    console.error("Error al guardar:", e.data);
    alert("Error al actualizar: " + (e.data?.detail || "Error de red"));
  }
};

const irARegistro = () => {
  navigateTo('/signup');
};

onMounted(cargarUsuarios);
</script>