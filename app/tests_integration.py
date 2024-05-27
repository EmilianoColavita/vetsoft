from django.test import TestCase
from django.shortcuts import reverse
from app.models import Client, Medicine, Pet, Product, Vet, Provider
from datetime import date, datetime, timedelta


class HomePageTest(TestCase):
    def test_use_home_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")

class FormPagesTest(TestCase):
    def test_forms_template(self):

        response_clients_form = self.client.get(reverse("clients_form"))
        response_vets_form = self.client.get(reverse("vets_form"))
        response_providers_form = self.client.get(reverse("providers_form"))
        response_pets_form = self.client.get(reverse("pets_form"))

        # verifico los templates usados
        self.assertTemplateUsed(response_clients_form, "clients/form.html")
        self.assertTemplateUsed(response_vets_form, "vets/form.html")
        self.assertTemplateUsed(response_providers_form, "providers/form.html")
        self.assertTemplateUsed(response_pets_form, "pets/form.html")

class ClientsTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_repo_display_all_clients(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("clients_form"))
        self.assertTemplateUsed(response, "clients/form.html")

    def test_can_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

        self.assertRedirects(response, reverse("clients_repo"))

    def test_validation_errors_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")

    def test_should_response_with_404_status_if_client_doesnt_exists(self):
        response = self.client.get(reverse("clients_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_email(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")

    def test_edit_user_with_valid_data(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        response = self.client.post(
            reverse("clients_form"),
            data={
                "id": client.id,
                "name": "Guido Carrillo",
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.name, "Guido Carrillo")
        self.assertEqual(editedClient.phone, client.phone)
        self.assertEqual(editedClient.address, client.address)
        self.assertEqual(editedClient.email, client.email)


##### PROVEDOR #####

class ProviderIntegrationTest(TestCase):
    def test_can_create_provider_with_address(self):
        response = self.client.post(
            reverse("providers_form"),
            data={
                "name": "Proveedor XYZ",
                "phone": "987654321",
                "email": "proveedor@ejemplo.com",
                "address": "Calle 123",
                "floor_apartament": "casa",
            },
        )
        providers = Provider.objects.all()
        self.assertEqual(len(providers), 1)

        self.assertEqual(providers[0].name, "Proveedor XYZ")
        self.assertEqual(providers[0].phone, "987654321")
        self.assertEqual(providers[0].email, "proveedor@ejemplo.com")
        self.assertEqual(providers[0].address, "Calle 123")
        self.assertEqual(providers[0].floor_apartament, "casa")

        self.assertRedirects(response, reverse("providers_repo"))

    def test_validation_errors_create_provider(self):
        response = self.client.post(
            reverse("providers_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")
        self.assertContains(response, "Por favor ingrese una dirección")
        self.assertContains(response, "Por favor ingrese si es una casa o el numero de piso del departamento")

    def test_validation_invalid_email(self):
        response = self.client.post(
            reverse("providers_form"),
            data={
                "name": "Proveedor XYZ",
                "phone": "987654321",
                "email": "proveedorejemplo.com",  # Email inválido
                "address": "Calle 123",
                "floor_apartament": "casa",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")


####################### PET ##############################

class PetsIntegrationTest(TestCase):
  def test_cannot_create_pet_with_future_birthday(self):
    
    today = date.today()
    future_date = today + timedelta(days=1)
    pet_data = {
        "name": "Mascota Invalida",
        "breed": "Gato",
        "birthday": future_date.strftime("%Y-%m-%d"),
        "weight": 5.0,
    }

    response = self.client.post(reverse("pets_form"), data=pet_data)

    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "pets/form.html")

    pets = Pet.objects.all()
    self.assertEqual(len(pets), 0)