from django.forms import ValidationError
from django.test import TestCase, Client as DjangoClient
from django.urls import reverse
from app.models import Breed, Client, Medicine, Pet, Product, Provider
from app.views import ClientRepositoryView, ProviderFormView

class ClientModelTest(TestCase):

    def test_cant_create_user_with_not_valid_name(self):
            saved, errors = Client.save_client(
                {
                    # Invalid name
                    "name": "123323",
                    "phone": "54123321",
                    "address": "13 y 44",
                    "email": "brujita75@vetsoft.com",
                }
            )
            self.assertFalse(saved)
            self.assertIn('name', errors)

    def test_cant_create_user_with_not_numeric_phone(self):
        saved, errors = Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54Not a Number",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        self.assertFalse(saved)
        self.assertIn('phone', errors)

    def test_can_create_and_get_client(self):
        saved, errors = Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        self.assertTrue(saved)
        self.assertIsNone(errors)

        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, 54221555232)
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@vetsoft.com")

    def test_can_update_client(self):
        saved, errors = Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        self.assertTrue(saved)
        self.assertIsNone(errors)
        client = Client.objects.get(pk=1)
        self.assertEqual(client.phone, 54221555232)

        client.update_client({"phone": "54221555233"})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, 54221555233)


    def test_phone_must_start_with_54(self):
        success, errors = Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "44221555232",  # Número de teléfono que no comienza con '54'
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )

        self.assertFalse(success)
        self.assertIn("phone", errors)


class ClientViewsTest(TestCase):
    def setUp(self):
        self.clientView = DjangoClient()

    def test_client_repository_view(self):
        response = self.clientView.get(reverse('clients_repo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clients/repository.html')

##### PROVEDOR #####
class ProviderModelTest(TestCase):
    def test_can_create_and_get_provider(self):
        Provider.save_provider(
            {
                "name": "Proveedor ABC",
                "phone": "123456789",
                "email": "proveedor@example.com",
                "address": "Calle 123",
                "floor_apartament": "Piso 3c",
            }
        )
        providers = Provider.objects.all()
        self.assertEqual(len(providers), 1)

        self.assertEqual(providers[0].name, "Proveedor ABC")
        self.assertEqual(providers[0].phone, "123456789")
        self.assertEqual(providers[0].email, "proveedor@example.com")
        self.assertEqual(providers[0].address, "Calle 123")
        self.assertEqual(providers[0].floor_apartament, "Piso 3c")

    def test_can_update_provider(self):
        Provider.save_provider(
            {
                "name": "Proveedor ABC",
                "phone": "123456789",
                "email": "proveedor@example.com",
                "address": "Calle 123",
                "floor_apartament": "Piso 3c",
            }
        )
        provider = Provider.objects.get(pk=1)

        self.assertEqual(provider.floor_apartament, "Piso 3c")

        provider.update_provider({"floor_apartament": "casa"})

        provider_updated = Provider.objects.get(pk=1)

        self.assertEqual(provider_updated.floor_apartament, "casa")

    def test_update_provider_with_error(self):
        Provider.save_provider(
            {
                "name": "Proveedor ABC",
                "phone": "123456789",
                "email": "proveedor@example.com",
                "address": "Calle 123",
                "floor_apartament": "Piso 3c",
            }
        )
        provider = Provider.objects.get(pk=1)

        self.assertEqual(provider.floor_apartament, "Piso 3c")

        provider.update_provider({"floor_apartament": ""})

        provider_updated = Provider.objects.get(pk=1)

        self.assertEqual(provider_updated.floor_apartament, "Piso 3c")

class ProviderViewsTest(TestCase):
    def setUp(self):
        self.client = DjangoClient()

    def test_provider_repository_view(self):
        response = self.client.get(reverse('providers_repo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'providers/repository.html')

class ProductModelTest(TestCase):
    def test_invalid_price(self):
        result, errors = Product.save_product({
                "name": "Producto Invalido",
                "type": "Tipo",
                "price": -10.0,
            })
        self.assertEqual(result, False)
        self.assertDictEqual(errors, {'price': 'Los precios deben ser mayores que 0'})

    def test_valid_price(self):
        Product.save_product({
            "name": "Producto Valido",
            "type": "Tipo",
            "price": 10.0,
        })
        product = Product.objects.get(pk=1)
        self.assertEqual(product.price, 10.0)

class ProductModelTest(TestCase):
    def test_valid_price(self):
        result, errors = Product.save_product({
            "name": "Producto Valido",
            "type": "Tipo",
            "price": 10.0,
        })
        self.assertEqual(result, True)
        self.assertIsNone(errors)

    def test_invalid_price(self):
        result, errors = Product.save_product({
            "name": "Producto Invalido",
            "type": "Tipo",
            "price": -10.0,
        })
        self.assertEqual(result, False)
        self.assertDictEqual(errors, {'price': 'Los precios deben ser mayores que 0'})

class MedicineViewsTest(TestCase):
    def setUp(self):
        self.client = DjangoClient()

    def test_medicine_repository_view(self):
        response = self.client.get(reverse('medicines_repo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'medicines/repository.html')

class MedicineModelTest(TestCase):
    def test_invalid_dose(self):
        result, errors = Medicine.save_medicine({
            "name": "Medicina Invalida",
            "description": "Descripción",
            "dose": 0.5,
        })
        self.assertEqual(result, False)
        self.assertDictEqual(errors, {'dose': 'Las dosis deben estar entre 1 y 10'})

    def test_valid_dose(self):
        result, errors = Medicine.save_medicine({
            "name": "Medicina Valida",
            "description": "Descripción",
            "dose": 5.0,
        })
        self.assertEqual(result, True)
        self.assertIsNone(errors)

class BreedModelTest(TestCase):
    def test_can_create_breed(self):
        valid_name_1 = "Perro - Ovejero Aleman"
        Breed.objects.create(
            name = valid_name_1
        )

        valid_name_2 = "Gato - Persa"

        Breed.objects.create(
            name = valid_name_2
        )

        breeds = Breed.objects.all()
        self.assertEqual(len(breeds), 2)

        self.assertEqual(breeds[0].name, valid_name_1)
        self.assertEqual(breeds[1].name, valid_name_2)

class PetViewTest(TestCase):
    def setUp(self):
        self.client = DjangoClient()

    def test_breed_repository_view(self):
        response = self.client.get(reverse('pets_repo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pets/repository.html')

class PetModelTest(TestCase):
    def test_invalid_weight(self):
        Breed.objects.create(name='A')
        result, errors = Pet.save_pet({
            "name": "Mascota Invalida",
            "breed": 1,
            "weight": -5.0,
            "birthday": "2024-05-20",
        })
        self.assertEqual(result, False)
        self.assertDictEqual(errors, {'weight': 'El peso debe ser mayor que 0'})

    def test_valid_weight(self):
        Breed.objects.create(name='B')
        result, errors = Pet.save_pet({
            "name": "Mascota Valida",
            "breed": 1,
            "weight": 5.0,
            "birthday": "2024-05-20",
        })
        self.assertEqual(result, True)
        self.assertIsNone(errors)
