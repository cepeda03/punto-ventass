from django import forms
from .models import Cliente, Producto

class AddClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ("codigo", "nombre", "telefono")
        labels = {
            "codigo": "Código cliente: ",
            "nombre": "Nombre adoptante: ",
            "telefono": "Teléfono (Contacto): ",
        }

class EditarClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ("codigo", "nombre", "telefono")
        labels = {
            "codigo": "Código cliente: ",
            "nombre": "Nombre adoptante: ",
            "telefono": "Teléfono (Contacto): ",
        }
        widgets = {
            "codigo": forms.TextInput(attrs={"type": "text", "id": "codigo_editar"}),
            "nombre": forms.TextInput(attrs={"id": "nombre_editar"}),
            "telefono": forms.TextInput(attrs={"id": "telefono_editar"}),
        }

class AddProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ("codigo", "descripcion", "imagen", "costo", "precio", "cantidad")
        labels = {
            "codigo": "Cód. Barras: ",
            "descripcion": "Descripción de mascota: ",
            "imagen": "Imagen: ",
            "costo": "Costos (refugio) $: ",
            "precio": "Aporte sugerido $: ",
            "cantidad": "Cantidad: ",
        }

class EditarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ("codigo", "descripcion", "imagen", "costo", "precio", "cantidad")
        labels = {
            "codigo": "Cód. Barras: ",
            "descripcion": "Descripción de mascota: ",
            "imagen": "Imagen: ",
            "costo": "Costos (refugio) $: ",
            "precio": "Aporte sugerido $: ",
            "cantidad": "Cantidad: ",
        }
        widgets = {
            "codigo": forms.TextInput(attrs={"type": "text", "id": "codigo_editar"}),
            "descripcion": forms.TextInput(attrs={"id": "descripcion_editar"}),
            "costo": forms.TextInput(attrs={"id": "costo_editar"}),
            "precio": forms.TextInput(attrs={"id": "precio_editar"}),
            "cantidad": forms.TextInput(attrs={"id": "cantidad_editar"}),
        }
