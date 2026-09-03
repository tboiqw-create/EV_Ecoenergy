from django.http import Http404
from django.shortcuts import render

from dispositivos.services import cargar_dispositivos, cargar_zonas, obtener_zona


def inicio(request):
    contexto = {
        "sistema": "EcoEnergy",
        "mensaje": "Monitoreo energético responsable",
        "asignatura": "Programación Back End",
        "zonas": [obtener_zona(zona["id"]) for zona in cargar_zonas()],
    }
    return render(
        request,
        "dispositivos/inicio.html",
        contexto,
    )


def dispositivos_zona(request, zona_id):
    zona = obtener_zona(zona_id)
    if zona is None:
        raise Http404("Zona no encontrada")

    contexto = {
        "zona": zona,
        "dispositivos": zona["dispositivos"],
        "total_consumo": zona["total_consumo"],
        "cantidad": zona["cantidad"],
        "estado": zona["estado"],
    }

    return render(request, "dispositivos/detalle_zona.html", contexto)


def catalogo(request):
    dispositivos = cargar_dispositivos()
    consumo_total = sum(item.get("consumo_kwh", 0) for item in dispositivos)

    contexto = {
        "dispositivos": dispositivos,
        "total": len(dispositivos),
        "consumo_total": consumo_total,
    }

    return render(request, "dispositivos/catalogo.html", contexto)



