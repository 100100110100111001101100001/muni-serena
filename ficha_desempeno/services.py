# PLACEHOLDER MINIMO — esto es responsabilidad real de tu compañero (App 2).
# Solo existe aca para que agenda_colectiva pueda importar FuncionariosService
# y correr hoy sin esperar su parte. Cuando el suba su ficha_desempeno real
# (con urls.py, views.py, templates, y agregada a INSTALLED_APPS), su version
# debe reemplazar/fusionarse con esta, manteniendo el mismo nombre de clase
# y los mismos metodos (get_all, get_by_id) para no romper agenda_colectiva.
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
