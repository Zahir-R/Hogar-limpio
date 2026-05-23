<template>
  <div class="bg-[#f6f6ff] text-[#272e42] min-h-screen font-body">
    <aside class="fixed left-0 top-0 bottom-0 z-50 flex flex-col h-screen w-72 bg-[#060e20] shadow-lg hidden lg:flex">
      <div class="p-8">
        <h1 class="text-2xl font-bold tracking-tight text-white font-manrope">Hogar Limpio</h1>
        <p class="text-slate-400 text-xs mt-1 font-medium tracking-widest uppercase">Panel de Servicios</p>
      </div>
      <nav class="flex-1 mt-4 space-y-1">
        <a class="bg-[#0056D2] text-white rounded-lg mx-4 py-3 px-4 shadow-lg flex items-center gap-3" href="#servicios">
          <span class="material-symbols-outlined">inventory_2</span>
          <span class="font-medium">Mis Servicios</span>
        </a>
      </nav>
    </aside>

    <div class="lg:pl-72 flex flex-col min-h-screen">
      <header class="w-full h-20 sticky top-0 bg-white/80 backdrop-blur-xl flex justify-between items-center px-12 z-40">
        <div class="flex items-center flex-1 max-w-xl">
          <div class="relative w-full">
            <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">search</span>
            <input class="w-full bg-gray-100 border-none rounded-full py-2.5 pl-12 pr-4" placeholder="Buscar servicios..." type="text" disabled />
          </div>
        </div>
        <div class="flex items-center gap-3 pl-6">
          <div class="text-right">
            <p class="text-sm font-bold">{{ nombreTrabajador }}</p>
            <p class="text-xs text-gray-500">Personal de Limpieza</p>
          </div>
          <div class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold">{{ avatarInicial }}</div>
        </div>
      </header>

      <main class="p-8 lg:p-12 space-y-10">
        <section class="flex flex-col md:flex-row justify-between items-start gap-6">
          <div>
            <h2 class="text-4xl font-extrabold tracking-tight font-manrope">Hola, {{ nombreTrabajador }}</h2>
            <p class="text-gray-500 mt-2 text-lg">Administra tus servicios y controla su estado de aprobación.</p>
          </div>
          <button @click="abrirModalCrear" class="px-5 py-3 rounded-full bg-[#0056D2] text-white font-semibold hover:bg-[#004bb2] shadow-lg">
            + Crear Servicio
          </button>
        </section>

        <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div class="rounded-3xl bg-white shadow-sm p-6 border border-gray-100">
            <p class="text-sm text-gray-500 uppercase tracking-[0.2em]">Servicios</p>
            <p class="mt-4 text-3xl font-bold">{{ servicios.length }}</p>
            <p class="mt-2 text-sm text-gray-500">Servicios registrados por ti.</p>
          </div>
          <div class="rounded-3xl bg-white shadow-sm p-6 border border-gray-100">
            <p class="text-sm text-gray-500 uppercase tracking-[0.2em]">Aprobados</p>
            <p class="mt-4 text-3xl font-bold">{{ servicios.filter(s => s.estado === 'Aprobado').length }}</p>
            <p class="mt-2 text-sm text-gray-500">Servicios listos para publicarse.</p>
          </div>
          <div class="rounded-3xl bg-white shadow-sm p-6 border border-gray-100">
            <p class="text-sm text-gray-500 uppercase tracking-[0.2em]">Pendientes</p>
            <p class="mt-4 text-3xl font-bold">{{ servicios.filter(s => s.estado === 'Pendiente').length }}</p>
            <p class="mt-2 text-sm text-gray-500">Esperando validación administrativa.</p>
          </div>
        </section>

        <section class="bg-white rounded-3xl shadow-sm border border-gray-100 p-6">
          <div class="flex items-center justify-between mb-6">
            <div>
              <h3 class="text-xl font-bold">Mis Servicios</h3>
              <p class="text-sm text-gray-500">Edita, elimina o revisa el estado de tus servicios.</p>
            </div>
            <span class="text-sm text-gray-400">Última actualización automática</span>
          </div>

          <div class="space-y-4">
            <div v-if="!servicios.length" class="rounded-2xl border border-dashed border-gray-200 p-10 text-center text-gray-500">
              No tienes servicios registrados aún. Crea uno nuevo para comenzar.
            </div>
            <div v-for="servicio in servicios" :key="servicio.id" class="rounded-3xl border border-gray-200 p-5 hover:shadow-lg transition-shadow">
              <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
                <div>
                  <h4 class="text-lg font-bold">{{ servicio.titulo }}</h4>
                  <p class="text-sm text-gray-500 mt-2">{{ servicio.descripcion }}</p>
                </div>
                <span :class="badgeClass(servicio.estado)" class="text-xs font-semibold uppercase px-3 py-1 rounded-full">
                  {{ servicio.estado }}
                </span>
              </div>
              <div class="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm text-gray-600">
                <p><strong>Categoría:</strong> {{ servicio.categoria }}</p>
                <p><strong>Precio:</strong> {{ formatPrice(servicio.precio) }}</p>
              </div>
              <div class="mt-5 flex flex-wrap gap-2">
                <button @click="abrirModalEditar(servicio)" class="px-4 py-2 rounded-full bg-[#0056D2] text-white text-sm hover:bg-[#0046ab]">Editar</button>
                <button @click="eliminarServicio(servicio.id)" class="px-4 py-2 rounded-full bg-red-600 text-white text-sm hover:bg-red-700">Eliminar</button>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>

    <div v-if="mostrarModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-2xl overflow-hidden border border-slate-200">
        <header class="flex items-center justify-between px-8 py-5 border-b border-slate-100">
          <div>
            <h3 class="text-xl font-bold">{{ isEditMode ? 'Editar Servicio' : 'Crear Servicio' }}</h3>
            <p class="text-sm text-gray-500">Usa este formulario para administrar tus servicios.</p>
          </div>
          <button @click="cerrarModal" class="text-gray-500 hover:text-gray-800">Cerrar</button>
        </header>

        <div class="p-8 space-y-5">
          <div class="grid grid-cols-1 gap-5">
            <label class="space-y-2 text-sm font-medium text-slate-700">
              Título del servicio
              <input v-model="form.titulo" type="text" class="w-full rounded-2xl border border-gray-200 p-3 text-sm focus:ring-2 focus:ring-blue-200" />
            </label>
            <label class="space-y-2 text-sm font-medium text-slate-700">
              Descripción
              <textarea v-model="form.descripcion" rows="4" class="w-full rounded-2xl border border-gray-200 p-3 text-sm focus:ring-2 focus:ring-blue-200"></textarea>
            </label>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
              <label class="space-y-2 text-sm font-medium text-slate-700">
                Precio
                <input v-model.number="form.precio" type="number" min="0" class="w-full rounded-2xl border border-gray-200 p-3 text-sm focus:ring-2 focus:ring-blue-200" />
              </label>
              <label class="space-y-2 text-sm font-medium text-slate-700">
                Categoría
                <input v-model="form.categoria" type="text" class="w-full rounded-2xl border border-gray-200 p-3 text-sm focus:ring-2 focus:ring-blue-200" />
              </label>
            </div>
          </div>
        </div>

        <footer class="px-8 py-5 bg-slate-50 border-t border-slate-100 flex flex-col sm:flex-row gap-3 justify-end">
          <button @click="cerrarModal" class="px-5 py-3 text-sm font-medium rounded-full border border-gray-200 text-slate-700 hover:bg-gray-50">Cancelar</button>
          <button @click="guardarServicio" class="px-5 py-3 text-sm font-bold rounded-full bg-[#0056D2] text-white hover:bg-[#004bb2]">{{ isEditMode ? 'Actualizar Servicio' : 'Crear Servicio' }}</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
