# SGR La Serena 2026 — Sistema de Gestión de Requerimientos

Proyecto Django de la **Municipalidad de La Serena** (proyecto integrado, Programación Back End — Inacap La Serena). Sistema compuesto por **4 aplicaciones independientes** que persisten en **archivos JSON locales** (sin base de datos SQL, según la pauta).

## Estructura del proyecto

```
muni-serena/
├── manage.py
├── requirements.txt          # Django>=5.0,<6.0
├── sgr_project/              # Configuración global (settings, urls)
├── static/                   # Bootstrap local (css/js) + logo
├── templates/base.html       # Layout común (navbar + footer + mensajes)
│
├── gestion_institucional/    # APP 1 — Portada y delegaciones
│   └── templates/gestion_institucional/inicio.html
│
├── ficha_desempeno/          # APP 2 — Fichas y semáforo diario
│   ├── data/funcionarios.json
│   ├── services.py           # FuncionariosService (lectura/escritura JSON)
│   └── templates/ficha_desempeno/
│       ├── ficha_personal_lista.html
│       ├── ficha_personal.html
│       └── registrar_actividad.html
│
├── agenda_colectiva/         # APP 3 — Tubo de trabajo (Kanban CRUD)
│   ├── data/tubo_trabajo.json
│   ├── forms.py              # CompromisoForm con validaciones
│   ├── services.py           # TuboTrabajoService (CRUD completo)
│   └── templates/agenda_colectiva/
│       ├── tubo_tablero.html
│       ├── card_tarea.html
│       └── editar_compromiso.html
│
└── atencion_social/          # APP 4 — Casos sociales (máx. 3 gestiones)
    ├── data/casos_sociales.json
    ├── forms.py
    ├── services.py           # CasosSocialesService
    └── templates/atencion_social/
        ├── lista_casos.html
        └── detalle_caso.html
```

## Apps y funcionalidad

| App | URL | Funcionalidad |
|---|---|---|
| `gestion_institucional` | `/` | Portada institucional, estadísticas comunales y 6 delegaciones territoriales |
| `ficha_desempeno` | `/desempeno/personal/` | Fichas del personal municipal con **semáforo diario** (verde/ámbar/rojo) según el avance real vs. el esperado al día 46 de 91 del trimestre, y registro de actividades en terreno |
| `agenda_colectiva` | `/agenda/kanban/` | Tablero Kanban con CRUD completo de compromisos vecinales (crear, editar, mover de estado, eliminar) y barra de cumplimiento comunal (mínimo 80%) |
| `atencion_social` | `/social/casos/` | Registro de beneficiarios con historial de hasta **3 gestiones secuenciales** por caso |

## Cómo levantar el proyecto en local

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

Abrir <http://127.0.0.1:8000/>. **No requiere `migrate`** (no hay base de datos: `DATABASES = {}`).

## Flujo de trabajo en equipo (Git)

- `main` → entrega final
- `develop` → integración de ambos estudiantes
- `feature/estudiante1-crud` → apps 3 y 4 (`agenda_colectiva`, `atencion_social`)
- `feature/estudiante2-analisis` → apps 1 y 2 (`gestion_institucional`, `ficha_desempeno`)

Cada estudiante trabaja en sus carpetas y se integra mediante Pull Requests hacia `develop`.
