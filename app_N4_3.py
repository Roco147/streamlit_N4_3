import streamlit as st
from calculos_N4_3 import *
from pdf_presupuesto import *

productos = ["Alfajor", "Gaseosa", "Chicle", "Agua"]
precios = [1500, 2800, 500, 1800]

st.title("Kiosco Carlos Paz")

if "ingresado" not in st.session_state:
    st.session_state["ingresado"] = False
if "carrito" not in st.session_state:
    st.session_state["carrito"] = []

nombre = st.text_input("Nombre del cliente")

if st.button("Iniciar pedido"):
    if nombre:
        st.session_state["ingresado"] = True

if st.session_state["ingresado"]:
    st.subheader("Agregar producto")
    producto = st.selectbox("Producto", productos)
    cantidad = st.number_input("Cantidad", value=1, min_value=1)

    if st.button("Agregar al pedido"):
        pos = buscar_posicion(productos, producto)
        precio = precios[pos]
        subtotal_item = cantidad * precio
        st.session_state["carrito"].append({
            "producto": producto,
            "cantidad": cantidad,
            "precio": precio,
            "subtotal": subtotal_item
        })
        st.success(f"Se agregó {cantidad} x {producto}")

    if len(st.session_state["carrito"]) > 0:
        st.write("---")
        st.subheader(f"Resumen del pedido de {nombre}")

        subtotal_acumulado = 0
        for item in st.session_state["carrito"]:
            st.write(f"• {item['cantidad']} x {item['producto']} - ${item['subtotal']:.2f}")
            subtotal_acumulado += item["subtotal"]

        pago = st.radio("Forma de pago", [EFECTIVO, TRANSFERENCIA])

        con_desc = aplicar_descuento(subtotal_acumulado, pago)
        descuento = subtotal_acumulado - con_desc
        iva = calcular_iva(con_desc)
        total = con_desc + iva

        st.write(f"Subtotal total: ${subtotal_acumulado:.2f}")
        st.write(f"Descuento: -${descuento:.2f}")
        st.write(f"IVA: +${iva:.2f}")
        st.metric("TOTAL FINAL", f"${total:.2f}")

        fecha_hoy = "2026-10-07"
        
        # Se envían los datos consolidados al módulo de PDF
        resumen_texto = ", ".join([f"{i['cantidad']}x {i['producto']}" for i in st.session_state["carrito"]])

        archivo_pdf = armar_pdf(
            numero=1,
            fecha=fecha_hoy,
            cliente=nombre,
            producto=resumen_texto,
            cantidad=1,
            precio=subtotal_acumulado,
            subtotal=subtotal_acumulado,
            descuento=descuento,
            iva=iva,
            total=total
        )

        st.download_button(
            label="Descargar presupuesto (PDF)",
            data=archivo_pdf,
            file_name=f"presupuesto_{nombre}.pdf",
            mime="application/pdf"
        )