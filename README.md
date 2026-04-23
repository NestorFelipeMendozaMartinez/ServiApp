# Plataforma de Servicios Bajo Demanda

Esta es una aplicación Django REST Framework para una plataforma de servicios bajo demanda, similar a Uber, Rappi y Fiverr.

## Características
- Autenticación JWT
- Perfiles de usuario con geolocalización
- Categorías y servicios
- Solicitudes de servicios y ofertas
- Sistema de calificaciones y reseñas
- Transacciones simuladas (efectivo/transferencia)
- Frontend web básico integrado

## Configuración de Desarrollo

1. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

2. Configurar la base de datos:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Crear superusuario:
   ```
   python manage.py createsuperuser
   ```

4. Ejecutar el servidor:
   ```
   python manage.py runserver
   ```

## Despliegue en Producción

1. Configurar variables de entorno:
   - Copia `.env.example` a `.env` y configura las variables:
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

## Tecnologías
- Backend: Django + DRF + JWT
- Base de datos: SQLite (dev) / PostgreSQL (prod)
- Frontend: HTML/JS básico