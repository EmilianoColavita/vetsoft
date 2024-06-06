from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import View
from django.views.generic import TemplateView

from .models import Breed, Client, Medicine, Pet, Product, Provider, Vet


def home(request):
    """gets homes view"""
    buttonsHome = [
        {'url': reverse("clients_repo"), 'id': 'home-Clientes', 'icon': 'bi-people', 'text': 'Clientes'},
        {'url': reverse("vets_repo"), 'id': 'home-Veterinarias', 'icon': 'bi-shop', 'text': 'Veterinarias'},
        {'url': reverse("products_repo"), 'id': 'home-Productos', 'icon': 'bi-basket', 'text': 'Productos'},
        {'url': reverse("medicines_repo"), 'id': 'home-Medicamentos', 'icon': 'bi-capsule', 'text': 'Medicamentos'},
        {'url': reverse("providers_repo"), 'id': 'home-Proveedores', 'icon': 'bi-truck', 'text': 'Proveedores'},
        {'url': reverse("pets_repo"), 'id': 'home-Mascotas', 'icon': 'bi-chat-heart', 'text': 'Mascotas'},
    ]

    return render(request, "home.html",context={'buttons': buttonsHome})

############################################# CLIENTS ##############################################
class ClientRepositoryView(View):
    """
    Vista para manejar el repositorio de clientes.

    """

    template_name = "clients/repository.html"

    def get(self, request):
        """gets a client/repo"""
        clients = Client.objects.all()
        return render(request, self.template_name, {"clients": clients})

class ClientFormView(View):
    """
    Vista para manejar el formulario de clientes.

    """

    template_name = "clients/form.html"

    def get(self, request, id=None):
        """gets a client/form"""
        client = None
        if id is not None:
            client = get_object_or_404(Client, pk=id)
        return render(request, self.template_name, {"client": client})

    def post(self, request, id=None):
        """saves a client"""
        client_id = request.POST.get("id", "")
        if client_id == "":
            saved, errors = Client.save_client(request.POST)
        else:
            client = get_object_or_404(Client, pk=client_id)
            saved, errors = client.update_client(request.POST)

        if saved:
            return redirect(reverse("clients_repo"))
        return render(request, self.template_name, {"errors": errors, "client": request.POST})

class ClientDeleteView(View):
    """
    Vista para manejar la eliminacion de clientes.

    """

    def post(self, request):
        """Deletes a client"""
        client_id = request.POST.get("client_id")
        client = get_object_or_404(Client, pk=int(client_id))
        client.delete()
        return redirect(reverse("clients_repo"))
####################################################################################################

############################################# PRODUCTS #############################################
class ProductRepositoryView(TemplateView):
    """
    Vista para manejar el repositorio del producto.
    """

    template_name = "products/repository.html"

    def get_context_data(self, **kwargs):
        """gets alls the products"""
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        return context

class ProductFormView(View):
    """
    Vista para manejar el formulario del producto.
    """

    template_name = "products/form.html"

    def get(self, request, id=None):
        """gets a product/form"""
        context = {}
        if id is not None:
            context["product"] = get_object_or_404(Product, pk=id)
        return render(request, self.template_name, context)

    def post(self, request, id=None):
        """save a product"""
        product_id = request.POST.get("id", "")
        if product_id == "":
            saved, errors = Product.save_product(request.POST)
        else:
            product = get_object_or_404(Product, pk=product_id)
            saved, errors = product.update_product(request.POST)

        if saved:
            return redirect(reverse("products_repo"))
        return render(request, self.template_name, {"errors": errors, "product": request.POST})

class ProductDeleteView(View):
    """
    Vista para manejar la eliminacion del producto.
    """

    def post(self, request):
        """Deletes a product"""
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, pk=int(product_id))
        product.delete()
        return redirect(reverse("products_repo"))
####################################################################################################

############################################ MEDICINAS #############################################

class MedicineRepositoryView(TemplateView):
    """
    Vista para manejar el repositorio de medicinas.
    """

    template_name = "medicines/repository.html"

    def get_context_data(self, **kwargs):
        """gets all the medicines"""
        context = super().get_context_data(**kwargs)
        context["medicines"] = Medicine.objects.all()
        return context

class MedicineFormView(View):
    """
    Vista para manejar el formulario de medicinas.
    """

    template_name = "medicines/form.html"

    def get(self, request, id=None):
        """gets a medicines/form"""
        context = {}
        if id is not None:
            context["medicine"] = get_object_or_404(Medicine, pk=id)
        return render(request, self.template_name, context)

    def post(self, request, id=None):
        """saves a medicine"""
        medicine_id = request.POST.get("id", "")
        if medicine_id == "":
            saved, errors = Medicine.save_medicine(request.POST)
        else:
            medicine = get_object_or_404(Medicine, pk=medicine_id)
            saved, errors = medicine.update_medicine(request.POST)

        if saved:
            return redirect(reverse("medicines_repo"))
        return render(request, self.template_name, {"errors": errors, "medicine": request.POST})

