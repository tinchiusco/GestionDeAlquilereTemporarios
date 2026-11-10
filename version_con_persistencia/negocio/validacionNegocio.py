from datetime import datetime


# Valido que la fecha exista en el calendario y tenga formato AAAA-MM-DD
def esFechaValida(fechaTexto):
    try:
        fecha = datetime.strptime(str(fechaTexto).strip(), "%Y-%m-%d")
        return 2000 <= fecha.year <= 2100
    except ValueError:
        return False


# Valido que la fecha de salida no sea anterior a la fecha de ingreso
def esRangoFechasValido(fechaInicioTexto, fechaFinTexto):
    try:
        fechaInicio = datetime.strptime(str(fechaInicioTexto).strip(), "%Y-%m-%d")
        fechaFin = datetime.strptime(str(fechaFinTexto).strip(), "%Y-%m-%d")
        return fechaFin >= fechaInicio
    except ValueError:
        return False


# Valido que el monto ingresado sea un numero positivo y no tenga letras
def esMontoValido(montoValor):
    try:
        numero = float(str(montoValor).strip())
        return numero > 0
    except ValueError:
        return False


# Valido que el DNI tenga solo numeros y entre 7 y 9 digitos
def esDniValido(dniTexto):
    if not isinstance(dniTexto, str):
        return False
    dniLimpio = dniTexto.strip()
    return dniLimpio.isdigit() and 7 <= len(dniLimpio) <= 9


# Valido que el telefono tenga solo numeros y al menos 6 digitos
def esTelefonoValido(telefonoTexto):
    if not isinstance(telefonoTexto, str):
        return False
    telefonoLimpio = telefonoTexto.strip()
    return telefonoLimpio.isdigit() and 6 <= len(telefonoLimpio) <= 15


# Valido que el email tenga un "@" y al menos un "." despues del "@"
def esEmailValido(emailTexto):
    if not isinstance(emailTexto, str):
        return False
    emailLimpio = emailTexto.strip()
    return "@" in emailLimpio and "." in emailLimpio.split("@")[-1]
