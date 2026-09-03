# EcoEnergy

Aplicación Django para consultar zonas de consumo energético y los dispositivos
instalados en cada zona. Los datos se cargan desde archivos JSON y las relaciones
se resuelven en Python.

## Requisitos

- Python 3.12 o superior
- Acceso a Internet para instalar las dependencias de `requirements.txt`

## Instalación

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

La clave de Django se genera automáticamente para el entorno local. En un
entorno compartido se puede definir `DJANGO_SECRET_KEY` antes de ejecutar la
aplicación.

## Ejecución

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py runserver
```

Luego abrir `http://127.0.0.1:8000/`.

## Funcionalidades

- Listado dinámico de las zonas de `data/zonas.json`.
- Detalle por zona con categorías, cantidad, consumo total y estado.
- Estado `ALERTA` cuando el consumo supera el límite; `NORMAL` en caso contrario.
- Soporte para zonas sin dispositivos y para cambios de cantidad en los JSON.
- Respuesta `404` controlada para identificadores inexistentes.

## Archivos de datos

- `data/zonas.json`: `id`, `nombre`, `limite_kwh`.
- `data/categorias.json`: `id`, `nombre`, `descripcion`.
- `data/dispositivos.json`: `id`, `nombre`, `consumo_kwh`, `zona_id`, `categoria_id`.