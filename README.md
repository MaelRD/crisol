# El Crisol

Sistema personal de conocimiento, aprendizaje y memoria asistido por IA. **Local-first**, open source y modular.

> Estado: **V0.1 en construcción — Fase 1 (bootstrap)**. Ver [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Requisitos (macOS, Apple Silicon)

| Herramienta | Instalación | Uso |
|---|---|---|
| uv | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | Python 3.12, entornos y dependencias |
| Docker Desktop | ya instalado | PostgreSQL + pgvector (Fase 2) |
| Ollama | ya instalado | embeddings y LLM locales (Fases 6 y 9) |

`uv` descarga Python 3.12 automáticamente (`.python-version`); no hace falta tocar el Python del sistema.

## Puesta en marcha

```bash
cp .env.example .env     # configuración local (no se versiona)
make install             # uv sync: crea .venv e instala dependencias
make check               # ruff + mypy + pytest
make dev                 # API en http://127.0.0.1:8000  (docs: /docs)
curl http://127.0.0.1:8000/health
```

## Estructura

```text
src/crisol/
├── main.py              # fábrica de la app FastAPI
├── core/                # configuración, logging, errores
├── api/routes/          # endpoints HTTP (delgados)
├── domain/              # modelo de conocimiento, sin I/O
├── services/            # casos de uso: ingestión, búsqueda, chat
├── repositories/        # acceso a PostgreSQL
└── infrastructure/      # adaptadores: database, embeddings, llm, loaders
tests/  data/  docker/  scripts/  docs/
```

## Configuración

Toda la configuración vive en variables `CRISOL_*` (ver `.env.example`) y se lee en un único sitio: `crisol.core.config.get_settings()`. No hay credenciales en el código.

## Privacidad

`data/` está en `.gitignore`: tus documentos nunca se versionan.
