# Technical-Entity-Extraction-Pipeline

Pipeline de extracción de entidades técnicas con LangChain (LCEL), salida validada con Pydantic y reintentos automáticos.

Recibe un párrafo de texto (descripción de arquitectura, log de error, etc.) y devuelve un objeto estructurado:

- `tecnologias` — lista de tecnologías detectadas
- `nivel_de_criticidad` — `baja` | `media` | `alta`
- `resumen_tecnico` — resumen breve del contenido

Soporta **Gemini**, **OpenAI** y **Anthropic** mediante un factory configurable.

## Requisitos

- Python 3.12+
- Una API key del proveedor que vayas a usar

## 1. Crear el entorno virtual

Desde la raíz del repositorio:

```bash
python -m venv env
```

Activar el entorno:

**Windows (PowerShell):**

```powershell
.\env\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source env/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## 2. Variables de entorno

Copiá el ejemplo y completá tus claves:

```bash
cp .env.example .env
```

Contenido de `.env`:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=tu_api_key_gemini
OPENAI_API_KEY=tu_api_key_openai
ANTHROPIC_API_KEY=tu_api_key_anthropic
```

| Variable | Descripción |
|----------|-------------|
| `LLM_PROVIDER` | Proveedor activo: `openai`, `anthropic` o `gemini` |
| `OPENAI_API_KEY` | Clave de OpenAI (si usás `openai`) |
| `ANTHROPIC_API_KEY` | Clave de Anthropic (si usás `anthropic`) |
| `GEMINI_API_KEY` | Clave de Google Gemini (si usás `gemini`) |

Solo necesitás la API key del proveedor elegido en `LLM_PROVIDER`.

## 3. Ejecutar el script de prueba

Con el entorno activado y el `.env` configurado:

```bash
python main.py
```

El script ejecuta `process_text()` de forma asíncrona sobre un texto de ejemplo e imprime el JSON validado.

## Ejemplo de salida esperada

Entrada (ejemplo):

> La API de pagos está montada en FastAPI detrás de un load balancer. Usa Redis para caché de sesiones y PostgreSQL como base principal. Bajo carga concurrente las conexiones a la DB se saturan y aparecen timeouts 504.

Salida:

```json
{
  "tecnologias": ["FastAPI", "Redis", "PostgreSQL"],
  "nivel_de_criticidad": "alta",
  "resumen_tecnico": "API con caché en Redis y persistencia en PostgreSQL; cuello de botella en conexiones concurrentes."
}
```

## Uso programático

```python
import asyncio
from chain import process_text

async def run():
    result = await process_text("Tu texto técnico acá...")
    print(result.model_dump_json(indent=2))

asyncio.run(run())
```

## 4. Tests automatizados

Con el entorno activado:

```bash
pytest -v
```

La suite cubre:

- validación del schema Pydantic (`tests/test_schemas.py`)
- prompt template, composición LCEL y `process_text()` con LLM mockeado (`tests/test_chain.py`)
- factory de providers (`tests/test_factory.py`)

No requieren API keys ni llamadas reales al modelo.

## Estructura

```
├── main.py              # Mini-script de prueba asíncrono
├── chain.py             # Prompt template + cadena LCEL + process_text()
├── schemas.py           # Modelo Pydantic (ExtraccionTecnica)
├── config/
│   └── config.py        # Provider, API keys y modelos default
├── model/
│   └── factory.py       # Factory: ChatOpenAI / ChatAnthropic / ChatGoogleGenerativeAI
├── tests/
│   ├── test_schemas.py
│   ├── test_chain.py
│   └── test_factory.py
├── requirements.txt
├── .env.example
└── consignas.md
```

## Componentes del pipeline

| Pieza | Dónde | Qué hace |
|-------|--------|----------|
| Esquema Pydantic | `schemas.py` | Contrato de salida con validaciones |
| Prompt template | `chain.py` | `ChatPromptTemplate` con `{text}` y `{format_instructions}` |
| Cadena LCEL | `chain.py` | `prompt \| model.with_structured_output(ExtraccionTecnica)` |
| Resiliencia | `chain.py` | `.with_retry(stop_after_attempt=3)` |
| Función async | `chain.py` | `process_text()` con `.ainvoke()` y logs |

## Checklist de entrega

- [x] `schemas.py` con modelo Pydantic
- [x] `chain.py` con LCEL, structured output y reintentos
- [x] `process_text()` asíncrona con logs
- [x] Mini-script de prueba (`main.py`)
- [x] README con instrucciones y ejemplo JSON
- [x] Suite de tests automatizados (`pytest`)