const auth = useAuth();

const servicios = ref([]);
const mostrarModal = ref(false);
const isEditMode = ref(false);
const selectedServiceId = ref(null);
const form = ref({
  titulo: '',
  descripcion: '',
  precio: 0,
  categoria: '',
  ofertante_id: ''
});

const nombreTrabajador = computed(() => {
  return auth.user.value?.displayName || auth.user.value?.email?.split('@')[0] || 'Trabajador';
});

const avatarInicial = computed(() => {
  return (auth.user.value?.displayName || auth.user.value?.email || 'T')[0].toUpperCase();
});

const badgeClass = (estado) => {
  if (estado === 'Aprobado') return 'bg-emerald-100 text-emerald-700';
  if (estado === 'Rechazado') return 'bg-red-100 text-red-700';
  return 'bg-yellow-100 text-yellow-700';
};

const formatPrice = (value) => {
  return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' }).format(value || 0);
};

const cargarServicios = async () => {
  try {
    const token = await auth.getToken(true);
    servicios.value = await $fetch('http://localhost:8000/api/servicios/mis-servicios', {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` }
    });
  } catch (error) {
    console.error('Error cargando servicios:', error);
    servicios.value = [];
  }
};

const abrirModalCrear = () => {
  isEditMode.value = false;
  selectedServiceId.value = null;
  form.value = {
    titulo: '',
    descripcion: '',
    precio: 0,
    categoria: '',
    ofertante_id: auth.user.value?.uid || ''
  };
  mostrarModal.value = true;
};

const abrirModalEditar = (servicio) => {
  isEditMode.value = true;
  selectedServiceId.value = servicio.id;
  form.value = {
    titulo: servicio.titulo,
    descripcion: servicio.descripcion,
    precio: servicio.precio,
    categoria: servicio.categoria,
    ofertante_id: servicio.ofertante_id
  };
  mostrarModal.value = true;
};

const cerrarModal = () => {
  mostrarModal.value = false;
};

const guardarServicio = async () => {
  try {
    const token = await auth.getToken(true);
    if (!token) throw new Error('No se pudo obtener el token de autenticación.');

    if (isEditMode.value && selectedServiceId.value) {
      await $fetch(`http://localhost:8000/api/servicios/${selectedServiceId.value}`, {
        method: 'PUT',
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: {
          titulo: form.value.titulo,
          descripcion: form.value.descripcion,
          precio: form.value.precio,
          categoria: form.value.categoria
        }
      });
      alert('Servicio actualizado correctamente.');
    } else {
      await $fetch('http://localhost:8000/api/servicios/registrar', {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: {
          titulo: form.value.titulo,
          descripcion: form.value.descripcion,
          precio: form.value.precio,
          categoria: form.value.categoria,
          ofertante_id: auth.user.value?.uid || ''
        }
      });
      alert('Servicio creado y enviado para validación.');
    }

    cerrarModal();
    await cargarServicios();
  } catch (error) {
    console.error('Error guardando servicio:', error);
    alert('Error al guardar el servicio. Revisa los datos e intenta de nuevo.');
  }
};

const eliminarServicio = async (id) => {
  if (!confirm('¿Deseas eliminar este servicio?')) return;
  try {
    const token = await auth.getToken(true);
    await $fetch(`http://localhost:8000/api/servicios/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    });
    servicios.value = servicios.value.filter((servicio) => servicio.id !== id);
    alert('Servicio eliminado correctamente.');
  } catch (error) {
    console.error('Error eliminando servicio:', error);
    alert('No se pudo eliminar el servicio.');
  }
};

onMounted(cargarServicios);
</script>
