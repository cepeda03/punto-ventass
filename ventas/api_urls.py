from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r"clientes", views.ClienteViewSet, basename="cliente")
router.register(r"productos", views.ProductoViewSet, basename="producto")
router.register(r"egresos", views.EgresoViewSet, basename="egreso")

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
