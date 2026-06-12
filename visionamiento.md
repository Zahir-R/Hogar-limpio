# UNIVERSIDAD MAYOR, REAL Y PONTIFICIA DE SAN

# FRANCISCO XAVIER DE CHUQUISACA

### FACULTAD DE CIENCIAS Y TECNOLOGIA

### ESTUDIANTES y CARRERAS:

### ● VARGAS ALARCON BRAYAN MARIO ING CIENCIAS DE LA COMPUTACION

### ● RIVERO TECO ZAHIR BARI ING CIENCIAS DE LA COMPUTACION

### ● ARANCIBIA LEON DIEGO ESTEBAN ING EN TECNOLOGÍAS DE LA

### INFORMACIÓN Y SEGURIDAD

### DOCENTE: ING R. DURAN

### MATERIA: INGENIERÍA DE SOFTWARE

### Fecha: 06/03/


## VISIÓN DEL PROYECTO: HOGAR LIMPIO

**1. Introducción
Nombre del Proyecto:
Hogar Limpio** – Plataforma Digital de Intermediación de Servicios Domésticos Verificados.
**Propósito del documento**
Este documento tiene como finalidad detallar los requisitos de alto nivel y el diseño
arquitectónico del sistema **Hogar Limpio**. Busca capturar la esencia técnica y comercial del
proyecto, sirviendo como guía maestra para el desarrollo de software en el entorno de la ciudad
de Sucre.
**Alcance**
El proyecto comprende el desarrollo de una plataforma (Backend en **Python** ) que conecte a
usuarios finales con personal de limpieza. **Hemos decidido** delimitar el alcance inicialmente al
radio urbano de Sucre y centrar los servicios exclusivamente en **limpieza básica** (mantenimiento
de áreas comunes, habitaciones, baños y cocinas), dejando fuera servicios especializados para
asegurar un control de calidad riguroso en esta primera fase.
**Definiciones y acrónimos**
    ● **Vetting:** Proceso de investigación y validación de antecedentes.
    ● **Python:** Lenguaje de programación interpretado de alto nivel, elegido por su agilidad y
       robustas librerías de seguridad.
    ● **Django/FastAPI:** Frameworks de Python considerados para la gestión de la lógica de
       negocio.
    ● **Pip/Poetry:** Herramientas de gestión de dependencias y paquetes en Python.
    ● **JWT (JSON Web Token):** Estándar para la transmisión segura de información entre
       partes como un objeto JSON.
    ● **Backend:** Capa de acceso a datos y lógica de negocio del software.
    ● **API:** Interfaz que permite la comunicación entre la aplicación y el servidor.
**2. Posicionamiento del negocio
Oportunidad de negocio**


Tras un análisis exhaustivo del mercado laboral en Bolivia, **hemos identificado** que el sector del
trabajo doméstico opera en un **80% de informalidad**. Según reportes de la Organización
Internacional del Trabajo (OIT) y testimonios en redes sociales locales (grupos de Facebook
como "Alguien Sabe Sucre"), existe un vacío crítico: la gente necesita ayuda en casa pero tiene
miedo de meter a un desconocido a su hogar. Esta desconfianza frena la economía digital en
Sucre, y **Hogar Limpio** nace para profesionalizar este vínculo mediante la tecnología.
**Declaración del problema
Elemento Descripción**
El problema
Inseguridad, falta de disponibilidad inmediata y variabilidad arbitraria de
precios
Afecta a Familias, universitarios y profesionales independientes en Sucre
El impacto
Riesgos de robos, pérdida de tiempo buscando recomendaciones y servicios
de mala calidad
Solución
exitosa
Una plataforma que garantice personal con antecedentes verificados y
precios fijos
**Declaración de la posición del producto (Análisis de Mercado Real)
El "Dolor" del Mercado (Basado en opiniones y noticias reales):**
● **Inseguridad Documentada:** En foros y secciones de noticias locales, el robo hormiga es
la queja número uno. Muchos usuarios comentan: "Contraté a alguien que vi en un aviso
en el poste y se llevó cosas pequeñas, no tengo cómo ubicarla".
● **Falta de Estándar:** No hay una tarifa clara. Los usuarios reportan que el precio depende
de "la cara del cliente" o del humor del trabajador, generando roces innecesarios.
● **Incumplimiento:** Vídeos y comentarios de trabajadores del sector indican que muchas
veces no asisten porque encuentran un trabajo que paga 10 pesos más ese mismo día,
dejando al cliente plantado.
**El Valor Agregado de Hogar Limpio:**
● **Confianza por Verificación:** No es una app abierta donde cualquiera entra y ya. Cada
trabajador pasa por una entrevista presencial y entrega certificados de antecedentes
penales.
● **Tarificación Algorítmica: Hemos decidido** implementar un módulo que calcule el costo
basado en metros cuadrados o número de habitaciones, eliminando la negociación
manual.
● **Seguro de Confianza:** Si algo sale mal, la app tiene el registro completo del personal,
ofreciendo una capa de seguridad legal que el mercado informal no tiene.


