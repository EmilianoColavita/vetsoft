from django.forms import ValidationError
from django.test import TestCase
from app.models import Client, Medicine, Pet, Product, Provider

class ClientModelTest(TestCase):
    def test_can_create_and_get_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

    def test_can_update_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": "221555233"})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555233")

    def test_update_client_with_error(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555232")

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

class PetModelTest(TestCase):
    def test_invalid_weight(self):
        result, errors = Pet.save_pet({
            "name": "Mascota Invalida",
            "breed": "Raza",
            "weight": -5.0,
            "birthday": "2024-05-20",
        })
        self.assertEqual(result, False)
        self.assertDictEqual(errors, {'weight': 'El peso debe ser mayor que 0'})

    def test_valid_weight(self):
        result, errors = Pet.save_pet({
            "name": "Mascota Valida",
            "breed": "Raza",
            "weight": 5.0,
            "birthday": "2024-05-20",
        })
        self.assertEqual(result, True)
        self.assertIsNone(errors)

########################### PET ##################################

class PetModelTest(TestCase):

    def test_save_pet_with_future_birthday_invalid(self):
        pet_data = {
            "name": "Test Pet",
            "breed": "Dog",
            "birthday": "2025-01-01",
            "weight": 10.0
        }

        success, errors = Pet.save_pet(pet_data)

        self.assertFalse(success)
        self.assertIn("La fecha de nacimiento debe ser anterior a la fecha actual.", errors.values())

    def test_save_pet_with_valid_birthday(self):
        pet_data = {
            "name": "Test Pet",
            "breed": "Dog",
            "birthday": "2023-01-01",
            "weight": 10.0
        }

        success, errors = Pet.save_pet(pet_data)

        self.assertTrue(success)
        self.assertIsNone(errors)