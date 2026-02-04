# Deployment Guide - Vercel

Esta guía te ayudará a desplegar el Contract Comparison Service en Vercel.

## Prerrequisitos

1. Cuenta en [Vercel](https://vercel.com)
2. [Vercel CLI](https://vercel.com/docs/cli) instalado (opcional)
3. Repositorio Git (GitHub, GitLab, o Bitbucket)

## Método 1: Deploy desde GitHub (Recomendado)

### Paso 1: Subir a GitHub

```bash
# Si aún no has inicializado Git
git init
git add .
git commit -m "Initial commit - Contract Comparison Service"

# Crear repositorio en GitHub y conectar
git remote add origin https://github.com/tu-usuario/contracts-service.git
git branch -M main
git push -u origin main
```

### Paso 2: Importar a Vercel

1. Ve a [vercel.com/new](https://vercel.com/new)
2. Selecciona "Import Git Repository"
3. Conecta tu cuenta de GitHub
4. Selecciona el repositorio `contracts-service`
5. Configura el proyecto:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (raíz del proyecto)
   - **Build Command**: (dejar vacío)
   - **Output Directory**: `frontend`
6. Click en "Deploy"

### Paso 3: Variables de Entorno (Opcional)

Si necesitas configurar variables:
1. Ve a Project Settings → Environment Variables
2. Agrega:
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: (genera una clave segura)

## Método 2: Deploy con Vercel CLI

### Instalar Vercel CLI

```bash
npm install -g vercel
```

### Deploy

```bash
# Desde el directorio raíz del proyecto
vercel

# Sigue las instrucciones:
# - Set up and deploy? Yes
# - Which scope? (tu usuario/organización)
# - Link to existing project? No
# - Project name? contracts-service
# - In which directory is your code located? ./
```

### Deploy a Producción

```bash
vercel --prod
```

## Arquitectura en Vercel

```
Vercel Deployment
├── Frontend (Static Files)
│   └── Servido directamente desde /frontend
│
└── Backend (Serverless Functions)
    └── /api/* → backend/api/index.py
```

## Configuración Automática

El proyecto incluye:
- ✅ `vercel.json` - Configuración de rutas y builds
- ✅ `backend/api/index.py` - Entry point serverless
- ✅ `requirements.txt` - Dependencias Python
- ✅ Frontend con rutas relativas - Compatible con Vercel

## URLs del Proyecto Desplegado

Después del deploy, tendrás:
- **Frontend**: `https://tu-proyecto.vercel.app/`
- **API Health**: `https://tu-proyecto.vercel.app/api/health`
- **API Compare**: `https://tu-proyecto.vercel.app/api/compare`

## Limitaciones en Vercel

⚠️ **Importante**: Vercel tiene algunas limitaciones:

1. **Tiempo de ejecución**: Máximo 10 segundos por request (hobby plan)
2. **Tamaño de payload**: Máximo 4.5 MB por request
3. **Archivos temporales**: Se borran después de cada invocación
4. **Cold starts**: La primera request puede ser lenta

Si necesitas procesar archivos muy grandes o tiempos largos, considera:
- **Railway**: Mejor para aplicaciones Python tradicionales
- **Render**: Soporta servicios persistentes
- **Heroku**: Alternativa tradicional para Flask

## Testing en Vercel

Después del deploy:

1. Abre `https://tu-proyecto.vercel.app/`
2. Verifica que el dashboard cargue correctamente
3. Prueba subir archivos de ejemplo desde `/samples`
4. Verifica que la comparación funcione

## Troubleshooting

### Error: Build failed
- Verifica que `requirements.txt` esté en la raíz
- Revisa los logs en Vercel Dashboard

### Error: API no responde
- Verifica que `backend/api/index.py` existe
- Revisa la configuración en `vercel.json`

### Error: Frontend no carga
- Verifica que los archivos estén en `/frontend`
- Revisa la ruta en `vercel.json`

## Redeployment

Cada vez que hagas push a GitHub, Vercel redesplegará automáticamente:

```bash
git add .
git commit -m "Update feature X"
git push
```

## Dominio Personalizado

1. Ve a Project Settings → Domains
2. Agrega tu dominio: `comparador.tuempresa.com`
3. Sigue las instrucciones de DNS

---

¡Listo! Tu servicio estará disponible globalmente en minutos. 🚀
