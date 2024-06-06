from django.urls import reverse

links = [
    {"label": "Home", "href": reverse("home"), "icon": "bi bi-house-door"},
    {"label": "Clientes", "href": reverse("clients_repo"), "icon": "bi bi-people"},
    {"label": "Veterinarias", "href": reverse("vets_repo"), "icon": "bi bi-shop"},
    {"label": "Productos", "href": reverse("products_repo"), "icon": "bi bi-basket"},
    {"label": "Medicamentos", "href": reverse("medicines_repo"), "icon": "bi bi-capsule"},
    {"label": "Proveedores", "href": reverse("providers_repo"), "icon": "bi bi-truck"},
    {"label": "Mascotas", "href": reverse("pets_repo"), "icon": "bi bi-chat-heart"},
]


def navbar(request):
    """navbar del home"""
    def add_active(link):
        copy = link.copy()

        if copy["href"] == "/":
            copy["active"] = request.path == "/"
        else:
            copy["active"] = request.path.startswith(copy.get("href", ""))

        return copy

    return {"links": map(add_active, links)}
