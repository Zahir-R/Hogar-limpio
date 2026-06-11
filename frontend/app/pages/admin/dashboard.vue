<template>
  <div class="flex h-screen overflow-hidden bg-gray-50 font-sans">
    <aside class="w-64 bg-white border-r border-gray-200 hidden md:flex flex-col">
      <div class="p-6 flex items-center gap-3">
        <div class="w-8 h-8 bg-[#135bec] rounded-lg flex items-center justify-center text-white font-bold">H</div>
        <span class="font-bold text-xl tracking-tight">HogarLimpio</span>
      </div>
      <nav class="flex-1 px-4 space-y-1">
        <button @click="selectedTab = 'usuarios'" :class="selectedTab === 'usuarios' ? 'bg-blue-50 text-[#135bec]' : 'text-gray-600'" class="w-full text-left flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-lg">
          <span class="material-symbols-outlined">group</span> Usuarios
        </button>
        <button @click="selectedTab = 'validacion'" :class="selectedTab === 'validacion' ? 'bg-blue-50 text-[#135bec]' : 'text-gray-600'" class="w-full text-left flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-lg">
          <span class="material-symbols-outlined">gavel</span> Validación de Servicios
        </button>
        <button @click="selectedTab = 'zonas'" :class="selectedTab === 'zonas' ? 'bg-blue-50 text-[#135bec]' : 'text-gray-600'" class="w-full text-left flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-lg">
          <span class="material-symbols-outlined">map</span> Zonas
        </button>
        <button @click="selectedTab = 'precios'" :class="selectedTab === 'precios' ? 'bg-blue-50 text-[#135bec]' : 'text-gray-600'" class="w-full text-left flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-lg">
          <span class="material-symbols-outlined">payments</span> Precios
        </button>
        <button @click="selectedTab = 'reservas'" :class="selectedTab === 'reservas' ? 'bg-blue-50 text-[#135bec]' : 'text-gray-600'" class="w-full text-left flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-lg">
          <span class="material-symbols-outlined">book_online</span> Reservas
        </button>
        <button @click="selectedTab = 'pagos'" :class="selectedTab === 'pagos' ? 'bg-blue-50 text-[#135bec]' : 'text-gray-600'" class="w-full text-left flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-lg">
          <span class="material-symbols-outlined">payments</span> Pagos
        </button>
      </nav>
    </aside>

    <main class="flex-1 flex flex-col min-w-0 overflow-hidden">
      <header class="bg-white border-b border-gray-200 h-16 flex items-center justify-between px-6">
        <div class="max-w-md w-full">
          <input class="w-full pl-4 pr-3 py-2 border border-gray-200 rounded-lg bg-gray-50 text-sm" placeholder="Buscar admin..." type="text" disabled />
        </div>
        <div class="flex items-center gap-3">
          <span class="text-sm font-semibold">Admin</span>
          <div class="w-8 h-8 bg-gray-200 rounded-full text-center leading-8 text-xs font-bold">A</div>
        </div>
      </header>

      <div class="flex-1 overflow-y-auto p-6">
        <div class="flex flex-col gap-6">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 class="text-2xl font-bold text-gray-900">Panel de Administración</h1>
              <p class="text-sm text-gray-500">Controla usuarios, valida servicios, gestiona zonas y precios.</p>
            </div>
          </div>

          <div class="bg-white shadow-sm border border-gray-200 rounded-lg overflow-hidden">
            <div class="border-b border-gray-200 bg-gray-50 px-6 py-4">
              <nav class="flex gap-3 flex-wrap">
                <button @click="selectedTab = 'usuarios'" :class="selectedTab === 'usuarios' ? 'bg-white text-slate-900 shadow-sm' : 'text-gray-500'" class="rounded-full px-4 py-2 text-sm font-semibold">Usuarios</button>
                <button @click="selectedTab = 'validacion'" :class="selectedTab === 'validacion' ? 'bg-white text-slate-900 shadow-sm' : 'text-gray-500'" class="rounded-full px-4 py-2 text-sm font-semibold">Validación de Servicios</button>
                <button @click="selectedTab = 'zonas'" :class="selectedTab === 'zonas' ? 'bg-white text-slate-900 shadow-sm' : 'text-gray-500'" class="rounded-full px-4 py-2 text-sm font-semibold">Zonas</button>
                <button @click="selectedTab = 'precios'" :class="selectedTab === 'precios' ? 'bg-white text-slate-900 shadow-sm' : 'text-gray-500'" class="rounded-full px-4 py-2 text-sm font-semibold">Precios</button>
                <button @click="selectedTab = 'reservas'" :class="selectedTab === 'reservas' ? 'bg-white text-slate-900 shadow-sm' : 'text-gray-500'" class="rounded-full px-4 py-2 text-sm font-semibold">Reservas</button>
                <button @click="selectedTab = 'pagos'" :class="selectedTab === 'pagos' ? 'bg-white text-slate-900 shadow-sm' : 'text-gray-500'" class="rounded-full px-4 py-2 text-sm font-semibold">Pagos</button>
              </nav>
            </div>

            <div class="p-6">
              <!-- USUARIOS TAB -->
              <div v-if="selectedTab === 'usuarios'">
                <div class="flex justify-between items-center mb-6">
                  <div>
                    <h2 class="text-xl font-bold text-gray-900">Gestión de Usuarios</h2>
                    <p class="text-sm text-gray-500">Administra cuentas de clientes y colaboradores.</p>
                  </div>
                  <button @click="irARegistro" class="px-4 py-2 bg-[#135bec] text-white rounded-lg text-sm font-medium hover:bg-[#0f4abf]">+ Añadir Usuario</button>
                </div>
                <div class="overflow-x-auto">
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
                          <div class="flex items-center gap-3">
                             <div class="h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold overflow-hidden">
                               <img v-if="user.profile_photo_url" :src="fotoUrl(user.profile_photo_url)" class="w-full h-full object-cover" />
                               <span v-else>{{ user.displayName?.charAt(0).toUpperCase() || 'U' }}</span>
                             </div>
                            <div>
                              <div class="text-sm font-medium text-gray-900">{{ user.displayName || 'Sin nombre' }}</div>
                            </div>
                          </div>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ user.email }}</td>
                        <td class="px-6 py-4 whitespace-nowrap">
                          <span class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">{{ user.role }}</span>
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

              <!-- VALIDACIÓN TAB -->
              <div v-else-if="selectedTab === 'validacion'" class="space-y-6">
                <div>
                  <h2 class="text-xl font-bold text-gray-900">Validación de Servicios</h2>
                  <p class="text-sm text-gray-500">Revisa y aprueba o rechaza los servicios pendientes.</p>
                </div>
                <div class="overflow-x-auto">
                  <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                      <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Título</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Categoría</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ofertante</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Precio</th>
                        <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Acciones</th>
                      </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                      <tr v-for="servicio in serviciosPendientes" :key="servicio.id">
                        <td class="px-6 py-4 text-sm text-gray-900">{{ servicio.titulo }}</td>
                        <td class="px-6 py-4 text-sm text-gray-500">{{ servicio.categoria }}</td>
                        <td class="px-6 py-4 text-sm text-gray-500">{{ servicio.ofertante_id }}</td>
                        <td class="px-6 py-4 text-sm text-gray-900">{{ formatPrice(servicio.precio) }}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium flex flex-col sm:flex-row sm:justify-end gap-2">
                          <button @click="validarServicio(servicio.id, 'Aprobado')" class="px-3 py-2 rounded-full bg-emerald-600 text-white text-xs hover:bg-emerald-700">Aprobar</button>
                          <button @click="validarServicio(servicio.id, 'Rechazado')" class="px-3 py-2 rounded-full bg-red-600 text-white text-xs hover:bg-red-700">Rechazar</button>
                        </td>
                      </tr>
                      <tr v-if="!serviciosPendientes.length">
                        <td colspan="5" class="px-6 py-10 text-center text-sm text-gray-500">No hay servicios pendientes en este momento.</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- ZONAS TAB -->
              <div v-else-if="selectedTab === 'zonas'" class="space-y-6">
                <div class="flex justify-between items-center">
                  <div>
                    <h2 class="text-xl font-bold text-gray-900">Gestión de Zonas</h2>
                    <p class="text-sm text-gray-500">Administra las zonas de cobertura y recargos.</p>
                  </div>
                  <button @click="abrirModalZona()" class="px-4 py-2 bg-[#135bec] text-white rounded-lg text-sm font-medium hover:bg-[#0f4abf]">+ Añadir Zona</button>
                </div>
                <div class="overflow-x-auto">
                  <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                      <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nombre</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Recargo</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Activo</th>
                        <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Acciones</th>
                      </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                      <tr v-for="zona in zonas" :key="zona.id">
                        <td class="px-6 py-4 text-sm font-medium text-gray-900">{{ zona.nombre }}</td>
                        <td class="px-6 py-4 text-sm text-gray-500">{{ (zona.surcharge * 100) }}%</td>
                        <td class="px-6 py-4">
                          <span :class="zona.active ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-500'" class="px-2.5 py-0.5 rounded-full text-xs font-medium">{{ zona.active ? 'Sí' : 'No' }}</span>
                        </td>
                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                          <button @click="abrirModalZona(zona)" class="text-[#135bec] hover:underline mr-3">Editar</button>
                          <button @click="eliminarZona(zona.id)" v-if="zona.active" class="text-red-600 hover:underline">Desactivar</button>
                        </td>
                      </tr>
                      <tr v-if="!zonas.length">
                        <td colspan="4" class="px-6 py-10 text-center text-sm text-gray-500">No hay zonas registradas.</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- RESERVAS TAB -->
              <div v-else-if="selectedTab === 'reservas'" class="space-y-6">
                <div>
                  <h2 class="text-xl font-bold text-gray-900">Todas las Reservas</h2>
                  <p class="text-sm text-gray-500">Vista general de todas las reservas del sistema.</p>
                </div>
                <div class="overflow-x-auto">
                  <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                      <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cliente</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Trabajador</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                        <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Total</th>
                      </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                      <tr v-for="r in reservas" :key="r.id">
                        <td class="px-6 py-4 text-sm text-gray-500">{{ r.cliente_uid?.slice(0, 8) }}...</td>
                        <td class="px-6 py-4 text-sm text-gray-500">{{ r.worker_uid?.slice(0, 8) }}...</td>
                        <td class="px-6 py-4 text-sm text-gray-900">{{ r.fecha }} {{ r.hora_inicio }}</td>
                        <td class="px-6 py-4">
                          <span :class="badgeClassReserva(r.estado)" class="px-2.5 py-0.5 rounded-full text-xs font-medium">{{ r.estado }}</span>
                        </td>
                        <td class="px-6 py-4 text-right text-sm font-medium">{{ formatPrice(r.precio_total) }}</td>
                      </tr>
                      <tr v-if="!reservas.length">
                        <td colspan="5" class="px-6 py-10 text-center text-sm text-gray-500">No hay reservas registradas.</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- PAGOS TAB -->
              <div v-else-if="selectedTab === 'pagos'" class="space-y-6">
                <div>
                  <h2 class="text-xl font-bold text-gray-900">Pagos</h2>
                  <p class="text-sm text-gray-500">Historial de transacciones del sistema.</p>
                </div>
                <div class="overflow-x-auto">
                  <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                      <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cliente</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Monto</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                      </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                      <tr v-for="p in pagos" :key="p.id">
                        <td class="px-6 py-4 text-sm text-gray-500 font-mono">{{ p.id?.slice(0, 8) }}...</td>
                        <td class="px-6 py-4 text-sm text-gray-500">{{ p.cliente_uid?.slice(0, 8) }}...</td>
                        <td class="px-6 py-4 text-sm text-gray-900">{{ formatPrice(p.monto) }}</td>
                        <td class="px-6 py-4">
                          <span class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">{{ p.estado }}</span>
                        </td>
                      </tr>
                      <tr v-if="!pagos.length">
                        <td colspan="4" class="px-6 py-10 text-center text-sm text-gray-500">No hay pagos registrados.</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- PRECIOS TAB -->
              <div v-else-if="selectedTab === 'precios'" class="space-y-6">
                <div>
                  <h2 class="text-xl font-bold text-gray-900">Configuración de Precios</h2>
                  <p class="text-sm text-gray-500">Ajusta los coeficientes de la fórmula de precios.</p>
                </div>
                <div class="max-w-lg space-y-5">
                  <label class="space-y-1 block">
                    <span class="text-sm font-medium text-gray-700">Tarifa Base (BOB)</span>
                    <input v-model.number="pricing.base_rate" type="number" min="0" step="1" class="w-full border border-gray-200 rounded-lg p-3 text-sm" />
                  </label>
                  <label class="space-y-1 block">
                    <span class="text-sm font-medium text-gray-700">Tarifa por Habitación (BOB)</span>
                    <input v-model.number="pricing.room_rate" type="number" min="0" step="1" class="w-full border border-gray-200 rounded-lg p-3 text-sm" />
                  </label>
                  <label class="space-y-1 block">
                    <span class="text-sm font-medium text-gray-700">Tarifa por m² (BOB)</span>
                    <input v-model.number="pricing.sqm_rate" type="number" min="0" step="0.1" class="w-full border border-gray-200 rounded-lg p-3 text-sm" />
                  </label>
                  <label class="flex items-center gap-3 text-sm">
                    <input type="checkbox" v-model="pricing.zone_surcharge_enabled" class="rounded" />
                    <span class="font-medium text-gray-700">Habilitar recargo por zona</span>
                  </label>
                  <div class="text-xs text-gray-400">Moneda: {{ pricing.currency }}</div>
                  <button @click="guardarPrecios" class="px-6 py-3 bg-[#135bec] text-white rounded-lg text-sm font-semibold hover:bg-[#0f4abf]">Guardar Configuración</button>
                  <p v-if="mensajePrecios" class="text-sm font-medium" :class="mensajePrecios.includes('Error') ? 'text-red-600' : 'text-emerald-600'">{{ mensajePrecios }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- MODAL ZONA -->
      <div v-if="mostrarModalZona" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-md overflow-hidden border border-slate-200">
          <header class="bg-slate-50 px-6 py-4 border-b border-slate-100">
            <h3 class="font-bold text-lg text-slate-800">{{ editandoZona ? 'Editar Zona' : 'Nueva Zona' }}</h3>
          </header>
          <div class="p-6 space-y-4">
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Nombre</label>
              <input v-model="formZona.nombre" class="w-full border border-slate-200 rounded-lg p-2 text-sm" type="text" />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase mb-1">Recargo (%)</label>
              <input v-model.number="formZona.surcharge" type="number" min="0" max="1" step="0.01" class="w-full border border-slate-200 rounded-lg p-2 text-sm" />
            </div>
            <label class="flex items-center gap-2 text-sm">
              <input type="checkbox" v-model="formZona.active" class="rounded" />
              <span>Activo</span>
            </label>
          </div>
          <footer class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
            <button @click="mostrarModalZona = false" class="px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 rounded-lg">Cancelar</button>
            <button @click="guardarZona" class="px-6 py-2 text-sm font-bold text-white bg-[#135bec] hover:bg-[#0f4abf] rounded-lg shadow-md">{{ editandoZona ? 'Actualizar' : 'Crear' }}</button>
          </footer>
        </div>
      </div>

      <!-- MODAL EDITAR USUARIO -->
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
            <button @click="mostrarModal = false" class="px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 rounded-lg">Cancelar</button>
            <button @click="guardarCambios" class="px-6 py-2 text-sm font-bold text-white bg-[#135bec] hover:bg-[#0f4abf] rounded-lg shadow-md">Guardar Cambios</button>
          </footer>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const auth = useAuth();
const selectedTab = ref('usuarios');
const usuarios = ref([]);
const serviciosPendientes = ref([]);
const mostrarModal = ref(false);
const usuarioAEditar = ref({ uid: '', displayName: '', role: '' });

// Zonas state
const zonas = ref([]);
const mostrarModalZona = ref(false);
const editandoZona = ref(false);
const zonaEditandoId = ref(null);
const formZona = ref({ nombre: '', surcharge: 0, active: true });

// Pricing state
const pricing = ref({ base_rate: 30, room_rate: 15, sqm_rate: 0.5, zone_surcharge_enabled: true, currency: 'BOB' });
const mensajePrecios = ref('');

// Reservas + pagos state
const reservas = ref([]);
const pagos = ref([]);

const fotoUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `http://localhost:8000${url}`
}

