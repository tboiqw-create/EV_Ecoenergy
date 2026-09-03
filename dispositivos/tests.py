from django.test import TestCase
from django.test import override_settings
from unittest.mock import patch


@override_settings(ALLOWED_HOSTS=["testserver"])
class VistasDispositivosTests(TestCase):
	def test_listado_muestra_todas_las_zonas(self):
		response = self.client.get("/")

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Oficinas administrativas")
		self.assertContains(response, "Area de produccion")
		self.assertContains(response, "Almacen")

	def test_detalle_calcula_alerta_y_resuelve_categoria(self):
		response = self.client.get("/zonas/2/dispositivos/")

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "ALERTA")
		self.assertContains(response, "Climatizacion")
		self.assertContains(response, "274.8 kWh")

	@patch("dispositivos.services.cargar_dispositivos")
	def test_nuevos_dispositivos_actualizan_metricas(self, cargar_dispositivos):
		cargar_dispositivos.return_value = [
			{
				"id": 101,
				"nombre": "Nuevo dispositivo 1",
				"consumo_kwh": 20.0,
				"zona_id": 1,
				"categoria_id": 1,
			},
			{
				"id": 102,
				"nombre": "Nuevo dispositivo 2",
				"consumo_kwh": 40.0,
				"zona_id": 1,
				"categoria_id": 2,
			},
		]

		response = self.client.get("/zonas/1/dispositivos/")

		self.assertContains(response, "Nuevo dispositivo 1")
		self.assertContains(response, "Nuevo dispositivo 2")
		self.assertContains(response, ">2<")
		self.assertContains(response, "60.0 kWh")
		self.assertContains(response, "NORMAL")

	@patch("dispositivos.services.cargar_dispositivos")
	def test_mayor_volumen_se_muestra_en_tabla(self, cargar_dispositivos):
		cargar_dispositivos.return_value = [
			{
				"id": identificador,
				"nombre": f"Dispositivo {identificador}",
				"consumo_kwh": 1.0,
				"zona_id": 1,
				"categoria_id": 1,
			}
			for identificador in range(1, 31)
		]

		response = self.client.get("/zonas/1/dispositivos/")

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "30.0 kWh")
		self.assertContains(response, "Dispositivo 30")

	def test_zona_sin_dispositivos_sigue_operativa(self):
		response = self.client.get("/zonas/3/dispositivos/")

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No hay dispositivos registrados")
		self.assertContains(response, "NORMAL")

	def test_zona_inexistente_responde_404(self):
		response = self.client.get("/zonas/999/dispositivos/")

		self.assertEqual(response.status_code, 404)
		self.assertContains(response, "La zona solicitada no existe", status_code=404)

