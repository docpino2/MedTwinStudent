# Acceso del piloto

Las rutas educativas `/api/v1/*` requieren una sesion Bearer. `GET /health`,
`POST /api/v1/auth/login` y los contratos OpenAPI son publicos. No hay registro
publico ni verificacion de propiedad del correo: se trata de acceso con cuentas
preautorizadas y contrasena.

## Contrato

- `POST /api/v1/auth/login`: JSON `email`, `password`; devuelve `access_token`,
  `token_type`, `expires_at` y `user` (`id`, `email`, `display_name`, `role`).
- `GET /api/v1/auth/me`: devuelve la cuenta activa usando Bearer.
- `POST /api/v1/auth/logout`: revoca el token enviado, devuelve 204.
- `GET /api/v1/auth/users`: lista cuentas sin hashes; solo rol `admin`.

Roles: `admin` (Administrador) y `user` (Usuario). Ambos pueden utilizar los
perfiles sinteticos compartidos del piloto. Esto no implementa aislamiento por
institucion ni permisos sobre expedientes de estudiantes reales.

## Configuracion

`PILOT_ACCOUNTS_JSON` contiene una lista de objetos con `email`, `display_name`,
`role` y `password_hash` Argon2id. Se configura exclusivamente en el servidor.
No guardar contrasenas o hashes productivos en Git, instrucciones Lovable,
capturas o archivos frontend. Cada cuenta usa su propia sal aleatoria incluso
cuando la contrasena de piloto sea compartida.

`AUTH_SESSION_HOURS` vale 8 por defecto. El token es aleatorio, opaco, y solo
su SHA-256 se guarda en `auth_sessions`. El frontend conserva el token en
sessionStorage, nunca la contrasena. Cada peticion comprueba caducidad y cuenta
activa. Cinco contrasenas incorrectas bloquean la cuenta durante 15 minutos.

El arranque crea solamente las tablas nuevas `auth_users` y `auth_sessions` e
inserta las cuentas iniciales ausentes. No requiere activar `INIT_DB_ON_STARTUP`.
Cambiar el JSON inicial no reemplaza claves, roles ni desactivaciones existentes.
Una rotacion posterior requiere actualizar el hash de la cuenta y revocar sus
sesiones mediante un proceso administrativo. El bootstrap es una solucion para
este piloto; debe pasar a migraciones versionadas al incorporar Alembic.

## Frontend

Validar `/auth/me` antes de montar el gemelo o cargar sus catalogos. Un 401
limpia sesion y datos locales; un 403 muestra acceso denegado. Ninguno debe
convertirse en datos simulados. Un error de red al verificar sesion permite
reintentar, sin conceder acceso. Un catalogo real no se mezcla con mocks.

## Confianza

La confianza inicial se fija antes de escribir la respuesta; la final se
confirma despues de responder, pero antes de ver la retroalimentacion. La UI
usa 0-100%, y la API recibe valores 0-1. La diferencia se expresa en puntos
porcentuales de confianza autodeclarada, nunca como ganancia de aprendizaje.
La calibracion requiere contrastar confianza y desempeno observado en la
rubrica a lo largo de varios intentos. Una disminucion puede reflejar mayor
reconocimiento de incertidumbre; un aumento por si solo no demuestra dominio.
