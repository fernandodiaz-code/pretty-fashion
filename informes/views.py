from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile
from xml.sax.saxutils import escape

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from pretty_fashion.decorators import admin_required
from ventas.models import Recarga
from datetime import datetime


@admin_required
def menu_informes(request):
    return render(request, "informes/menu.html")


@admin_required
def informe_recargas(request):
    recargas = []
    total = 0
    cantidad = 0
    fecha_inicio = ""
    fecha_fin = ""

    if request.method == "POST":
        fecha_inicio = request.POST.get("fecha_inicio", "")
        fecha_fin = request.POST.get("fecha_fin", "")

        try:
            qs = Recarga.objects.all()

            if fecha_inicio:
                fecha_i = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
                qs = qs.filter(created_at__date__gte=fecha_i)
            if fecha_fin:
                fecha_f = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
                qs = qs.filter(created_at__date__lte=fecha_f)

            recargas = qs.order_by("-created_at")
            total = sum(r.monto for r in recargas)
            cantidad = recargas.count()
        except ValueError:
            pass

    return render(request, "informes/recargas.html", {
        "recargas": recargas,
        "total": total,
        "cantidad": cantidad,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
    })


def _ventas_dia_actual():
    hoy = timezone.localdate()
    recargas = Recarga.objects.filter(created_at__date=hoy).order_by("created_at")
    total = sum(r.monto for r in recargas)
    cantidad = recargas.count()
    return hoy, recargas, total, cantidad


def _xlsx_cell(ref, value):
    if isinstance(value, int):
        return f'<c r="{ref}"><v>{value}</v></c>'
    return f'<c r="{ref}" t="inlineStr"><is><t>{escape(str(value))}</t></is></c>'


def _xlsx_row(numero, valores):
    celdas = []
    for indice, valor in enumerate(valores):
        columna = chr(ord("A") + indice)
        celdas.append(_xlsx_cell(f"{columna}{numero}", valor))
    return f'<row r="{numero}">{"".join(celdas)}</row>'


def _crear_xlsx_reporte_final_dia(fecha, recargas, total, cantidad):
    filas = [[
        "ID",
        "Fecha",
        "Peso",
        "Lugar",
        "Metodo de pago",
        "Pago mixto",
        "Monto pago 1",
        "Metodo pago 2",
        "Monto pago 2",
        "Precio base",
        "Descuento",
        "Total",
        "Comentario",
    ]]

    for recarga in recargas:
        filas.append([
            recarga.id,
            timezone.localtime(recarga.created_at).strftime("%d/%m/%Y %H:%M"),
            f"{recarga.galon_peso} kg",
            recarga.get_lugar_venta_display(),
            recarga.get_metodo_pago_display(),
            "Si" if recarga.pago_mixto else "No",
            recarga.monto_pago_1,
            recarga.get_metodo_pago_2_display() if recarga.pago_mixto else "",
            recarga.monto_pago_2,
            recarga.precio_base,
            recarga.descuento_total,
            recarga.monto,
            recarga.comentario,
        ])

    filas.append([])
    filas.append(["", "", "", "", "Cantidad", cantidad, "Total", total, ""])
    sheet_data = "".join(
        _xlsx_row(numero, fila)
        for numero, fila in enumerate(filas, start=1)
        if fila
    )

    worksheet = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
    <sheetViews><sheetView workbookViewId="0"/></sheetViews>
    <sheetFormatPr defaultRowHeight="15"/>
    <cols>
        <col min="1" max="13" width="18" customWidth="1"/>
    </cols>
    <sheetData>{sheet_data}</sheetData>
</worksheet>'''

    workbook = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
    <sheets>
        <sheet name="Reporte Final Dia" sheetId="1" r:id="rId1"/>
    </sheets>
</workbook>'''

    workbook_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>'''

    root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>'''

    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
    <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>'''

    archivo = BytesIO()
    with ZipFile(archivo, "w", ZIP_DEFLATED) as xlsx:
        xlsx.writestr("[Content_Types].xml", content_types)
        xlsx.writestr("_rels/.rels", root_rels)
        xlsx.writestr("xl/workbook.xml", workbook)
        xlsx.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        xlsx.writestr("xl/worksheets/sheet1.xml", worksheet)

    return archivo.getvalue()


@admin_required
def reporte_final_dia(request):
    hoy, recargas, total, cantidad = _ventas_dia_actual()
    return render(request, "informes/reporte_final_dia.html", {
        "fecha": hoy,
        "recargas": recargas,
        "total": total,
        "cantidad": cantidad,
    })


@admin_required
def descargar_reporte_final_dia(request):
    fecha, recargas, total, cantidad = _ventas_dia_actual()
    contenido = _crear_xlsx_reporte_final_dia(fecha, recargas, total, cantidad)
    response = HttpResponse(
        contenido,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = (
        f'attachment; filename="reporte-final-dia-{fecha:%Y-%m-%d}.xlsx"'
    )
    return response
