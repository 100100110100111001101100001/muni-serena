import json
import os
import uuid
from django.conf import settings


class TuboTrabajoAPI:
    """Simulador de API local con persistencia interactiva en JSON"""

    @staticmethod
    def _get_path():
        return os.path.join(settings.BASE_DIR, 'agenda_colectiva', 'data', 'tubo_trabajo.json')

    @classmethod
    def _load_json(cls):
        path = cls._get_path()
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)

    @classmethod
    def _save_json(cls, data):
        path = cls._get_path()
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    @classmethod
    def get_all_compromisos(cls):
        """Simula GET /api/compromisos"""
        return cls._load_json()

    @classmethod
    def create_compromiso(cls, solicitante, telefono, territorio, descripcion, fecha, responsable):
        """Simula POST /api/compromisos"""
        compromisos = cls._load_json()
        nuevo_id = f"COMP-2026-{str(uuid.uuid4().hex[:4]).upper()}"

        nuevo_item = {
            "id_compromiso": nuevo_id,
            "vecino_solicitante": solicitante,
            "telefono": telefono,
            "territorio": territorio,
            "descripcion": descripcion,
            "estado": "Ingresado",
            "fecha_compromiso": fecha,
            "responsable_nombre": responsable
        }
        compromisos.append(nuevo_item)
        cls._save_json(compromisos)
        return nuevo_item

    @classmethod
    def update_estado_compromiso(cls, id_compromiso, nuevo_estado):
        """Simula PATCH /api/compromisos/<id>"""
        compromisos = cls._load_json()
        for c in compromisos:
            if c['id_compromiso'] == id_compromiso:
                c['estado'] = nuevo_estado
                cls._save_json(compromisos)
                return True
        return False