class MedicineDeleteView(View):
    """
    Vista para manejar la eliminacion de medicinas.
    """

    def post(self, request):
        """Deletes a medicine"""
        medicine_id = request.POST.get("medicine_id")
        medicine = get_object_or_404(Medicine, pk=int(medicine_id))
        medicine.delete()
        return redirect(reverse("medicines_repo"))
####################################################################################################

############################################# VETS #################################################
class VetRepositoryView(View):
    """
    Vista para manejar el repositorio de veterinarias.
    """

    def get(self, request):
        """gets a vets/repo"""
        vets = Vet.objects.all()
        return render(request, "vets/repository.html", {"vets": vets})

class VetFormView(View):
    """
    Vista para manejar el formulario de veterinarias.
    """

    template_name = "vets/form.html"

    def get(self, request, id=None):
        """gets a vets/form"""
        vet = None
        if id is not None:
            vet = get_object_or_404(Vet, pk=id)
        return render(request, self.template_name, {"vet": vet})

    def post(self, request, id=None):
        """saves a vet"""
        vet_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if vet_id == "":
            saved, errors = Vet.save_vet(request.POST)
        else:
            vet = get_object_or_404(Vet, pk=vet_id)
            saved, errors = vet.update_vet(request.POST)

        if saved:
            return redirect(reverse("vets_repo"))
        return render(request, self.template_name, {"errors": errors, "vet": request.POST})

class VetDeleteView(View):
    """
    Vista para manejar la eliminacion de veterinarias.
    """

    def post(self, request):
        """Deletes a vet"""
        vet_id = request.POST.get("vet_id")
        vet = get_object_or_404(Vet, pk=int(vet_id))
        vet.delete()
        return redirect(reverse("vets_repo"))
####################################################################################################

########################################### PROVEEDORES ############################################
class ProviderRepositoryView(View):
    """
    Vista para manejar el repositorio de proveedores.
    """

    def get(self, request):
        """gets a providers/repo"""
        providers = Provider.objects.all()
        return render(request, "providers/repository.html", {"providers": providers})

class ProviderFormView(View):
    """
    Vista para manejar el formulario de proveedores.
    """

    template_name = "providers/form.html"

    def get(self, request, id=None):
        """gets a providers/form"""

        provider = None

        if id is not None:
            provider = get_object_or_404(Provider, pk=id)
        return render(request, self.template_name, {"provider": provider})

    def post(self, request, id=None):
        """saves a provider"""
        provider_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if provider_id == "":
            saved, errors = Provider.save_provider(request.POST)
        else:
            provider = get_object_or_404(Provider, pk=provider_id)
            saved, errors = provider.update_provider(request.POST)

        if saved:
            return redirect(reverse("providers_repo"))
        return render(request, self.template_name, {"errors": errors, "provider": request.POST})

class ProviderDeleteView(View):
    """
    Vista para manejar la eliminacion de proveedores.
    """

    def post(self, request):
        """Deletes a provider"""
        provider_id = request.POST.get("provider_id")
        provider = get_object_or_404(Provider, pk=int(provider_id))
        provider.delete()
        return redirect(reverse("providers_repo"))
####################################################################################################

############################################### PETS ###############################################
class PetRepositoryView(View):
    """
    Vista para manejar el repositorio de mascotas.
    """

    def get(self, request):
        """gets a pets/repo"""

        pets = Pet.objects.all()
        return render(request, "pets/repository.html", {"pets": pets})

class PetFormView(View):
    """
    Vista para manejar el formulario de mascotas.
    """

    template_name = "pets/form.html"

    def get(self, request, id=None):
        """gets a pets/form"""

        pet = None
        breeds = Breed.objects.all()
        if id is not None:
            pet = get_object_or_404(Pet, pk=id)
        return render(request, self.template_name, {"pet": pet, "breeds": breeds})

    def post(self, request, id=None):
        """saves a pet"""
        pet_id = request.POST.get("id", "")
        errors = {}
        saved = True

        if pet_id == "":
            saved, errors = Pet.save_pet(request.POST)
        else:
            pet = get_object_or_404(Pet, pk=pet_id)
            saved, errors = pet.update_pet(request.POST)

        if saved:
            return redirect(reverse("pets_repo"))
        return render(request, self.template_name, {"errors": errors, "pet": request.POST})

class PetDeleteView(View):
    """
    Vista para manejar la eliminacion de mascotas.
    """

    def post(self, request):
        """Deletes a pet"""
        pet_id = request.POST.get("pet_id")
        pet = get_object_or_404(Pet, pk=int(pet_id))
        pet.delete()
        return redirect(reverse("pets_repo"))
####################################################################################################
