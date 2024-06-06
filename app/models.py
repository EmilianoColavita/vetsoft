from datetime import date, datetime

from django.db import models


############################################## CLIENT ##############################################
class Client(models.Model):
    """
    Representa a un cliente con sus datos básicos.
    """
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    @classmethod
    def validate_client(cls, data):
        """validate a client by the data passed"""
        errors = {}

        name = data.get("name", "")
        phone = data.get("phone", "")
        email = data.get("email", "")

        if name == "":
            errors["name"] = "Por favor ingrese un nombre"

        if phone == "":
            errors["phone"] = "Por favor ingrese un teléfono"
        elif not phone.startswith('54'):
            errors["phone"] = "El teléfono debe comenzar con '54'"

        if email == "":
            errors["email"] = "Por favor ingrese un email"
        elif email.count("@") == 0:
            errors["email"] = "Por favor ingrese un email valido"
        elif not email.endswith("@vetsoft.com"):
            errors["email"] = 'El email debe finalizar con "@vetsoft.com"'

        return errors

    @classmethod
    def save_client(cls, client_data):
        """save a client"""
        errors = cls.validate_client(client_data)

        if len(errors.keys()) > 0:
            return False, errors

        Client.objects.create(
            name=client_data.get("name"),
            phone=client_data.get("phone"),
            email=client_data.get("email"),
            address=client_data.get("address"),
        )

        return True, None

    def update_client(self, client_data):
        """Passed a client, update it if not problem with data"""
        self.name = client_data.get("name", "") or self.name
        self.email = client_data.get("email", "") or self.email
        self.phone = client_data.get("phone", "") or self.phone
        self.address = client_data.get("address", "") or self.address

        errors = self.validate_client({
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
        })

        if len(errors.keys()) > 0:
            return False, errors

        self.save()
        return True, None

    def __str__(self):
        return self.name
####################################################################################################

############################################# PRODUCT ##############################################
class Product(models.Model):

    """
    Representa a un producto con sus datos básicos.
    """
    name = models.CharField(max_length=75)
    type = models.CharField(max_length=25)
    price = models.FloatField()

    @classmethod
    def save_product(cls, product_data: dict) -> tuple[bool, dict | None]:
        """Saves a product"""
        errors = cls.validate_product(product_data)

        if errors:
            return False, errors

        Product.objects.create(
            name=product_data.get("name"),
            type=product_data.get("type"),
            price=product_data.get("price"),
        )
        return True, None

    @classmethod
    def validate_product(cls, data: dict) -> dict | None:
        """Return the dict of text for the fields with errors (if exists any) None otherwise"""
        errors = {
            "name": "Por favor ingrese un nombre",
            "type": "Por favor ingrese un tipo",
            "price": "Por favor ingrese un precio",
        }
        for key in list(errors.keys()):
            # restrict values not null
            if data.get(key):
                errors.pop(key)

                # retrict price not negative
                if (key == 'price' and (float(data.get(key)) <= 0) ):
                    errors[key] = "Los precios deben ser mayores que 0"

        return errors or None

    def update_product(self, product_data: dict)  -> tuple[bool, dict | None]:
        """update a product if data passed is correct"""
        errors = self.validate_product(product_data)

        if errors:
            return False, errors

        self.name = product_data.get("name", self.name)
        self.type = product_data.get("type", self.type)
        self.price = product_data.get("price", self.price)
        self.save()
        return True, None

    def __str__(self):
        return self.name
####################################################################################################

############################################# MEDICINE #############################################
class Medicine(models.Model):
    """
    Representa a una medicina con sus datos básicos.
    """

    name = models.CharField(max_length=75)
    description = models.CharField(max_length=255)
    dose = models.FloatField()

    @classmethod
    def save_medicine(cls, medicine_data: dict) -> tuple[bool, dict | None]:
        """Save a medicine if data passed is correct"""
        errors = cls.validate_medicine(medicine_data)

        if errors:
            return False, errors

        Medicine.objects.create(
            name=medicine_data.get("name"),
            description=medicine_data.get("description"),
            dose=medicine_data.get("dose"),
        )
        return True, None

    @classmethod
    def validate_medicine(cls, data: dict) -> dict | None:
        """Validate that the passed data is correct"""

        errors = {
            "name": "Por favor ingrese un nombre",
            "description": "Por favor ingrese una descripción",
            "dose": "Por favor ingrese una dosis",
        }
        for key in list(errors.keys()):
            # restrict values not null
            if data.get(key):
                errors.pop(key)

                # restrict (1 < dosis < 10)
                if (key == 'dose' and not (1 <= float(data.get(key)) <= 10) ):
                    errors[key] = "Las dosis deben estar entre 1 y 10"
        return errors or None

    def update_medicine(self, medicine_data: dict) -> tuple[bool, dict | None]:
        """update a product if data passed is correct"""
        errors = self.validate_medicine(medicine_data)

        if errors:
            return False, errors

        self.name = medicine_data.get("name", self.name)
        self.description = medicine_data.get("description", self.description)
        self.dose = medicine_data.get("dose", self.dose)
        self.save()
        return True, None

    def __str__(self):
        return self.name
####################################################################################################

