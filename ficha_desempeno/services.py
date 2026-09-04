import json
import os
from django.conf import settings


class FuncionariosService:
    @staticmethod
    def _get_path():
        data_dir = os.path.join(settings.BASE_DIR, 'ficha_desempeno', 'data')
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, 'funcionarios.json')

    @classmethod
    def get_all(cls):
        path = cls._get_path()
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @classmethod
    def get_by_id(cls, fid):
        funcionarios = cls.get_all()
        for f in funcionarios:
            if f['id'] == int(fid):
                return f
        return None

    @classmethod
    def registrar_avance(cls, fid, cantidad):
        funcionarios = cls.get_all()
        for f in funcionarios:
            if f['id'] == int(fid):
                f['avance_actual'] += int(cantidad)
                # Incrementar el primer item de medición por defecto en este prototipo funcional
                if f['items']:
                    f['items'][0]['avance'] += int(cantidad)
                break

        with open(cls._get_path(), 'w', encoding='utf-8') as file:
            json.dump(funcionarios, file, indent=2, ensure_ascii=False)
