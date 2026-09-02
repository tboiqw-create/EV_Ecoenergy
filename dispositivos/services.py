import json
from pathlib import Path

from django.conf import settings


def cargar_json(nombre_archivo):
    ruta = Path(settings.BASE_DIR) / "data" / nombre_archivo

    if not ruta.exists():
        return []

    try:
        with ruta.open(encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(datos, list):
        return []

    return datos


def cargar_dispositivos():
    return cargar_json("dispositivos.json")


zonas = cargar_json("zonas.json")
categorias = cargar_json("categorias.json")
dispositivos = cargar_dispositivos()


def buscar_por_id(coleccion, identificador):
    return next(
        (item for item in coleccion if item.get("id") == identificador),
        None,
    )