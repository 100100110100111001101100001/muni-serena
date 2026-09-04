import json
import os
from django.conf import settings


class TuboTrabajoService:
    @staticmethod
    def _get_path():
        data_dir = os.path.join(settings.BASE_DIR, 'agenda_colectiva', 'data')
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, 'tubo_trabajo.json')

    @classmethod
    def get_all(cls):
        path = cls._get_path()
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @classmethod
    def get_by_id(cls, tid):
        compromisos = cls.get_all()
        for c in compromisos:
            if c['id'] == int(tid):
                return c
        return None

    @classmethod
    def create(cls, data):
        compromisos = cls.get_all()
        new_id = max([c['id'] for c in compromisos]) + 1 if compromisos else 1
        nuevo = {
            "id": new_id,
            "vecino": data['vecino'],
            "telefono": data['telefono'],
            "territorio": data['territorio'],
            "descripcion": data['descripcion'],
            "estado": "Ingresado",
            "fecha_compromiso": str(data['fecha_compromiso']),
            "responsable_id": int(data['responsable_id'])
        }
        compromisos.append(nuevo)
        cls._save(compromisos)
        return nuevo

    @classmethod
    def update(cls, tid, data):
        compromisos = cls.get_all()
        for c in compromisos:
            if c['id'] == int(tid):
                c['vecino'] = data['vecino']
                c['telefono'] = data['telefono']
                c['territorio'] = data['territorio']
                c['descripcion'] = data['descripcion']
                c['fecha_compromiso'] = str(data['fecha_compromiso'])
                c['responsable_id'] = int(data['responsable_id'])
                break
        cls._save(compromisos)

    @classmethod
    def update_estado(cls, tid, nuevo_estado):
        compromisos = cls.get_all()
        for c in compromisos:
            if c['id'] == int(tid):
                c['estado'] = nuevo_estado
                break
        cls._save(compromisos)

    @classmethod
    def delete(cls, tid):
        compromisos = cls.get_all()
        compromisos = [c for c in compromisos if c['id'] != int(tid)]
        cls._save(compromisos)

    @classmethod
    def _save(cls, data):
        with open(cls._get_path(), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