############################################### VET ################################################
class Vet(models.Model):
    """
    Representa a una veterinaria con sus datos básicos.
    """

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()


    @classmethod
    def validate_vet(cls, data):
        """Validate that the passed data is correct for a vet"""
        errors = {}

        name = data.get("name", "")
        phone = data.get("phone", "")
        email = data.get("email", "")

        if name == "":
            errors["name"] = "Por favor ingrese un nombre"

        if phone == "":
            errors["phone"] = "Por favor ingrese un teléfono"

        if email == "":
            errors["email"] = "Por favor ingrese un email"
        elif email.count("@") == 0:
            errors["email"] = "Por favor ingrese un email valido"

        return errors

    @classmethod
    def save_vet(cls, vet_data):
        """save a vet if data passed is correct"""
        errors = cls.validate_vet(vet_data)

        if len(errors.keys()) > 0:
            return False, errors

        Vet.objects.create(
            name=vet_data.get("name"),
            phone=vet_data.get("phone"),
            email=vet_data.get("email"),
        )
        return True, None

    def __str__(self):
        return self.name

    def update_vet(self, vet_data):
        """update a vet if data passed is correct"""
        self.name = vet_data.get("name", "") or self.name
        self.email = vet_data.get("email", "") or self.email
        self.phone = vet_data.get("phone", "") or self.phone

        self.save()
        return True, None

####################################################################################################

############################################# PROVIDER #############################################
class Provider(models.Model):
    """
    Representa a un proveedor con sus datos básicos.
    """

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)
    floor_apartament = models.CharField(max_length=100, blank=True) #1. Agregar un atributo para la dirección en la clase Provider. agrego localidad.

    def __str__(self):
        return self.name

    @classmethod
    def validate_provider(cls, data):
        """Validate that the passed data is correct for a provider"""
        errors = {}

        name = data.get("name", "")
        phone = data.get("phone", "")
        email = data.get("email", "")
        address = data.get("address", "")
        floor_apartament = data.get("floor_apartament", "")

        if name == "":
            errors["name"] = "Por favor ingrese un nombre"

        if phone == "":
            errors["phone"] = "Por favor ingrese un teléfono"

        if email == "":
            errors["email"] = "Por favor ingrese un email"
        elif email.count("@") == 0:
            errors["email"] = "Por favor ingrese un email valido"

        if address == "":
            errors["address"] = "Por favor ingrese una dirección"

        if floor_apartament == "":
            errors["floor_apartament"] = "Por favor ingrese si es una casa o el numero de piso del departamento"

        return errors

    @classmethod
    def save_provider(cls, provider_data):
        """save a provider if data passed is correct"""
        errors = cls.validate_provider(provider_data)

        if len(errors.keys()) > 0:
            return False, errors

        Provider.objects.create(
            name=provider_data.get("name"),
            phone=provider_data.get("phone"),
            email=provider_data.get("email"),
            address=provider_data.get("address"),
            floor_apartament=provider_data.get("floor_apartament"),
        )

        return True, None

    def update_provider(self, provider_data):
        """update a provider if data passed is correct"""
        self.name = provider_data.get("name", "") or self.name
        self.email = provider_data.get("email", "") or self.email
        self.phone = provider_data.get("phone", "") or self.phone
        self.address = provider_data.get("address", "") or self.address
        self.floor_apartament = provider_data.get("floor_apartament", "") or self.floor_apartament

        self.save()
        return True, None

####################################################################################################

############################################ BREED_PET #############################################
class Breed(models.Model):
    """
    Representa a los tipos de razas
    """
    name = models.CharField(max_length=50, unique=True)
    def _str_(self):
        return self.name

####################################################################################################

############################################### PET ################################################

class Pet(models.Model):
    """
    Representa a una mascota con sus datos básicos.
    """

    name = models.CharField(max_length=100)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    weight = models.FloatField(default=0.0)
    birthday = models.DateField()

    @classmethod
    def validate_pet(cls, data):
        """Validate that the passed data is correct for a pet"""
        errors = {}

        name = data.get("name", "")
        breed = data.get("breed", "")
        birthday = data.get("birthday", "")
        weight = data.get("weight", "")

        # Validar que la fecha de nacimiento sea menor a la fecha actual
        if birthday == "":
                errors["birthday"] = "Por favor ingrese una fecha"
        else:
            try:
                birthday_date = datetime.strptime(birthday, "%Y-%m-%d").date()
                if birthday_date >= date.today():
                    errors['birthday'] = 'La fecha de nacimiento debe ser anterior a la fecha actual.'
            except ValueError:
             errors['birthday'] = 'La fecha de nacimiento no es válida.'

        if name == "":
            errors["name"] = "Por favor ingrese un nombre"

        if breed == "":
            errors["breed"] = "Por favor ingrese una raza"

        if weight == "":
            errors["weight"] = "Por favor ingrese un peso"
        else:
            if (float(weight) < 0):
                errors["weight"] = "El peso debe ser mayor que 0"
        return errors

    @classmethod
    def save_pet(cls, pet_data):
        """save a product if data passed is correct for a pet"""
        errors = cls.validate_pet(pet_data)
        if len(errors.keys()) > 0:
            return False, errors

        Pet.objects.create(
            name=pet_data.get("name"),
            breed=Breed.objects.get(pk=pet_data.get("breed")),
            birthday=pet_data.get("birthday"),
            weight=pet_data.get("weight"),
        )

        return True, None

    def update_pet(self, pet_data):
        """update a pet if data passed is correct"""
        self.name = pet_data.get("name", "") or self.name
        self.breed = Breed.objects.get(pk=pet_data.get("breed")) or self.breed
        self.birthday = pet_data.get("birthday", "") or self.birthday

        self.save()
        return True, None

    def __str__(self):
        return self.name

####################################################################################################
