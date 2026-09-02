import json
import os
from django.conf import settings

# Simula la capa de API que leeria/escribiria en un backend real.
# Por ahora solo lee el JSON local (no hay BD, segun la pauta).

class TuboTrabajoAPI:
    @staticmethod
    def _get_path():
        return os.path.join(settings.BASE_DIR, 'agenda_colectiva', 'data', 'tubo_trabajo.json')

    @classmethod
    def get_all(cls):
        """Simula GET /api/compromisos"""
        try:
            with open(cls._get_path(), 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
