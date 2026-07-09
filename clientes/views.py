from django.shortcuts import render
from .models import Customer
from ventas.models import Recarga


def consultar_cliente(request):
    datos = None
    recargas = []
    mensaje = ""

    if request.method == "POST":
        rut = request.POST.get("rut", "").strip()

        try:
            cliente = Customer.objects.get(document_number=rut)
            datos = {
                "rut": cliente.document_number,
                "nombre": f"{cliente.first_name} {cliente.last_name}",
            }
            recargas = Recarga.objects.filter(cliente_rut=rut).order_by("-created_at")
            if not recargas:
                mensaje = "El cliente no tiene recargas registradas."
        except Customer.DoesNotExist:
            mensaje = "Cliente no encontrado."

    return render(request, "clientes/consulta.html", {
        "datos": datos,
        "recargas": recargas,
        "mensaje": mensaje,
    })
