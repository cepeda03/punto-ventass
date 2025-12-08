from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
import json

from .models import Cliente, Egreso, Producto, ProductosEgreso
from .forms import (
    AddClienteForm, EditarClienteForm,
    AddProductoForm, EditarProductoForm
)

from rest_framework import viewsets, permissions
from .serializers import Adoptanteserializer, ProductoSerializer, EgresoSerializer


# -----------------------------
# API (sin cambios en modelos)
# -----------------------------

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by("id")
    serializer_class =Adoptanteserializer
    permission_classes = [permissions.IsAuthenticated]


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by("id")
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]


class EgresoViewSet(viewsets.ModelViewSet):
    queryset = Egreso.objects.all().order_by("id")
    serializer_class = EgresoSerializer
    permission_classes = [permissions.IsAuthenticated]


# -----------------------------
# Vistas Web (renombrado UI)
# -----------------------------

def adopciones_view(request):
    """
    Listado de adopciones / solicitudes (modelo real: Egreso)
    """
    adopciones = Egreso.objects.all()
    num_adopciones = adopciones.count()
    context = {
        "Solicitudes": adopciones,          # compatibilidad si tu template usa Solicitudes
        "num_Solicitudes": num_adopciones,  # compatibilidad
        "adopciones": adopciones,
        "num_adopciones": num_adopciones
    }
    return render(request, "Solicitudes.html", context)


def adoptantes_view(request):
    """
    Adoptantes (modelo real: Cliente)
    """
    adoptantes = Cliente.objects.all()
    form_add = AddClienteForm()
    form_editar = EditarClienteForm()
    context = {
        "Adoptantes": adoptantes,  # compatibilidad
        "adoptantes": adoptantes,
        "form_personal": form_add,
        "form_editar": form_editar,
    }
    return render(request, "Adoptantes.html", context)


def add_adoptante_view(request):
    if request.method == "POST":
        form = AddClienteForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Adoptante guardado correctamente")
            except Exception:
                messages.error(request, "Error al guardar el adoptante")
        else:
            messages.error(request, "Formulario inválido")
    return redirect("Adoptantes")


def edit_adoptante_view(request):
    if request.method == "POST":
        adoptante = Cliente.objects.get(pk=request.POST.get("id_personal_editar"))
        form = EditarClienteForm(request.POST, request.FILES, instance=adoptante)
        if form.is_valid():
            form.save()
            messages.success(request, "Adoptante actualizado correctamente")
        else:
            messages.error(request, "Formulario inválido")
    return redirect("Adoptantes")


def delete_adoptante_view(request):
    if request.method == "POST":
        adoptante = Cliente.objects.get(pk=request.POST.get("id_personal_eliminar"))
        adoptante.delete()
        messages.success(request, "Adoptante eliminado")
    return redirect("Adoptantes")


def mascotas_view(request):
    """
    Mascotas disponibles (modelo real: Producto)
    """
    mascotas = Producto.objects.all()
    form_add = AddProductoForm()
    form_editar = EditarProductoForm()
    context = {
        "productos": mascotas,  # compatibilidad
        "mascotas": mascotas,
        "form_add": form_add,
        "form_editar": form_editar
    }
    return render(request, "productos.html", context)


def add_mascota_view(request):
    if request.method == "POST":
        form = AddProductoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Mascota registrada correctamente")
            except Exception:
                messages.error(request, "Error al registrar la mascota")
        else:
            messages.error(request, "Formulario inválido")
    return redirect("Productos")


def edit_mascota_view(request):
    if request.method == "POST":
        mascota = Producto.objects.get(pk=request.POST.get("id_producto_editar"))
        form = EditarProductoForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, "Mascota actualizada correctamente")
        else:
            messages.error(request, "Formulario inválido")
    return redirect("Productos")


def delete_mascota_view(request):
    if request.method == "POST":
        mascota = Producto.objects.get(pk=request.POST.get("id_producto_eliminar"))
        mascota.delete()
        messages.success(request, "Mascota eliminada")
    return redirect("Productos")


