# 📋 Contract Comparison Service

Sistema empresarial de comparación de documentos contractuales desarrollado para compañías de seguros.

## 🚀 Descripción

Servicio profesional que permite comparar dos archivos de contratos con la misma estructura y genera reportes detallados mostrando:
- ✅ Campos coincidentes
- ⚠️ Campos diferentes (con valores de cada archivo)
- 📄 Campos únicos en cada archivo
- 📊 Estadísticas de comparación

## 🏗️ Arquitectura

```
contracts-service/
├── backend/              # API REST en Python Flask
│   ├── api/             # Endpoints REST
│   ├── services/        # Lógica de negocio
│   ├── utils/           # Utilidades
│   └── tests/           # Tests unitarios e integración
│
├── frontend/            # Dashboard empresarial
│   ├── index.html      # UI principal
│   ├── css/            # Estilos corporativos
│   └── js/             # Lógica cliente
│
└── samples/            # Archivos de ejemplo
```

## 🛠️ Tecnologías

**Backend:**
- Python 3.9+
- Flask (API REST)
- Pandas (procesamiento de datos)
- openpyxl (Excel)

**Frontend:**
- HTML5, CSS3, JavaScript
- Diseño empresarial responsive
- Drag & drop file upload

## 📦 Instalación

### Backend

```bash
# Navegar al directorio backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Mac/Linux:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Frontend

No requiere instalación adicional. Solo abrir `frontend/index.html` en un navegador.

## 🚀 Uso

### Paso 1: Instalar Dependencias del Backend

```bash
# Navegar al directorio backend
cd backend

# Crear entorno virtual (solo la primera vez)
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 2: Iniciar el Servidor

```bash
# Desde el directorio backend con el entorno virtual activado
python3 app.py
```

Por defecto, el servidor intentará usar el puerto **5000**. Si ese puerto está ocupado (común en macOS por AirPlay Receiver), usa un puerto alternativo:

```bash
PORT=5001 python3 app.py
```

Verás un mensaje como:
```
Contract Comparison Service initialized
 * Running on http://127.0.0.1:5001
```

### Paso 3: Abrir el Dashboard

El servidor ahora sirve automáticamente el frontend. Simplemente abre tu navegador y ve a:

```
http://localhost:5001/
```

(O el puerto que hayas configurado)

### Paso 4: Comparar Contratos

1. **Cargar Archivos**: 
   - Arrastra o haz clic en las áreas "Documento 1" y "Documento 2"
   - Selecciona dos archivos con la misma estructura
   - Formatos soportados: JSON, CSV, Excel, TXT

2. **Iniciar Comparación**: 
   - Haz clic en el botón **"🔍 COMPARAR CONTRATOS"**
   - Espera unos segundos mientras se procesa

3. **Revisar Resultados**: 
   - Ver el **Resumen Ejecutivo** con estadísticas clave
   - Explorar las tablas de **Diferencias**, **Coincidencias**, y **Campos Únicos**
   - Revisar el porcentaje de coincidencia

4. **Exportar Reporte** (opcional):
   - Descargar como **JSON** para procesamiento adicional
   - Descargar como **HTML** para compartir o archivar

### Archivos de Ejemplo

El proyecto incluye archivos de prueba en la carpeta `samples/`:
- `contract1.json` - Contrato original
- `contract2.json` - Contrato modificado

Prueba el sistema con estos archivos para ver todas las funcionalidades.

---

## 🔧 Solución de Problemas

### Puerto en Uso

Si ves el error: `Address already in use` o `Port 5000 is in use`:

**Opción 1: Usar otro puerto**
```bash
PORT=5001 python3 app.py
```

**Opción 2: Detener el proceso en el puerto**
```bash
# Ver qué está usando el puerto 5000
lsof -i:5000

# Matar el proceso
lsof -ti:5000 | xargs kill -9
```

**Opción 3: Desactivar AirPlay Receiver (macOS)**
1. Abre **Configuración del Sistema** (System Settings)
2. Busca **General** → **AirPlay & Handoff**
3. Desactiva **AirPlay Receiver**

### El Frontend no Carga

Si el dashboard no aparece en `http://localhost:5001/`:
1. Verifica que el servidor esté corriendo (revisa la terminal)
2. Asegúrate de estar usando el puerto correcto
3. Prueba refrescar el navegador con `Cmd + Shift + R` (macOS) o `Ctrl + Shift + R` (Windows/Linux)

### Error al Comparar Archivos

Si la comparación falla:
1. Verifica que ambos archivos tengan el mismo formato
2. Revisa que los archivos sean válidos (JSON bien formado, CSV con headers, etc.)
3. Verifica el tamaño (máximo 50MB por archivo)
4. Revisa la consola del navegador (F12) para detalles del error

## 📊 Formatos Soportados

- **JSON** (.json)
- **CSV** (.csv)
- **Excel** (.xlsx, .xls)
- **Texto** (.txt) - formato clave:valor

## 🔌 API Endpoints

### `GET /api/health`
Health check del servicio.

**Response:**
```json
{
  "status": "healthy",
  "service": "Contract Comparison Service",
  "version": "1.0.0"
}
```

### `POST /api/compare`
Compara dos archivos de contratos.

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `file1`: Archivo 1
  - `file2`: Archivo 2

**Response:**
```json
{
  "status": "success",
  "report": {
    "metadata": {...},
    "summary": {
      "total_fields": 10,
      "matches": 7,
      "differences": 2,
      "match_percentage": 70.0
    },
    "details": {
      "matches": [...],
      "differences": [...],
      "only_in_file1": [...],
      "only_in_file2": [...]
    }
  }
}
```

### `POST /api/compare/html`
Compara dos archivos y retorna reporte HTML.

**Request:** Igual que `/api/compare`

**Response:** HTML rendered del reporte

## 🧪 Tests

```bash
cd backend

# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar tests específicos
pytest tests/test_parser.py -v
pytest tests/test_comparator.py -v
pytest tests/test_api.py -v

# Ver coverage
pytest tests/ --cov=services --cov=api
```

## 📝 Ejemplo de Uso

Archivos de ejemplo incluidos en `/samples`:

**contract1.json:**
```json
{
  "contractNumber": "CTR-2024-001",
  "customerName": "Juan Pérez",
  "premium": 1500.00
}
```

**contract2.json:**
```json
{
  "contractNumber": "CTR-2024-001",
  "customerName": "Juan Pérez García",
  "premium": 1600.00
}
```

**Resultado:**
- ✅ Coincidencias: `contractNumber`
- ⚠️ Diferencias: `customerName`, `premium`

## 🎨 Diseño Empresarial

El dashboard incluye:
- Paleta de colores corporativa (azul Zurich)
- Interfaz drag & drop intuitiva
- Tablas interactivas con hover effects
- Loading states con spinners
- Diseño responsive
- Exportación de reportes

## 📄 Licencia

Proyecto desarrollado para uso empresarial interno.

## 👨‍💻 Autor

Desarrollado como servicio de arquitectura empresarial para compañías de seguros.

## 🔧 Configuración Avanzada

### Variables de Entorno

Crear archivo `.env` en `/backend`:

```
FLASK_ENV=development
SECRET_KEY=your-secret-key
MAX_FILE_SIZE=52428800
PORT=5000
```

### CORS

Configurar orígenes permitidos en `backend/config.py`:

```python
CORS_ORIGINS = ['http://localhost:3000', 'https://your-domain.com']
```

## 📞 Soporte

Para soporte técnico o consultas, contactar al equipo de desarrollo.