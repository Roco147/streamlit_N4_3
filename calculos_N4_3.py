EFECTIVO = "Efectivo"
TRANSFERENCIA = "Transferencia"

def buscar_posicion(lista, nombre):
    for i in range(len(lista)):
        if lista[i] == nombre:
            return i
    return -1

def aplicar_descuento(monto, forma_pago):
    if forma_pago == EFECTIVO:
        return monto - (monto * 10 / 100)
    return monto

def calcular_iva(monto):
    return monto * 21 / 100