def delete_adopcion_view(request):
    """
    Eliminar solicitud/adopción (modelo real: Egreso)
    """
    if request.method == "POST":
        adopcion = Egreso.objects.get(pk=request.POST.get("id_producto_eliminar"))
        adopcion.delete()
        messages.success(request, "Solicitud eliminada")
    return redirect("Venta")


class add_adopcion(ListView):
    """
    Registrar solicitud/adopción (modelo real: Egreso)
    """
    template_name = "add_Solicitudes.html"
    model = Egreso

    def post(self, request, *args, **kwargs):
        try:
            action = request.POST.get("action")

            # Autocomplete de mascotas (Producto)
            if action == "autocomplete":
                data = []
                term = request.POST.get("term", "")
                for i in Producto.objects.filter(descripcion__icontains=term)[0:10]:
                    item = i.toJSON()
                    item["value"] = i.descripcion
                    data.append(item)
                return JsonResponse(data, safe=False)

            # Guardar solicitud
            elif action == "save":
                total_aporte = (
                    float(request.POST.get("efectivo", 0)) +
                    float(request.POST.get("tarjeta", 0)) +
                    float(request.POST.get("transferencia", 0)) +
                    float(request.POST.get("vales", 0)) +
                    float(request.POST.get("otro", 0))
                )

                fecha = request.POST.get("fecha")
                id_adoptante = request.POST.get("id_cliente")
                adoptante_obj = Cliente.objects.get(pk=int(id_adoptante))

                datos = json.loads(request.POST.get("verts", "{}"))
                total = float(datos.get("total", 0))
                mascotas = datos.get("productos", [])

                ticket = int(request.POST.get("ticket", 0)) == 1
                desglosar_iva = int(request.POST.get("desglosar", 0)) == 1
                observaciones = request.POST.get("comentarios", "")

                nueva_solicitud = Egreso.objects.create(
                    fecha_pedido=fecha,
                    cliente=adoptante_obj,
                    total=total,
                    pagado=total_aporte,
                    comentarios=observaciones,
                    ticket=ticket,
                    desglosar=desglosar_iva,
                )

                for p in mascotas:
                    mascota = Producto.objects.get(pk=int(p["id"]))
                    ProductosEgreso.objects.create(
                        egreso=nueva_solicitud,
                        producto=mascota,
                        cantidad=float(p.get("cantidad", 1)),
                        precio=float(p.get("precio", mascota.precio)),
                        subtotal=float(p.get("subtotal", 0)),
                        iva=float(p.get("iva", 0)),
                    )

                # ✅ IMPORTANTE: tu JS espera [id, true, iva]
                return JsonResponse([nueva_solicitud.id, True, str(desglosar_iva)], safe=False)

            else:
                return JsonResponse({"error": "Acción no válida"}, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productos_lista"] = Producto.objects.all()  # compatibilidad
        context["Adoptantes"] = Cliente.objects.all()    # compatibilidad
        context["mascotas_lista"] = Producto.objects.all()
        context["adoptantes_lista"] = Cliente.objects.all()
        return context


def export_pdf_view(request, id=None, iva=None):
    """
    Genera comprobante (ticket.html). OJO: genera HTML con content_type PDF (como tu base).
    """
    if id is None or iva is None:
        return redirect("Venta")

    template = get_template("ticket.html")
    subtotal = 0
    iva_suma = 0

    solicitud = Egreso.objects.get(pk=int(id))
    items = ProductosEgreso.objects.filter(egreso=solicitud)

    for i in items:
        subtotal += float(i.subtotal)
        iva_suma += float(i.iva)

    # ✅ empresa como dict para que ticket.html use empresa.nombre/moneda/etc
    empresa = {
        "nombre": "Fundación / Refugio",
        "domicilio": "Dirección del refugio",
        "telefono": "+56 9 0000 0000",
        "moneda": "$",
        "imagen": None,
    }

    context = {
        "num_ticket": id,
        "iva": iva,
        "fecha": solicitud.fecha_pedido,
        "cliente": solicitud.cliente.nombre,
        "items": items,
        "total": solicitud.total,
        "empresa": empresa,
        "comentarios": solicitud.comentarios,
        "subtotal": subtotal,
        "iva_suma": iva_suma,
    }

    html_template = template.render(context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; comprobante.pdf"
    response.write(html_template)
    return response
