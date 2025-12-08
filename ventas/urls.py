from django.urls import path
from . import views

urlpatterns = [
    path("", views.adopciones_view, name="Venta"),

    path("clientes/", views.adoptantes_view, name="Clientes"),
    path("add_cliente/", views.add_adoptante_view, name="AddCliente"),
    path("edit_cliente/", views.edit_adoptante_view, name="EditCliente"),
    path("delete_cliente/", views.delete_adoptante_view, name="DeleteCliente"),

    path("productos/", views.mascotas_view, name="Productos"),
    path("add_producto/", views.add_mascota_view, name="AddProducto"),
    path("edit_producto/", views.edit_mascota_view, name="EditProducto"),
    path("delete_producto/", views.delete_mascota_view, name="DeleteProducto"),

    path("add_venta/", views.add_adopcion.as_view(), name="AddVenta"),
    path("delete_venta/", views.delete_adopcion_view, name="DeleteVenta"),

    path("ticket/<int:id>/<str:iva>/", views.export_pdf_view, name="Ticket"),
]
