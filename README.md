# muni-serena
trabajo para la muni de serena en proyecto integrado

## Maqueta estática

El proyecto incluye una exportación estática en `docs/`, lista para publicar
en GitHub Pages. Las páginas se generan usando las mismas plantillas, datos
simulados y archivos Bootstrap locales del proyecto Django. Los formularios y
acciones CRUD se muestran como parte de la maqueta, pero no modifican datos.

Para regenerarla después de cambiar vistas, plantillas o datos:

```powershell
python scripts/export_static.py
```

En GitHub Pages, selecciona la rama publicada y la carpeta `/docs` como fuente.
