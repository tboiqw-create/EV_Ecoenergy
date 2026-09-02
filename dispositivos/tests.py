from django.test import TestCase
from django.test import override_settings


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

	def test_zona_sin_dispositivos_sigue_operativa(self):
		response = self.client.get("/zonas/3/dispositivos/")

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No hay dispositivos registrados")
		self.assertContains(response, "NORMAL")

	def test_zona_inexistente_responde_404(self):
		response = self.client.get("/zonas/999/dispositivos/")

		self.assertEqual(response.status_code, 404)

