import json
import os
from datetime import date
from django.conf import settings


class CasosSocialesService:
    @staticmethod
    def _get_path():
        data_dir = os.path.join(settings.BASE_DIR, 'atencion_social', 'data')
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, 'casos_sociales.json')

    @classmethod
    def get_all(cls):
        path = cls._get_path()
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @classmethod
    def get_by_id(cls, cid):
        casos = cls.get_all()
        for c in casos:
            if c['id'] == int(cid):
                return c
        return None

    @classmethod
    def create_caso(cls, data):
        casos = cls.get_all()
        new_id = max([c['id'] for c in casos]) + 1 if casos else 1
        nuevo = {
            "id": new_id,
            "rut_vecino": data['rut_vecino'],
            "nombre_vecino": data['nombre_vecino'],
            "direccion": data['direccion'],
            "telefono": data['telefono'],
            "atenciones": []
        }
        casos.append(nuevo)
        cls._save(casos)
        return nuevo

    @classmethod
    def add_atencion(cls, cid, atencion_data):
        casos = cls.get_all()
        for c in casos:
            if c['id'] == int(cid):
                etapa = len(c['atenciones']) + 1
                if etapa > 3:
                    # Limite tecnico absoluto exigido por la regla oficial (Maximo 3 etapas)
                    raise ValueError("Este caso social ya ha agotado el límite de 3 gestiones permitidas.")

                nueva_atencion = {
                    "etapa": etapa,
                    "fecha": str(date.today()),
                    "servicio": atencion_data['servicio'],
                    "observacion": atencion_data['observacion'],
                    "resultado": atencion_data['resultado']
                }
                c['atenciones'].append(nueva_atencion)
                break
        cls._save(casos)

    @classmethod
    def delete_caso(cls, cid):
        casos = cls.get_all()
        casos = [c for c in casos if c['id'] != int(cid)]
        cls._save(casos)

    @classmethod
    def _save(cls, data):
        with open(cls._get_path(), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