const getToken = async () => {
  return await auth.getToken();
};

const cargarUsuarios = async () => {
  try {
    const token = await getToken();
    usuarios.value = await $fetch('http://localhost:8000/admin/users', {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` }
    });
  } catch (e) {
    console.error('Error al conectar con FastAPI:', e);
  }
};

const cargarServiciosPendientes = async () => {
  try {
    const token = await getToken();
    serviciosPendientes.value = await $fetch('http://localhost:8000/api/admin/servicios/pendientes', {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` }
    });
  } catch (e) {
    console.error('Error cargando servicios pendientes:', e);
  }
};

const cargarZonas = async () => {
  try {
    const token = await getToken();
    zonas.value = await $fetch('http://localhost:8000/api/admin/zonas', {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` }
    });
  } catch (e) {
    console.error('Error cargando zonas:', e);
  }
};

const cargarPricing = async () => {
  try {
    pricing.value = await $fetch('http://localhost:8000/api/pricing');
  } catch (e) {
    console.error('Error cargando pricing:', e);
  }
};

const eliminarUsuario = async (uid) => {
  if (confirm('¿Estás seguro de eliminar este usuario?')) {
    try {
      const token = await getToken();
      await $fetch(`http://localhost:8000/admin/users/${uid}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      });
      usuarios.value = usuarios.value.filter(u => u.uid !== uid);
      alert('Usuario eliminado con éxito');
    } catch (e) {
      console.error(e);
      alert('Error al eliminar');
    }
  }
};

const modificarUsuario = (user) => {
  usuarioAEditar.value = { ...user };
  mostrarModal.value = true;
};

const guardarCambios = async () => {
  try {
    const token = await getToken();
    await $fetch(`http://localhost:8000/admin/users/${usuarioAEditar.value.uid}/update`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: {
        new_name: usuarioAEditar.value.displayName,
        new_role: usuarioAEditar.value.role
      }
    });
    alert('¡Usuario actualizado con éxito!');
    mostrarModal.value = false;
    await cargarUsuarios();
  } catch (e) {
    console.error('Error al guardar:', e);
    alert('Error al actualizar: ' + (e.data?.detail || 'Error de red'));
  }
};

