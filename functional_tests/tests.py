from datetime import date, timedelta
import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, expect, Browser

from django.urls import reverse

from app.models import Client, Medicine, Provider, Pet

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
    def test_should_have_navbar_with_links(self):
        self.page.goto(self.live_server_url)

        # Home
        navbar_home_link = self.page.get_by_test_id("navbar-Home")
        expect(navbar_home_link).to_be_visible()
        expect(navbar_home_link).to_have_text("Home")
        expect(navbar_home_link).to_have_attribute("href", self.live_server_url + reverse("home"))

        # Clientes
        navbar_clients_link = self.page.get_by_test_id("navbar-Clientes")
        expect(navbar_clients_link).to_be_visible()
        expect(navbar_clients_link).to_have_text("Clientes")
        expect(navbar_clients_link).to_have_attribute("href", self.live_server_url + reverse("clients_repo"))

        # Proveedores
        navbar_providers_link = self.page.get_by_test_id("navbar-Proveedores")
        expect(navbar_providers_link).to_be_visible()
        expect(navbar_providers_link).to_have_text("Proveedores")
        expect(navbar_providers_link).to_have_attribute("href", self.live_server_url + reverse("providers_repo"))

        # Medicinas
        navbar_medicines_link = self.page.get_by_test_id("navbar-Medicinas")
        expect(navbar_medicines_link).to_be_visible()
        expect(navbar_medicines_link).to_have_text("Medicinas")
        expect(navbar_medicines_link).to_have_attribute("href", self.live_server_url + reverse("medicines_repo"))

        # Productos
        navbar_products_link = self.page.get_by_test_id("navbar-Productos")
        expect(navbar_products_link).to_be_visible()
        expect(navbar_products_link).to_have_text("Productos")
        expect(navbar_products_link).to_have_attribute("href", self.live_server_url + reverse("products_repo"))

        # Veterinarias
        navbar_vets_link = self.page.get_by_test_id("navbar-Veterinarias")
        expect(navbar_vets_link).to_be_visible()
        expect(navbar_vets_link).to_have_text("Veterinarias")
        expect(navbar_vets_link).to_have_attribute("href", self.live_server_url + reverse("vets_repo"))

        # Mascotas
        navbar_pets_link = self.page.get_by_test_id("navbar-Mascotas")
        expect(navbar_pets_link).to_be_visible()
        expect(navbar_pets_link).to_have_text("Mascotas")
        expect(navbar_pets_link).to_have_attribute("href", self.live_server_url + reverse("pets_repo"))

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
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        Client.objects.create(
            name="Guido Carrillo",
            address="1 y 57",
            phone="221232555",
            email="goleador@gmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).not_to_be_visible()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

    def test_should_show_add_client_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo cliente", exact=False
        )
        expect(add_client_action).to_have_attribute("href", reverse("clients_form"))

    def test_should_show_client_edit_action(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )

    def test_should_show_client_delete_action(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de cliente"
        )
        client_id_input = edit_form.locator("input[name=client_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("clients_delete"))
        expect(client_id_input).not_to_be_visible()
        expect(client_id_input).to_have_value(str(client.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    #! No anda
    def test_should_can_be_able_to_delete_a_client(self):
        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("clients_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()


class ClientCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_client(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75@hotmail.com")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono")
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email valido")
        ).to_be_visible()

    def test_should_be_able_to_edit_a_client(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Teléfono").fill("221232555")
        self.page.get_by_label("Email").fill("goleador@gmail.com")
        self.page.get_by_label("Dirección").fill("1 y 57")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("13 y 44")).not_to_be_visible()
        expect(self.page.get_by_text("221555232")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).not_to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
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
            phone="123456789",
            email="proveedor1@example.com",
            floor_apartament="Piso 1a",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("providers_edit", kwargs={"id": provider.id})
        )

    def test_should_show_provider_delete_action(self):
        provider = Provider.objects.create(
            name="Proveedor 1",
            address="Calle 1",
            phone="123456789",
            email="proveedor1@example.com",
            floor_apartament="Piso 1a",
        )

        self.page.goto(f"{self.live_server_url}{reverse('providers_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de proveedor"
        )
        provider_id_input = edit_form.locator("input[name=provider_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("providers_delete"))
        expect(provider_id_input).not_to_be_visible()
        expect(provider_id_input).to_have_value(str(provider.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

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

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

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

        self.page.get_by_label("Nombre").fill("Proveedor Modificado")
        self.page.get_by_label("Teléfono").fill("987654321")
        self.page.get_by_label("Email").fill("proveedor_modificado@example.com")
        self.page.get_by_label("Dirección").fill("Avenida Principal")
        self.page.get_by_label("Piso/Departamento").fill("Cabaña")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Proveedor Antiguo")).not_to_be_visible()
        expect(self.page.get_by_text("Calle 456")).not_to_be_visible()
        expect(self.page.get_by_text("987654321")).not_to_be_visible()
        expect(self.page.get_by_text("proveedor_antiguo@example.com")).not_to_be_visible()
        expect(self.page.get_by_text("casa")).not_to_be_visible()

        expect(self.page.get_by_text("Proveedor Modificado")).to_be_visible()
        expect(self.page.get_by_text("Avenida Principal")).to_be_visible()
        expect(self.page.get_by_text("987654321")).to_be_visible()
        expect(self.page.get_by_text("Cabaña")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("providers_edit", kwargs={"id": provider.id})
        )

class MedicineTest(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicine_repo')}")
        expect(self.page.get_by_text("No existen medicinas")).to_be_visible()

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

        self.page.goto(f"{self.live_server_url}{reverse('medicine_repo')}")

        expect(self.page.get_by_text("No existen medicinas")).not_to_be_visible()

        expect(self.page.get_by_text("Aspirina")).to_be_visible()
        expect(self.page.get_by_text("Analgesico")).to_be_visible()
        expect(self.page.get_by_text("5.0")).to_be_visible()

        expect(self.page.get_by_text("Ibuprofeno")).to_be_visible()
        expect(self.page.get_by_text("Antiinflamatorio")).to_be_visible()
        expect(self.page.get_by_text("7.5")).to_be_visible()

    def test_should_show_add_medicine_action(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicine_repo')}")

        add_medicine_action = self.page.get_by_role(
            "link", name="Nueva medicina", exact=False
        )
        expect(add_medicine_action).to_have_attribute("href", reverse("medicine_form"))

    def test_should_show_medicine_edit_action(self):
        medicine = Medicine.objects.create(
            name="Aspirina",
            description="Analgesico",
            dose=5.0,
        )

        self.page.goto(f"{self.live_server_url}{reverse('medicine_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("medicine_edit", kwargs={"id": medicine.id})
        )

    def test_should_show_medicine_delete_action(self):
        medicine = Medicine.objects.create(
            name="Aspirina",
            description="Analgesico",
            dose=5.0,
        )

        self.page.goto(f"{self.live_server_url}{reverse('medicine_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de medicina"
        )
        medicine_id_input = edit_form.locator("input[name=medicine_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("medicine_delete"))
        expect(medicine_id_input).not_to_be_visible()
        expect(medicine_id_input).to_have_value(str(medicine.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_medicine(self):
        Medicine.objects.create(
            name="Aspirina",
            description="Analgesico",
            dose=5.0,
        )

        self.page.goto(f"{self.live_server_url}{reverse('medicine_repo')}")

        expect(self.page.get_by_text("Aspirina")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("medicine_delete"))

        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Aspirina")).not_to_be_visible()

    #! no anda
    def test_should_be_able_to_create_a_new_medicine(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicine_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Paracetamol")
        self.page.get_by_label("Descripción").fill("Antipirético")
        self.page.get_by_label("Dosis").fill("7.5")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Paracetamol")).to_be_visible()
        expect(self.page.get_by_text("Antipirético")).to_be_visible()
        expect(self.page.get_by_text("7.5")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        self.page.goto(f"{self.live_server_url}{reverse('medicine_form')}")

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

    #! no anda
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

        expect(self.page.get_by_text("Ibuprofeno")).not_to_be_visible()
        expect(self.page.get_by_text("Antiinflamatorio")).not_to_be_visible()
        expect(self.page.get_by_text("7.5")).not_to_be_visible()

        expect(self.page.get_by_text("Naproxeno")).to_be_visible()
        expect(self.page.get_by_text("Analgésico")).to_be_visible()
        expect(self.page.get_by_text("5")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("medicine_edit", kwargs={"id": medicine.id})
        )


####PET####
class PetTests(PlaywrightTestCase):
    def test_should_validate_pet_date_of_birth_less_than_today(self):
        today_date = date.today().strftime("%Y-%m-%d")

        self.page.goto(f"{self.live_server_url}{reverse('pet_create')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        pet_name_field = self.page.get_by_label("Nombre")
        pet_name_field.fill("Ian")

        pet_date_of_birth_field = self.page.get_by_label("Fecha de nacimiento")
        future_date = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")

        # Validate future date
        with self.page.expect_validation_error() as validation_error:
            pet_date_of_birth_field.fill(future_date)
            self.page.get_by_role("button", name="Guardar").click()
        expect(validation_error.got.message).to_contain(
            "La fecha de nacimiento de la mascota debe ser menor a la fecha actual"
        )

        # Enter a valid date in the past
        past_date = (date.today() - timedelta(days=365)).strftime("%Y-%m-%d")
        pet_date_of_birth_field.fill(past_date)
        self.page.get_by_role("button", name="Guardar").click()

        # Verify pet is created with valid date
        expect(self.page.get_by_text("Luna")).to_be_visible()
