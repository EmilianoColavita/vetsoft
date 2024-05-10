from django.urls import path
from . import views

urlpatterns = [
    # Ruta raíz
    path("", view=views.home, name="home"),

    #CLIENTES
    path("clientes/", view=views.clients_repository, name="clients_repo"),
    path("clientes/nuevo/", view=views.clients_form, name="clients_form"),
    path("clientes/editar/<int:id>/", view=views.clients_form, name="clients_edit"),
    path("clientes/eliminar/", view=views.clients_delete, name="clients_delete"),

    #PRODUCTOS
    path("productos/", views.ProductRepositoryView.as_view(), name="products_repo"),
    path("productos/nuevo/", views.ProductFormView.as_view(), name="products_create"),
    path("productos/editar/<int:id>/", views.ProductFormView.as_view(), name="products_edit"),
    path("productos/eliminar/", views.ProductDeleteView.as_view(), name="products_delete"),

    #VETERINARIAS
    path("veterinarias/", view=views.vets_repository, name="vets_repo"),
    path("veterinarias/nuevo/", view=views.vets_form, name="vets_form"),
    path("veterinarias/editar/<int:id>/", view=views.vets_form, name="vets_edit"),
    path("veterinarias/eliminar/", view=views.vets_delete, name="vets_delete"),

    #MEDICAMENTOS
    path("medicamentos/", views.MedicineRepositoryView.as_view(), name="medicines_repo"),
    path("medicamentos/nuevo/", views.MedicineFormView.as_view(), name="medicines_create"),
    path("medicamentos/editar/<int:id>/", views.MedicineFormView.as_view(), name="medicines_edit"),
    path("medicamentos/eliminar/", views.MedicineDeleteView.as_view(), name="medicines_delete"),

    #PROVEEDORES
    path("proveedores/", view=views.ProviderRepositoryView.as_view(), name="providers_repo"),
    path("proveedores/nuevo/", view=views.ProviderFormView.as_view(), name="providers_form"),
    path("proveedores/editar/<int:id>/", view=views.ProviderFormView.as_view(), name="providers_edit"),
    path("proveedores/eliminar/", view=views.ProviderDeleteView.as_view(), name="providers_delete"),

    #MASCOTAS
    path("mascotas/", view=views.PetRepositoryView.as_view(), name="pets_repo"),
    path("mascotas/nueva/", view=views.PetFormView.as_view(), name="pets_form"),
    path("mascotas/editar/<int:id>/", view=views.PetFormView.as_view(), name="pets_edit"),
    path("mascotas/eliminar/", view=views.PetDeleteView.as_view(), name="pets_delete"),
]