const validarServicio = async (servicioId, estado) => {
  try {
    const token = await getToken();
    await $fetch(`http://localhost:8000/api/admin/servicios/${servicioId}/validar`, {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: { estado }
    });
    alert(`Servicio ${estado} correctamente.`);
    await cargarServiciosPendientes();
  } catch (e) {
    console.error('Error validando servicio:', e);
    alert('No se pudo validar el servicio.');
  }
};

const irARegistro = () => {
  navigateTo('/signup');
};

const formatPrice = (value) => {
  return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'BOB' }).format(value || 0);
};

const badgeClassReserva = (estado) => {
  if (estado === 'Completado') return 'bg-emerald-100 text-emerald-700'
  if (estado === 'Cancelado') return 'bg-red-100 text-red-700'
  if (estado === 'Confirmado') return 'bg-blue-100 text-blue-700'
  if (estado === 'En_curso') return 'bg-purple-100 text-purple-700'
  return 'bg-yellow-100 text-yellow-700'
};

// Zona methods
const abrirModalZona = (zona = null) => {
  if (zona) {
    editandoZona.value = true;
    zonaEditandoId.value = zona.id;
    formZona.value = { nombre: zona.nombre, surcharge: zona.surcharge, active: zona.active };
  } else {
    editandoZona.value = false;
    zonaEditandoId.value = null;
    formZona.value = { nombre: '', surcharge: 0, active: true };
  }
  mostrarModalZona.value = true;
};

