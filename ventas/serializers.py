from rest_framework import serializers
from .models import Cliente, Producto, Egreso

class Adoptanteserializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")


class EgresoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Egreso
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")