**3. Descripción de los Stakeholders y usuarios
Resumen de las partes interesadas**
    ● **Equipo de Desarrollo (Vargas, Rivero, Arancibia):** Responsables de la arquitectura en
       Python, la seguridad de la base de datos y la escalabilidad del sistema.
    ● **Administración Central:** Encargada de la validación física de los documentos de los
       trabajadores en Sucre.
    ● **Clientes:** Personas que buscan eficiencia y, sobre todo, seguridad en su entorno privado.
    ● **Evaluadores:** El tribunal académico de la Facultad de Ciencia y Tecnología (USFX).
**Perfiles de las partes interesadas y de los usuarios
1. El Personal de Limpieza (Oferta):
Hemos decidido** ofrecer dos modalidades para ser inclusivos pero organizados:
    ● **Perfil Independiente (Estilo "Gig Economy"):** Personas que tienen otras actividades y
       quieren ganar dinero extra en sus horas libres. Ellos activan su disponibilidad en la app.
    ● **Perfil Dedicado:** Trabajadores que buscan una agenda llena y estabilidad. La app les
       prioriza servicios para asegurar que tengan ingresos constantes.
    ● **Requisito Obligatorio:** Todos, sin excepción, deben pasar la revisión de seguridad
       (Cédula de Identidad, Antecedentes de la FELCC y verificación de domicilio).
**2. El Cliente Ideal (Demanda):**
    ● Cualquier ciudadano con residencia en Sucre. Al ver el perfil del trabajador, el cliente
       podrá ver fotos, años de experiencia y, lo más importante, la **calificación de otros**
       **clientes**. Esto empodera al usuario para elegir según su presupuesto y confianza.
**4. Características del producto
Funciones "Estrella"**
    ● **Módulo de Verificación "Escudo":** Interfaz administrativa desarrollada en Python para
       auditar la vigencia de antecedentes penales. El sistema inhabilita automáticamente
       perfiles con documentos vencidos.
    ● **Geolocalización por Zonas:** Para optimizar costos de transporte en Sucre, **hemos**
       **decidido** que el sistema agrupe servicios por zonas geográficas (Ej: San Roque, Central,
       Zona Sur).
    ● **Sistema de Reputación Dinámica:** Algoritmo que premia al personal con mejores
       calificaciones, dándoles prioridad en la visualización de servicios.


● **Pagos Digitales (QR):** Integración de pasarelas de pago bolivianas para transacciones sin
efectivo.
**Requisitos del sistema**
● **Funcionales:**
o **Gestión de Cuentas:** Registro y login diferenciado para dos tipos de perfiles:
“Cliente” y “Personal de Limpieza”.
o **Gestión de reservas:** Sistema para programar, visualizar y cancelar servicios
únicos o periódicos en días y horas específicas.
o **Panel de administración:** Interfaz para que los administradores supervisen la
plataforma, auditen servicios y gestionen la verificación de usuarios.
● **No funcionales:**
o **Seguridad:** Encriptación de contraseñas y protección de datos personales.
o **Disponibilidad:** El sistema debe estar activo 24/7.
o **Usabilidad:** Interfaz intuitiva para personas que no están acostumbradas a usar
tecnología compleja.

**5. Restricciones y Aspectos Técnicos**
    ● **Tecnología Base: Hemos decidido** utilizar **Python** como lenguaje principal del backend
       por su capacidad para manejar lógica de datos compleja y su facilidad para integrarse
       con servicios de mapas y pagos.
    ● **Arquitectura:** Se utilizará un modelo de microservicios o un monolito modular
       (dependiendo de la escala) para asegurar que el sistema no se bloquee durante horas
       pico de demanda en Sucre.
    ● **Dependencias:** El proyecto utilizará gestores de paquetes como **Pip** y entornos virtuales
       para asegurar que el desarrollo sea limpio y reproducible entre los tres integrantes del
       equipo.
    ● **Contexto Legal:** El software se alineará con la normativa boliviana vigente para
       garantizar que el manejo de fotos de Cédulas de Identidad y croquis de domicilio sea
       estrictamente confidencial.


