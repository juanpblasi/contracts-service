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

### 1. Iniciar el Backend

```bash
cd backend
python app.py
```

El servidor estará disponible en: `http://localhost:5000`

### 2. Abrir el Dashboard

Abrir `frontend/index.html` en un navegador web.

### 3. Comparar Contratos

1. **Cargar Archivos**: Arrastra o selecciona dos archivos con la misma estructura
2. **Comparar**: Click en "Comparar Contratos"
3. **Revisar Resultados**: Ver el reporte detallado con estadísticas
4. **Exportar**: Descargar el reporte en JSON o HTML

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