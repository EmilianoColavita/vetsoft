from django.test import TestCase
from django.shortcuts import reverse
from app.models import Breed, City, Client, Medicine, Pet, Product, Vet, Provider
from datetime import date, datetime, timedelta
from app.views import MedicineFormView, MedicineRepositoryView, PetFormView, VetFormView

class ViewTestCase(TestCase):
    def test_urls_are_correct(self):
        self.assertTrue(PetFormView.template_name, 'pets/form.html')
        self.assertTrue(VetFormView.template_name, 'vets/form.html')
        self.assertTrue(MedicineFormView.template_name, 'medicines/form.html')
        self.assertTrue(MedicineRepositoryView.template_name, 'medicines/repository.html')

    def test_can_go_pages(self):
        responses = []
        # Obtener URLs y respuestas para clientes
        r_client_repo = self.client.get(reverse('clients_repo'))
        r_client_form = self.client.get(reverse('clients_form'))
        responses.append(r_client_repo)
        responses.append(r_client_form)

        # Obtener URLs y respuestas para medicines
        r_medicine_repo = self.client.get(reverse('medicines_repo'))
        r_medicine_form = self.client.get(reverse('medicines_form'))
        responses.append(r_medicine_repo)
        responses.append(r_medicine_form)
        
        # Obtener URLs y respuestas para productos
        r_product_repo = self.client.get(reverse('products_repo'))
        r_product_form = self.client.get(reverse('products_form'))
        responses.append(r_product_repo)
        responses.append(r_product_form)
        
        # Obtener URLs y respuestas para vets
        r_vet_repo = self.client.get(reverse('vets_repo'))
        r_vet_form = self.client.get(reverse('vets_form'))
        responses.append(r_vet_repo)
        responses.append(r_vet_form)

        # Obtener URLs y respuestas para providers
        r_provider_repo = self.client.get(reverse('providers_repo'))
        r_provider_form = self.client.get(reverse('providers_form'))
        responses.append(r_provider_repo)
        responses.append(r_provider_form)
        
        # Valido las responses
        self.assertTrue(all((r.status_code < 400) for r in responses))
    
    def test_post_forms_urls_exists(self):
        responses = []
        # Obtener URLs y respuestas para clientes
        r_client_form = self.client.post(reverse('clients_form'))
        responses.append(r_client_form)

        # Obtener URLs y respuestas para medicines
        r_medicine_form = self.client.post(reverse('medicines_form'))
        responses.append(r_medicine_form)

        # Obtener URLs y respuestas para productos
        r_product_form = self.client.post(reverse('products_form'))
        responses.append(r_product_form)

        # Obtener URLs y respuestas para vets
        r_vet_form = self.client.post(reverse('vets_form'))
        responses.append(r_vet_form)

        # Obtener URLs y respuestas para providers
        r_provider_form = self.client.post(reverse('providers_form'))
        responses.append(r_provider_form)

        # Valido las responses
        self.assertTrue(all((r.status_code != 404) for r in responses))

class DeleteViewTestCase(TestCase):
    def setUp(self):
        # Crear objetos de prueba
        self.city1 = City.objects.create(name='Berisso')
        self.client1 = Client.objects.create(
            name="Juan Sebastián Veron",
            phone=54221555232,
            city=self.city1,
            email="brujita75@vetsoft.com",
        )
        
        self.product1 = Product.objects.create(
            name="Product 1",
            type="1",
            price=10.0
        )
        self.medicine1 = Medicine.objects.create(
            name="ibuprofeno",
            description="dscrp",
            dose=1.0
        )
        self.vet1 = Vet.objects.create(
            name = "vet1",
            phone = "54100",
            email = "v@vetsoft.com",
        )
        self.provider1 = Provider.objects.create(
            name = "prov1",
            phone = "54100",
            email = "v@vetsoft.com",
            address = "calle 1",
            floor_apartament = "1",
            )
        self.breed1 = Breed.objects.create(
            name = "Ovejero Aleman"
        )
        
        self.pet1 = Pet.objects.create(
            name = "Mascota Valida",
            breed = self.breed1,
            weight = 5.0,
            birthday = "2024-05-20"
        )

    def test_delete_client(self):
        response = self.client.post(reverse('clients_delete'), {'client_id': self.client1.id})
        self.assertEqual(response.status_code, 302)  # Redirección exitosa
        self.assertFalse(Client.objects.filter(id=self.client1.id).exists())  # Cliente eliminado

    def test_delete_product(self):
        response = self.client.post(reverse('products_delete'), {'product_id': self.product1.id})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(id=self.product1.id).exists())

    def test_delete_medicine(self):
        response = self.client.post(reverse('medicines_delete'), {'medicine_id': self.medicine1.id})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Medicine.objects.filter(id=self.medicine1.id).exists())

    def test_delete_vet(self):
        response = self.client.post(reverse('vets_delete'), {'vet_id': self.vet1.id})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Vet.objects.filter(id=self.vet1.id).exists())

    def test_delete_provider(self):
        response = self.client.post(reverse('providers_delete'), {'provider_id': self.provider1.id})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Provider.objects.filter(id=self.provider1.id).exists())

    def test_delete_pet(self):
        response = self.client.post(reverse('pets_delete'), {'pet_id': self.pet1.id})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Pet.objects.filter(id=self.pet1.id).exists())            

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
        City.objects.create(name='Berisso')
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "city": 1,
                "email": "brujita75@vetsoft.com",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, 54221555232)
        self.assertEqual(clients[0].city, City.objects.get(pk=1))
        self.assertEqual(clients[0].email, "brujita75@vetsoft.com")

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
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")

    def test_edit_user_with_valid_data(self):
        city = City.objects.create(name='Berisso')
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            phone=54221555232,
            city=city,
            email="brujita75@vetsoft.com",
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
        self.assertEqual(editedClient.city.id, city.id)
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

class MedicinesIntegrationTest(TestCase):
    def test_can_create_medicine_and_view_in_list(self):
        medicine_data = {
            'name': 'Ibuprofeno',
            'description': 'desc',
            'dose': 1.0
        }

        response = self.client.post(reverse('medicines_form'), data=medicine_data)
        self.assertTrue(response.status_code < 400)
        
    
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
