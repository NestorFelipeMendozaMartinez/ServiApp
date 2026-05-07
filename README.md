# Proyecto Django + Vue.js

## Estructura

- `servicios/`  → Proyecto Django (backend)
- `frontend/`   → Proyecto Vue.js (frontend SPA)

## Cómo ejecutar

### Backend (Django)
1. Crea y activa el entorno virtual:
   ```
   python -m venv .venv
   .venv\Scripts\activate  # En Windows
   ```
2. Instala dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Aplica migraciones:
   ```
   python manage.py migrate
   ```
4. Ejecuta el servidor:
   ```
   python manage.py runserver
   ```

### Frontend (Vue.js)
1. Instala Node.js desde https://nodejs.org/
2. Ve a la carpeta `frontend/` y crea el proyecto Vue:
   ```
   cd frontend
   npm create vue@latest
   # Sigue las instrucciones
   cd <nombre-proyecto>
   npm install
   npm run dev
   ```

## Conexión
- El frontend hace peticiones a la API Django (`http://localhost:8000/api/...`).
- Configura CORS en Django para permitir peticiones desde el frontend.
- Usa JWT para autenticación si es necesario.

## Producción
- El frontend se puede construir con `npm run build` y servir los archivos estáticos desde un servidor web.
- El backend puede desplegarse en cualquier servicio compatible con Django.

---

**¡Listo para escalar y profesionalizar tu app!**
     - `DJANGO_SECRET_KEY=<tu_clave_secreta>`
     - `DJANGO_DEBUG=False`
     - `DJANGO_ALLOWED_HOSTS=<tu_dominio>,localhost`
     - `DATABASE_URL=<url_postgresql>` (para PostgreSQL)

   El proyecto usa `python-dotenv` para cargar automáticamente el archivo `.env`.

2. Instalar dependencias de producción:
   ```
   pip install -r requirements.txt
   ```

3. Ejecutar migraciones:
   ```
   python manage.py migrate
   ```

4. Recopilar archivos estáticos:
   ```
   python manage.py collectstatic
   ```

5. Usar un servidor WSGI como Gunicorn:
   ```
   gunicorn servicios.wsgi:application
   ```

## API Endpoints

### Usuarios
- POST /api/users/register/ - Registro
- POST /api/users/login/ - Login (JWT)
- GET/PUT /api/users/profile/ - Perfil

### Servicios
- GET/POST /api/services/categories/ - Categorías
- GET/POST /api/services/services/ - Servicios
- GET/PUT/DELETE /api/services/services/<id>/ - Detalle

### Solicitudes
- GET/POST /api/requests/requests/ - Solicitudes
- GET/PUT/DELETE /api/requests/requests/<id>/ - Detalle
- GET/POST /api/requests/offers/ - Ofertas
- GET/PUT/DELETE /api/requests/offers/<id>/ - Detalle
- GET/POST /api/requests/reviews/ - Reseñas
- GET/POST /api/requests/transactions/ - Transacciones
- POST /api/requests/offers/<id>/contract-sign/ - Firmar contrato (cliente o proveedor)
- GET /api/requests/offers/<id>/contract/ - Descargar contrato PDF

## Tecnologías
- Backend: Django + DRF + JWT
- Base de datos: SQLite (dev) / PostgreSQL (prod)
- Frontend: HTML/JS básico