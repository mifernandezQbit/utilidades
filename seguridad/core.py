#***************************************************************************************#
# Función: verificarSeguridadMCU                                                        #
# Propósito: Verificar si determinado MCU está permitido según configuración de P00950  #
# Entrada:  mcu - centro de costos a verificar                                          #
#           inclusiva - tipo de seguridad, si el rango es inclusivo o exclusivo         #
#           rangoMCU - rango de centros de costos a los que está incluído o excluído    #
# Salida: True si tiene permitido el MCU, caso contrario False                          #
# VERSION: 1.0.0                                                                        #
#***************************************************************************************#
def verificarSeguridadMCU(mcu,inclusiva=False, rangoMCU=[],):
    # Normalizamos el valor ingresado
    mcu = mcu.strip()
    existe = False
    # iteramos sobre los rangos hasta encontrar uno
    for item in rangoMCU:
        cc_desde = item.get("ccDesde", "").strip()
        cc_hasta = item.get("ccHasta", "").strip()

        # Si el rango está vacío, continuamos
        if not cc_desde or not cc_hasta:
            continue

        # Comparación alfabética (string)
        if cc_desde <= mcu <= cc_hasta:
            existe=True
            break

    # Dependiendo si es inclusiva o exclusiva respondemos 
    return existe if inclusiva else not existe