#***************************************************************************************#
# Función: verificarSeguridadMCU                                                        #
# Propósito: Verificar si determinado MCU está permitido según configuración de P00950  #
# Entrada:  mcu - centro de costos a verificar                                          #
#           inclusiva - tipo de seguridad, si el rango es inclusivo o exclusivo         #
#           rangoMCU - rango de centros de costos a los que está incluído o excluído    #
#           accionJDE - acción a validar (Alta, Baja, Modificacion, Consulta)           #
# Salida: True si tiene permitido el MCU, caso contrario False                          #
# VERSION: 1.1.0                                                                        #
#***************************************************************************************#
import logging

def verificarSeguridadMCU(mcu, accionJDE, inclusiva=False, rangoMCU=[]):

    mcuJust = mcu.rjust(12, ' ')

    acciones = {
        "A": "agregar",
        "C": "cambiar",
        "D": "borrar",
        "I": "lectura"
    }

    campoAccion = acciones.get(accionJDE)

    for item in rangoMCU:

        cc_desde = item.get("ccDesde", "").replace("*BLANKS", "").rjust(12, ' ')
        cc_hasta = item.get("ccHasta", "").replace("*BLANKS", "").rjust(12, ' ')

        if not cc_desde or not cc_hasta:
            continue

        if cc_desde <= mcuJust <= cc_hasta:
            #Inclusiva y Exclusiva se tratan de igual forma
            valor = item.get(campoAccion, "N")

            return valor == "Y"

    # Si no se encontró ningún rango:
    if inclusiva:
        # Seguridad inclusiva:
        # si no existe ningún rango aplicable, el acceso se deniega.
        return False

    # Seguridad exclusiva:
    # Si no existe ningún rango aplicable luego de aplicar la prioridad
    # Rol -> *PUBLIC, el acceso queda permitido.
    return True

# MIF OBSOLETA
def completarRequestSeguridad(json,accion):

    jsonCompleto = json
    # verificar si seguridad está activada
    if 'seguridadCCActivada' in jsonCompleto and jsonCompleto['seguridadCCActivada']:
        # verificar tipo de seguridad y determinar valor a buscar
        if 'seguridadInclusiva' in jsonCompleto and jsonCompleto['seguridadInclusiva']:
            jsonCompleto['valorAccionCC']='Y'
        else:
            jsonCompleto['valorAccionCC']='N'
        
        # asignar acción JDE
        jsonCompleto['accionJDE']=accion

    return jsonCompleto