const guardarZona = async () => {
  try {
    const token = await getToken();
    if (editandoZona.value && zonaEditandoId.value) {
      await $fetch(`http://localhost:8000/api/admin/zonas/${zonaEditandoId.value}`, {
        method: 'PUT',
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: {
          nombre: formZona.value.nombre,
          surcharge: formZona.value.surcharge,
          active: formZona.value.active
        }
      });
    } else {
      await $fetch('http://localhost:8000/api/admin/zonas', {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: {
          nombre: formZona.value.nombre,
          surcharge: formZona.value.surcharge,
          active: formZona.value.active
        }
      });
    }
    mostrarModalZona.value = false;
    await cargarZonas();
  } catch (e) {
    console.error('Error guardando zona:', e);
    alert('Error al guardar la zona.');
  }
};

const eliminarZona = async (zonaId) => {
  if (!confirm('¿Desactivar esta zona?')) return;
  try {
    const token = await getToken();
    await $fetch(`http://localhost:8000/api/admin/zonas/${zonaId}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    });
    await cargarZonas();
  } catch (e) {
    console.error('Error desactivando zona:', e);
  }
};

const cargarReservas = async () => {
  try {
    const token = await getToken();
    reservas.value = await $fetch('http://localhost:8000/api/reservas', {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` }
    });
  } catch (e) {
    console.error('Error cargando reservas:', e);
  }
};

const cargarPagos = async () => {
  try {
    const token = await getToken();
    pagos.value = await $fetch('http://localhost:8000/api/admin/payments', {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` }
    });
  } catch (e) {
    console.error('Error cargando pagos:', e);
  }
};

// Pricing methods
const guardarPrecios = async () => {
  mensajePrecios.value = '';
  try {
    const token = await getToken();
    await $fetch('http://localhost:8000/api/admin/pricing', {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: {
        base_rate: pricing.value.base_rate,
        room_rate: pricing.value.room_rate,
        sqm_rate: pricing.value.sqm_rate,
        zone_surcharge_enabled: pricing.value.zone_surcharge_enabled,
        currency: pricing.value.currency
      }
    });
    mensajePrecios.value = 'Configuración de precios actualizada.';
  } catch (e) {
    console.error('Error guardando precios:', e);
    mensajePrecios.value = 'Error al guardar la configuración.';
  }
};

onMounted(async () => {
  await Promise.all([
    cargarUsuarios(),
    cargarServiciosPendientes(),
    cargarZonas(),
    cargarPricing(),
    cargarReservas(),
    cargarPagos()
  ]);
});
</script>
