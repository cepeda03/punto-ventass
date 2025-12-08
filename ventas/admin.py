from django.contrib import admin
from .models import Cliente, Producto, Empresa

class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "telefono", "codigo")
    search_fields = ["nombre"]
    readonly_fields = ("created", "updated")

admin.site.register(Cliente, ClienteAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ("descripcion", "cantidad", "costo")
    search_fields = ["descripcion"]
    readonly_fields = ("created", "updated")

admin.site.register(Producto, ProductoAdmin)

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "domicilio", "telefono")
    readonly_fields = ("created", "updated")

admin.site.register(Empresa, EmpresaAdmin)
