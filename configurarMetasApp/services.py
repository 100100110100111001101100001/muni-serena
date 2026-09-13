import json
import os

from django.conf import settings


class PeriodosService:
    @staticmethod
    def _get_path():
        data_dir = os.path.join(settings.BASE_DIR, 'configurarMetasApp', 'data')
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, 'data.json')

    @classmethod
    def get_all(cls):
        path = cls._get_path()
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as data_file:
            return json.load(data_file)

    @classmethod
    def get_by_id(cls, periodo_id):
        return next((periodo for periodo in cls.get_all() if periodo['id'] == int(periodo_id)), None)

    @classmethod
    def create(cls, nombre, items):
        periodos = cls.get_all()
        new_id = max((periodo['id'] for periodo in periodos), default=0) + 1
        periodo = {'id': new_id, 'nombre': nombre, 'items': items}
        periodos.append(periodo)
        cls._save(periodos)
        return periodo

    @classmethod
    def update(cls, periodo_id, nombre, items):
        periodos = cls.get_all()
        for periodo in periodos:
            if periodo['id'] == int(periodo_id):
                periodo['nombre'] = nombre
                periodo['items'] = items
                break
        cls._save(periodos)

    @classmethod
    def delete(cls, periodo_id):
        periodos = [periodo for periodo in cls.get_all() if periodo['id'] != int(periodo_id)]
        cls._save(periodos)

    @classmethod
    def _save(cls, periodos):
        with open(cls._get_path(), 'w', encoding='utf-8') as data_file:
            json.dump(periodos, data_file, indent=2, ensure_ascii=False)
