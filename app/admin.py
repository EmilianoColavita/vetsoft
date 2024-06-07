from django.contrib import admin

from .models import Breed, City, Client, Pet, Vet

# Register your models here.
admin.site.register(Breed)
admin.site.register(City)
admin.site.register(Client)
admin.site.register(Pet)
admin.site.register(Vet)

