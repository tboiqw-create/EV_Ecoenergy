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


def cargar_zonas():
    return cargar_json("zonas.json")


def cargar_categorias():
    return cargar_json("categorias.json")


def obtener_zona(zona_id):
    zona = buscar_por_id(cargar_zonas(), zona_id)
    if zona is None:
        return None

    categorias = {categoria["id"]: categoria for categoria in cargar_categorias()}
    dispositivos = [
        dict(
            dispositivo,
            categoria_nombre=categorias.get(
                dispositivo.get("categoria_id"), {}
            ).get("nombre", "Sin categoría"),
        )
        for dispositivo in cargar_dispositivos()
        if dispositivo.get("zona_id") == zona_id
    ]
    total_consumo = sum(dispositivo.get("consumo_kwh", 0) for dispositivo in dispositivos)
    limite = zona.get("limite_kwh", 0)

    return {
        **zona,
        "dispositivos": dispositivos,
        "cantidad": len(dispositivos),
        "total_consumo": total_consumo,
        "estado": "ALERTA" if total_consumo > limite else "NORMAL",
    }


def buscar_por_id(coleccion, identificador):
    return next(
        (item for item in coleccion if item.get("id") == identificador),
        None,
    )