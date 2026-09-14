"""Export the Django mockup as a self-contained GitHub Pages site."""

import os
import posixpath
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urlsplit

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sgr_project.settings")

import django

django.setup()

from django.test import RequestFactory

from agenda_colectiva import views as agenda_views
from agenda_colectiva.services import TuboTrabajoService
from atencion_social import views as social_views
from atencion_social.services import CasosSocialesService
from auditoriaApp import views as auditoria_views
from configurarMetasApp import views as metas_views
from configurarMetasApp.services import PeriodosService
from evidenciasApp import views as evidencias_views
from ficha_desempeno import views as desempeno_views
from ficha_desempeno.services import FuncionariosService
from gestion_institucional import views as institucional_views
from resumenAlcaldeApp import views as alcalde_views


OUTPUT_DIR = BASE_DIR / "docs"
STATIC_DIR = BASE_DIR / "static"


def page(path, view, *args):
    return {"path": path, "view": view, "args": args}


def build_pages():
    pages = [
        page("index.html", institucional_views.vista_inicio),
        page("agenda/kanban.html", agenda_views.vista_tubo_tablero),
        page("social/casos.html", social_views.vista_lista_casos),
        page("evidencias/index.html", evidencias_views.dashboard_evidencias),
        page("auditoria/index.html", auditoria_views.registros_auditoria),
        page("metas/index.html", metas_views.periodos_lista),
        page("metas/crear.html", metas_views.crear_periodo),
        page("desempeno/index.html", desempeno_views.vista_ficha_personal_lista),
        page("resumen-alcalde/index.html", alcalde_views.resumen_general),
    ]

    for funcionario in FuncionariosService.get_all():
        funcionario_id = funcionario["id"]
        pages.extend(
            [
                page(
                    f"desempeno/personal-{funcionario_id}.html",
                    desempeno_views.vista_ficha_personal,
                    funcionario_id,
                ),
                page(
                    f"desempeno/registrar-{funcionario_id}.html",
                    desempeno_views.vista_registrar_actividad,
                    funcionario_id,
                ),
            ]
        )

    for compromiso in TuboTrabajoService.get_all():
        pages.append(
            page(
                f"agenda/editar-{compromiso['id']}.html",
                agenda_views.vista_editar_compromiso,
                compromiso["id"],
            )
        )

    for caso in CasosSocialesService.get_all():
        pages.append(
            page(
                f"social/caso-{caso['id']}.html",
                social_views.vista_detalle_caso,
                caso["id"],
            )
        )

    for periodo in PeriodosService.get_all():
        pages.append(
            page(
                f"metas/editar-{periodo['id']}.html",
                metas_views.editar_periodo,
                periodo["id"],
            )
        )

    return pages


def static_target(path):
    path = path.split("?", 1)[0]
    if path == "/":
        return "index.html"
    if path.startswith("/static/"):
        return path.lstrip("/")

    routes = {
        "/desempeno/personal/": "desempeno/index.html",
        "/agenda/kanban/": "agenda/kanban.html",
        "/social/casos/": "social/casos.html",
        "/evidencias/": "evidencias/index.html",
        "/metas/": "metas/index.html",
        "/auditoria/": "auditoria/index.html",
        "/resumen-alcalde/": "resumen-alcalde/index.html",
        "/agenda/kanban/crear/": "#",
    }
    if path in routes:
        return routes[path]

    matchers = [
        (r"^/desempeno/personal/(\d+)/$", "desempeno/personal-{}.html"),
        (r"^/desempeno/personal/(\d+)/registrar/$", "desempeno/registrar-{}.html"),
        (r"^/agenda/kanban/editar/(\d+)/$", "agenda/editar-{}.html"),
        (r"^/social/casos/(\d+)/$", "social/caso-{}.html"),
        (r"^/metas/editar/(\d+)/$", "metas/editar-{}.html"),
    ]
    for pattern, target in matchers:
        match = re.match(pattern, path)
        if match:
            return target.format(match.group(1))

    if any(
        path.startswith(prefix)
        for prefix in (
            "/agenda/kanban/eliminar/",
            "/agenda/kanban/estado/",
            "/social/casos/crear",
            "/social/casos/",
            "/metas/crear/",
            "/metas/eliminar/",
        )
    ):
        return "#"
    return None


def rewrite_links(html, current_path):
    current_dir = posixpath.dirname(current_path) or "."

    def replace_attribute(match):
        url = match.group("url")
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc or not parsed.path.startswith("/"):
            return match.group(0)
        target = static_target(parsed.path)
        if target is None:
            return match.group(0)
        if target == "#":
            rewritten = "#"
        else:
            rewritten = posixpath.relpath(target, current_dir)
            if parsed.query:
                rewritten += "?" + parsed.query
            if parsed.fragment:
                rewritten += "#" + parsed.fragment
        return f'{match.group("prefix")}{rewritten}{match.group("quote")}'

    attribute_pattern = re.compile(
        r'(?P<prefix>(?:href|action|src)=["\'])(?P<url>[^"\']+)(?P<quote>["\'])'
    )
    html = attribute_pattern.sub(replace_attribute, html)
    html = re.sub(
        r"<form(\s[^>]*)?>",
        lambda match: (
            match.group(0)
            if "onsubmit=" in match.group(0)
            else match.group(0)[:-1] + ' onsubmit="return false;">'
        ),
        html,
    )
    return html


def render_page(request_factory, definition):
    request = request_factory.get("/", HTTP_HOST="localhost")
    response = definition["view"](request, *definition["args"])
    return rewrite_links(response.content.decode("utf-8"), definition["path"])


def main():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)
    shutil.copytree(STATIC_DIR, OUTPUT_DIR / "static")
    (OUTPUT_DIR / ".nojekyll").touch()

    request_factory = RequestFactory()
    pages = build_pages()
    for definition in pages:
        destination = OUTPUT_DIR / definition["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            render_page(request_factory, definition), encoding="utf-8"
        )

    print(f"Exportadas {len(pages)} páginas estáticas en {OUTPUT_DIR}")


if __name__ == "__main__":
    main()