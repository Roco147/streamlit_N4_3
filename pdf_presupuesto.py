from fpdf import FPDF

NOMBRE_KIOSCO = "Kiosco Carlos Paz"
LOGO = "logo.png"

def renglon(pdf, texto, valor):
    pdf.cell(120, 9, texto)
    pdf.cell(0, 9, valor, align="R", new_x="LMARGIN", new_y="NEXT")

def armar_pdf(numero, fecha, cliente, producto, cantidad, precio, subtotal, descuento, iva, total):
    pdf = FPDF()
    pdf.add_page()

    # Encabezado (Punto 1 y 2 del wireframe)
    try:
        pdf.image(LOGO, x=10, y=10, w=28)
    except:
        pass

    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 12, NOMBRE_KIOSCO, align="R", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"Presupuesto N° {numero}", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Fecha: {fecha}", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)

    # Cliente y Producto (Puntos 3-4)
    pdf.set_font("Helvetica", "", 12)
    renglon(pdf, "Cliente", cliente)
    renglon(pdf, f"{cantidad} x {producto}", f"${precio:.2f} c/u")
    pdf.ln(5)

    # Subtotal, Descuento, IVA (Punto 5)
    renglon(pdf, "Subtotal", f"${subtotal:.2f}")
    renglon(pdf, "Descuento", f"-${descuento:.2f}")
    renglon(pdf, "IVA 21%", f"${iva:.2f}")

    # TOTAL en negrita (Punto 6)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(255, 140, 0)
    renglon(pdf, "TOTAL", f"${total:.2f}")
    pdf.set_text_color(0, 0, 0)

    # Pie (Punto 7)
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 6, "Presupuesto válido por 7 días.")

    return bytes(pdf.output())