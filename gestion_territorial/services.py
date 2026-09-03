import json
import os
from django.conf import settings

# Simula la capa de API que leeria/escribiria en un backend real.
# Por ahora solo lee el JSON local (no hay BD, segun la pauta).


class FuncionariosAPI:
    @staticmethod
    def _get_path():
        return os.path.join(settings.BASE_DIR, 'gestion_territorial', 'data', 'funcionarios.json')

    @classmethod
    def get_all(cls):
        """Simula GET /api/funcionarios"""
        try:
            with open(cls._get_path(), 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    @classmethod
    def get_by_id(cls, id_funcionario):
        """Simula GET /api/funcionarios/<id>"""
        for funcionario in cls.get_all():
            if funcionario.get('id') == id_funcionario:
                return funcionario
        return None
