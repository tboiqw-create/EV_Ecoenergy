from django.http import HttpResponse
from django.shortcuts import render

from dispositivos.services import cargar_dispositivos


def inicio(request):
    contexto = {
        "sistema": "EcoEnergy",
        "mensaje": "Monitoreo energético responsable",
        "asignatura": "Programación Back End",
    }
    return render(
        request,
        "dispositivos/inicio.html",
        contexto,
    )


def dispositivos_zona(request, zona_id):
    if zona_id != 3:
        return HttpResponse("Zona no encontrada", status=404)

    dispositivos = cargar_dispositivos()
    total_consumo = sum(item.get("consumo_kwh", 0) for item in dispositivos)
    cantidad = len(dispositivos)
    estado = (
        "Activo"
        if any(item.get("estado") == "Activo" for item in dispositivos)
        else ("Inactivo" if dispositivos else "Vacío")
    )

    contexto = {
        "zona": f"Zona {zona_id}",
        "dispositivos": dispositivos,
        "total_consumo": total_consumo,
        "cantidad": cantidad,
        "estado": estado,
    }

    return render(request, "dispositivos/detalle_zona.html", contexto)


def catalogo(request):
    dispositivos = cargar_dispositivos()

    activos = sum(1 for item in dispositivos if item["estado"] == "Activo")

    contexto = {
        "dispositivos": dispositivos,
        "total": len(dispositivos),
        "total_activos": activos,
    }

    return render(request, "dispositivos/catalogo.html", contexto)
