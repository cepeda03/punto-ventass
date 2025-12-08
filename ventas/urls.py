from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()

# API “bonita” (opcional para tu frontend; no afecta la web)
router.register(r"adoptantes", views.ClienteViewSet)
router.register(r"mascotas", views.ProductoViewSet)
router.register(r"solicitudes", views.EgresoViewSet)

urlpatterns = [
    # API REST
    path("api/", include(router.urls)),
    path("api/api-auth/", include("rest_framework.urls")),

    # JWT
    path(
        "api/token/",
        TokenObtainPairView.as_view(permission_classes=[AllowAny]),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(permission_classes=[AllowAny]),
        name="token_refresh",
    ),

    # WEB (mantengo los names antiguos para no romper templates)
    path("", views.adopciones_view, name="Venta"),
    path("clientes/", views.adoptantes_view, name="Clientes"),
    path("add_cliente/", views.add_adoptante_view, name="AddCliente"),
    path("edit_cliente/", views.edit_adoptante_view, name="EditCliente"),
    path("delete_cliente/", views.delete_adoptante_view, name="DeleteCliente"),

    path("productos/", views.mascotas_view, name="Productos"),
    path("add_producto/", views.add_mascota_view, name="AddProducto"),
    path("edit_producto/", views.edit_mascota_view, name="EditProduct"),
    path("delete_product/", views.delete_mascota_view, name="DeleteProduct"),

    path("add_venta/", views.add_adopcion.as_view(), name="AddVenta"),
    path("delete_venta/", views.delete_adopcion_view, name="DeleteVenta"),

    path("export/", views.export_pdf_view, name="ExportPDF"),
    path("export/<id>/<iva>/", views.export_pdf_view, name="ExportPDF"),

    # Rutas bonitas extra (opcionales)
    path("adopciones/", views.adopciones_view, name="Adopciones"),
    path("mascotas/", views.mascotas_view, name="Mascotas"),
    path("adoptantes/", views.adoptantes_view, name="Adoptantes"),
    path("solicitud/nueva/", views.add_adopcion.as_view(), name="NuevaSolicitud"),
]
