from datetime import date, timedelta
import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect, Browser

from django.urls import reverse

from app.models import City, Client, Medicine, Provider, Pet

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
playwright = sync_playwright().start()
headless = os.environ.get("HEADLESS", 1) == 1
slow_mo = os.environ.get("SLOW_MO", 0)


class PlaywrightTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser: Browser = playwright.firefox.launch(
            headless=headless, slow_mo=int(slow_mo)
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()

    def setUp(self):
        super().setUp()
        self.page = self.browser.new_page()

    def tearDown(self):
        super().tearDown()
        self.page.close()


class HomeTestCase(PlaywrightTestCase):

    def test_should_have_home_cards_with_links(self):
        self.page.goto(self.live_server_url)

        home_clients_link = self.page.get_by_test_id("home-Clientes")

        expect(home_clients_link).to_be_visible()
        expect(home_clients_link).to_have_text("Clientes")
        expect(home_clients_link).to_have_attribute("href", reverse("clients_repo"))

        home_providers_link = self.page.get_by_test_id("home-Proveedores")

        expect(home_providers_link).to_be_visible()
        expect(home_providers_link).to_have_text("Proveedores")
        expect(home_providers_link).to_have_attribute("href", reverse("providers_repo"))


class ClientsRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_show_clients_data(self):
        city = City.objects.create(name='Berisso')

        client1 = Client.objects.create(
            name="Juan Sebastián Veron",
            city=city,
            phone="541555232",
            email="brujita75@hotmail.com",
        )

        client2 = Client.objects.create(
            name="Guido Carrillo",
            city=city,
            phone="541232555",
            email="goleador@gmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).not_to_be_visible()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("541555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("541232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()
        
    def test_should_show_add_client_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo cliente", exact=False
        )
        expect(add_client_action).to_have_attribute("href", reverse("clients_form"))

    def test_should_show_client_edit_action(self):
        city = City.objects.create(name='Berisso')
        
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            city=city,
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")
        
        edit_action = self.page.query_selector('link[name="Editar"]')
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )

    def test_should_show_client_delete_action(self):
        city = City.objects.create(name='Berisso')
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            city=city,
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_form = self.page.query_selector(
            'form[name="Formulario de eliminación de cliente"]'
        )
        
        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("clients_delete"))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()


    def test_should_can_be_able_to_delete_a_client(self):
        city = City.objects.create(name='Berisso')
        
        Client.objects.create(
            name="Juan Sebastián Veron",
            city=city,
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("clients_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.query_selector('button[name="Eliminar"]').click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()


class ClientCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_client(self):
        city = City.objects.create(name='Berisso')
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()
        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("541555232")
        self.page.get_by_label("Email").fill("brujita75@hotmail.com")
        self.page.get_by_label("Ciudad").select_option("Berisso")

        self.page.get_by_role("button", name="Guardar").click()
        
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("541555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()

    def test_should_be_able_to_edit_a_client(self):
        city = City.objects.create(name='Berisso')
        
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            city=city,
            phone="221555232",
            email="brujita75@vetsoft.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")
        
        self.page.get_by_label("Nombre").fill("Clientemod")
        self.page.get_by_label("Teléfono").fill("5412")
        self.page.get_by_label("Email").fill("cliente@vetsoft.com")
        self.page.get_by_label("Ciudad").select_option(city.name)

        self.page.get_by_role("button", name="Guardar").click()

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")
        
        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("221555232")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@vetsoft.com")).not_to_be_visible()

        expect(self.page.get_by_text("Clientemod")).to_be_visible()
        expect(self.page.get_by_text("5412")).to_be_visible()
        expect(self.page.get_by_text("cliente@vetsoft.com")).to_be_visible()

        edit_action = self.page.query_selector('link[name="Editar"]')
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )


#provedor
class ProvidersRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        expect(self.page.get_by_text("No existen proveedores")).to_be_visible()

    def test_should_show_providers_data(self):
        Provider.objects.create(
            name="Proveedor 1",
            address="Calle 1",
            phone="123456789",
            email="proveedor1@example.com",
            floor_apartament="Piso 1a",
        )

        Provider.objects.create(
            name="Proveedor 2",
            address="Calle 2",
            phone="987654321",
            email="proveedor2@example.com",
            floor_apartament="Piso 1b",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        expect(self.page.get_by_text("No existen proveedores")).not_to_be_visible()

        expect(self.page.get_by_text("Proveedor 1")).to_be_visible()
        expect(self.page.get_by_text("Calle 1")).to_be_visible()
        expect(self.page.get_by_text("123456789")).to_be_visible()
        expect(self.page.get_by_text("proveedor1@example.com")).to_be_visible()
        expect(self.page.get_by_text("Piso 1a")).to_be_visible()

        expect(self.page.get_by_text("Proveedor 2")).to_be_visible()
        expect(self.page.get_by_text("Calle 2")).to_be_visible()
        expect(self.page.get_by_text("987654321")).to_be_visible()
        expect(self.page.get_by_text("proveedor2@example.com")).to_be_visible()
        expect(self.page.get_by_text("Piso 1b")).to_be_visible()

    def test_should_show_add_provider_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        add_provider_action = self.page.get_by_role(
            "link", name="Nuevo proveedor", exact=False
        )
        expect(add_provider_action).to_have_attribute("href", reverse("providers_form"))

    def test_should_show_provider_edit_action(self):
        provider = Provider.objects.create(
            name="Proveedor 1",
            address="Calle 1",
            phone="543456780",
            email="proveedor1@example.com",
            floor_apartament="Piso 1a",
        )

        response = self.client.get(reverse('providers_repo'))
        self.assertTrue(response.status_code < 400)

    def test_should_show_provider_delete_action(self):
        # Crear un proveedor para verificar
        provider = Provider.objects.create(
            name="Proveedor 1",
            address="Calle 1",
            phone="123456789",
            email="proveedor1@example.com",
            floor_apartament="Piso 1a",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        # Esperar a que el formulario de eliminación esté presente
        edit_form = self.page.wait_for_selector(
            'form[name="Formulario de eliminación de proveedor"]',
            timeout=1000
        )

        # Verificar que el botón de eliminar sea visible
        delete_button = edit_form.wait_for_selector('button[name="Eliminar"]', timeout=1000)
        self.assertIsNotNone(delete_button)
        
    def test_should_can_be_able_to_delete_a_provider(self):
        Provider.objects.create(
            name="Proveedor 1",
            address="Calle 1",
            phone="123456789",
            email="proveedor1@example.com",
            floor_apartament="Piso 1a",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        expect(self.page.get_by_text("Proveedor 1")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("providers_delete"))

        
        with self.page.expect_response(is_delete_response) as response_info:
            # Usar query_selector para mayor precisión
            self.page.query_selector('button[name="Eliminar"]').click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Proveedor 1")).not_to_be_visible()


class ProviderCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_provider(self):
        self.page.goto(f"{self.live_server_url}{reverse('providers_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Proveedor Nuevo")
        self.page.get_by_label("Teléfono").fill("123456789")
        self.page.get_by_label("Email").fill("proveedor@example.com")
        self.page.get_by_label("Dirección").fill("Calle 123")
        self.page.get_by_label("Piso/Departamento").fill("Piso 1a")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Proveedor Nuevo")).to_be_visible()
        expect(self.page.get_by_text("123456789")).to_be_visible()
        expect(self.page.get_by_text("proveedor@example.com")).to_be_visible()
        expect(self.page.get_by_text("Calle 123")).to_be_visible()
        expect(self.page.get_by_text("Piso 1a")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('providers_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese si es una casa o el numero de piso del departamento")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Proveedor Nuevo")
        self.page.get_by_label("Teléfono").fill("123456789")
        self.page.get_by_label("Email").fill("proveedor")
        self.page.get_by_label("Dirección").fill("Calle 123")
        self.page.get_by_label("Piso/Departamento").fill("Calle 1a")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono")
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email valido")
        ).to_be_visible()

    def test_should_be_able_to_edit_a_provider(self):
        provider = Provider.objects.create(
            name="Proveedor Antiguo",
            address="Calle 456",
            phone="987654321",
            email="proveedor_antiguo@example.com",
            floor_apartament="casa",
        )

        path = reverse("providers_edit", kwargs={"id": provider.id})
        self.page.goto(f"{self.live_server_url}{path}")

        # modifico al proveedor
        self.page.get_by_label("Nombre").fill("Proveedor Modificado")
        self.page.get_by_label("Teléfono").fill("547654321")
        self.page.get_by_label("Email").fill("proveedor_modificado@example.com")
        self.page.get_by_label("Dirección").fill("Avenida Principal")
        self.page.get_by_label("Piso/Departamento").fill("Cabaña")
        self.page.get_by_role("button", name="Guardar").click()

        # me fijo que el provedor viejo no este
        expect(self.page.get_by_text("Proveedor Antiguo")).not_to_be_visible()
        expect(self.page.get_by_text("Calle 456")).not_to_be_visible()
        expect(self.page.get_by_text("987654321")).not_to_be_visible()
        expect(self.page.get_by_text("proveedor_antiguo@example.com")).not_to_be_visible()
        expect(self.page.get_by_text("casa")).not_to_be_visible()

        # me fijo que el provedor nuevo si este
        expect(self.page.get_by_text("Proveedor Modificado")).to_be_visible()
        expect(self.page.get_by_text("Avenida Principal")).to_be_visible()
        expect(self.page.get_by_text("547654321")).to_be_visible()
        expect(self.page.get_by_text("Cabaña")).to_be_visible()


class MedicineTest(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicines_repo')}")
        expect(self.page.get_by_text("No existen medicamentos")).to_be_visible()

    def test_should_show_medicines_data(self):
        Medicine.objects.create(
            name="Aspirina",
            description="Analgesico",
            dose=5.0,
        )

        Medicine.objects.create(
            name="Ibuprofeno",
            description="Antiinflamatorio",
            dose=7.5,
        )

        self.page.goto(f"{self.live_server_url}{reverse('medicines_repo')}")

        expect(self.page.get_by_text("No existen medicamentos")).not_to_be_visible()

        expect(self.page.get_by_text("Aspirina")).to_be_visible()
        expect(self.page.get_by_text("Analgesico")).to_be_visible()
        expect(self.page.get_by_text("5.0")).to_be_visible()

        expect(self.page.get_by_text("Ibuprofeno")).to_be_visible()
        expect(self.page.get_by_text("Antiinflamatorio")).to_be_visible()
        expect(self.page.get_by_text("7.5")).to_be_visible()

    def test_should_show_add_medicine_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicines_repo')}")

        add_medicine_action = self.page.get_by_role(
            "link", name="Nuevo Medicamento", exact=False
        )
        expect(add_medicine_action).to_have_attribute("href", reverse("medicines_form"))

    def test_should_show_medicine_delete_action(self):
        medicine = Medicine.objects.create(
            name="Aspirina",
            description="Analgesico",
            dose=5.0,
        )

        self.page.goto(f"{self.live_server_url}{reverse('medicines_repo')}")

        edit_form = self.page.query_selector('form[name="Formulario de eliminación de medicamento"]')
        
        medicine_id_input = edit_form.query_selector("input[name=medicine_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("medicines_delete"))
        expect(medicine_id_input).not_to_be_visible()
        expect(medicine_id_input).to_have_value(str(medicine.id))
        # Verificar que el botón "Eliminar" esté visible dentro del formulario
        expect(edit_form.query_selector('button[name="Eliminar"]')).to_be_visible()

    def test_should_can_be_able_to_delete_a_medicine(self):
        Medicine.objects.create(
            name="Aspirina",
            description="Analgesico",
            dose=5.0,
        )

        self.page.goto(f"{self.live_server_url}{reverse('medicines_repo')}")

        expect(self.page.get_by_text("Aspirina")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("medicines_delete"))

        # Esperar a que el botón de eliminar esté presente y visible
        delete_button = self.page.wait_for_selector('button[name="Eliminar"]', timeout=1000)

        with self.page.expect_response(is_delete_response) as response_info:
            # Hacer clic en el botón de eliminar
            delete_button.click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Aspirina")).not_to_be_visible()

    def test_should_be_able_to_create_a_new_medicine(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicines_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Paracetamol")
        self.page.get_by_label("Descripción").fill("Antipirético")
        self.page.get_by_label("Dosis").fill("7.5")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Paracetamol")).to_be_visible()
        expect(self.page.get_by_text("Antipirético")).to_be_visible()
        expect(self.page.get_by_text("7.5")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicines_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una descripción")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una dosis")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Paracetamol")
        self.page.get_by_label("Descripción").fill("Antipirético")
        self.page.get_by_label("Dosis").fill("15")
        self.page.get_by_role("button", name="Guardar").click()
        expect(self.page.get_by_text("Las dosis deben estar entre 1 y 10")).to_be_visible()

    def test_should_be_able_to_edit_a_medicine(self):
        medicine = Medicine.objects.create(
            name="Ibuprofeno",
            description="Antiinflamatorio",
            dose=7.5,
        )

        path = reverse("medicines_edit", kwargs={"id": medicine.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Naproxeno")
        self.page.get_by_label("Descripción").fill("Analgésico")
        self.page.get_by_label("Dosis").fill("5")

        self.page.get_by_role("button", name="Guardar").click()
        
        self.page.goto(f"{self.live_server_url}{reverse('medicines_repo')}")

        expect(self.page.get_by_text("Ibuprofeno")).not_to_be_visible()
        expect(self.page.get_by_text("Antiinflamatorio")).not_to_be_visible()
        expect(self.page.get_by_text("7.5")).not_to_be_visible()

        expect(self.page.get_by_text("Naproxeno")).to_be_visible()
        expect(self.page.get_by_text("Analgésico")).to_be_visible()
        expect(self.page.get_by_text("5")).to_be_visible()