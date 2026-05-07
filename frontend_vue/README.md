# Frontend Vue.js

Este directorio contendrá el frontend moderno de la aplicación usando Vue.js.

## Instalación y uso

1. Instala Node.js si no lo tienes: https://nodejs.org/
2. Abre una terminal en esta carpeta y ejecuta:

   npm create vue@latest

3. Sigue las instrucciones para crear el proyecto (nombre, configuración, etc).
4. Entra a la carpeta creada y ejecuta:

   npm install
   npm run dev

Esto levantará el frontend en modo desarrollo (por defecto en http://localhost:5173).

## Conexión con Django

- Asegúrate de que el backend Django esté corriendo (http://localhost:8000).
- Configura las peticiones del frontend para apuntar a la API de Django.
- Usa JWT para autenticación si tu backend lo requiere.

## Estructura recomendada

- `/src` Código fuente Vue.js
- `/public` Archivos estáticos

## Notas

- El frontend y backend se desarrollan y despliegan por separado para mayor escalabilidad.
- Puedes construir el frontend con `npm run build` y servir los archivos estáticos en producción.
