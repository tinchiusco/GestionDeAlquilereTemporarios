from negocio import propietarioNegocio
from negocio import propiedadNegocio
from negocio import estadiaNegocio
from negocio import egresoNegocio
from negocio import liquidacionNegocio



# menu principal en consola
def menuPrincipal(cotizacionActual):
    while True:
        print("------Sistema GAT------ \nMenu de opciones:\n1. Menu Propietarios \n2. Menu Propiedades \n3. Traer liquidaciones \n4. Salir ")
        try:
            opcionMenuPpal = int(input("Ingrese una opción: ").strip())
        except ValueError:
            print("Error: Debe ingresar un número válido.")
            continue 

        if opcionMenuPpal == 1:
            menuPropietarios()
        elif opcionMenuPpal == 2:
            menuPropiedades(cotizacionActual)
        elif opcionMenuPpal == 3:
            menuLiquidaciones()
        elif opcionMenuPpal == 4:
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Por favor, ingrese una opción válida.")


# Menu por consola para crear, actualizar o eliminar propietarios
def menuPropietarios():
    print("------Menu Propietarios------")
    try:
        opcionPropietario = int(input("1. Crear Propietario \n2. Actualizar Propietario \n3. Eliminar Propietario \n4. Volver al menu principal\nIngrese una opción: ").strip())
    except ValueError:
        print("Error: Debe ingresar un número válido.")
        return

    # Traigo todas las propiedades desde mysql
    propiedades = propiedadNegocio.obtenerPropiedades()

    if opcionPropietario == 1:
        nombre = input("Ingrese el nombre del propietario: ").strip()
        apellido = input("Ingrese el apellido del propietario: ").strip()
        telefono = input("Ingrese el teléfono del propietario: ").strip()
        email = input("Ingrese el email del propietario: ").strip()
        dni = input("Ingrese el DNI del propietario: ").strip()

        propiedadesSeleccionadas = []
        if len(propiedades) > 0:
            print("\n--------------------Propiedades disponibles:---------------------")
            for i, propiedad in enumerate(propiedades):
                print(f"{i + 1}. {propiedad}")
            try:
                eleccion = int(input("Seleccione la propiedad que desea asignar al propietario (0 para ninguna): ").strip() or 0)
                if 1 <= eleccion <= len(propiedades):
                    propiedadesSeleccionadas.append(propiedades[eleccion - 1])
                elif eleccion != 0:
                    print("Error: Número de propiedad fuera de rango.")
                    return
            except ValueError:
                print("Error: Debe ingresar un número válido para la propiedad.")
                return

        propietario = propietarioNegocio.crearPropietario(nombre, apellido, telefono, email, dni, propiedadesSeleccionadas)
        if propietario is None:
            print("\nError: Datos inválidos (verifique DNI de 7-9 dígitos, teléfono numérico, email con '@' y '.') o el DNI ya existe.")
        else:
            print("\nPropietario creado correctamente:")
            print(propietarioNegocio.obtenerDatos(propietario))

    elif opcionPropietario == 2:
        print("\n------ Actualizar Propietario ------")
        dniBuscar = input("Ingrese el DNI del propietario a actualizar: ").strip()
        # Traigo el propietario desde mysql buscando por su DNI
        propietario = propietarioNegocio.buscarPropietarioPorDni(dniBuscar)

        if propietario is None:
            print("\nNo existe un propietario con ese DNI (o el formato de DNI es inválido).")
            return

        propiedadesActualesTexto = ", ".join([p.getNombre() for p in propietario.getPropiedades()]) if propietario.getPropiedades() else "Sin asignar"
        print("\nPropietario encontrado:")
        print(f"Nombre: {propietario.getNombre()}")
        print(f"Apellido: {propietario.getApellido()}")
        print(f"Telefono: {propietario.getTelefono()}")
        print(f"Email: {propietario.getEmail()}")
        print(f"DNI: {propietario.getDni()}")
        print(f"Propiedades asignadas: {propiedadesActualesTexto}")

        print("\nIngrese los nuevos datos.")
        print("(Presione ENTER para mantener el valor actual)\n")

        nombre = input(f"Nombre [{propietario.getNombre()}]: ").strip() or propietario.getNombre()
        apellido = input(f"Apellido [{propietario.getApellido()}]: ").strip() or propietario.getApellido()
        telefono = input(f"Telefono [{propietario.getTelefono()}]: ").strip() or propietario.getTelefono()
        email = input(f"Email [{propietario.getEmail()}]: ").strip() or propietario.getEmail()
        dni = input(f"DNI [{propietario.getDni()}]: ").strip() or propietario.getDni()

        print("\nPropiedades disponibles:")
        for i, propiedad in enumerate(propiedades):
            print(f"{i + 1}. {propiedad}")

        try:
            eleccion = int(input("\nSeleccione una propiedad para asignarle (0 para mantener las actuales): ").strip() or 0)
        except ValueError:
            print("Error: Debe ingresar un número válido.")
            return

        propiedadesActualizadas = propietario.getPropiedades()
        if eleccion != 0:
            if 1 <= eleccion <= len(propiedades):
                propiedadSeleccionada = propiedades[eleccion - 1]
                # Evito duplicar en la lista si ya la tenia asignada
                if all(p.getId() != propiedadSeleccionada.getId() for p in propiedadesActualizadas):
                    propiedadesActualizadas.append(propiedadSeleccionada)
            else:
                print("Error: Número de propiedad fuera de rango.")
                return

        actualizado = propietarioNegocio.actualizarPropietario(propietario, nombre, apellido, telefono, email, dni, propiedadesActualizadas)
        if actualizado:
            print("\nPropietario actualizado correctamente.")
            print("\nDatos actualizados:")
            print(propietarioNegocio.obtenerDatos(propietario))
        else:
            print("\nError: Datos inválidos (verifique DNI de 7-9 dígitos, teléfono numérico y email válido).")

    elif opcionPropietario == 3:
        print("\n------ Eliminar Propietario ------")
        dniEliminar = input("Ingrese el DNI del propietario a eliminar: ").strip()
        if propietarioNegocio.eliminarPropietario(dniEliminar):
            print("Propietario eliminado correctamente.")
        else:
            print("No se encontró un propietario con ese DNI.")

    elif opcionPropietario == 4:
        return

    else:
        print("Opción no válida. Por favor, ingrese una opción válida.")


# Menu por consola para gestionar propiedades y registrar estadias o egresos
def menuPropiedades(cotizacionActual):
    print("------Menu Propiedades------")
    try:
        opcionPropiedad = int(input("1. Crear Propiedad \n2. Actualizar Propiedad \n3. Eliminar Propiedad \n4. Registrar Estadía \n5. Registrar Egreso \n6. Volver al menu principal\nIngrese una opción: ").strip())
    except ValueError:
        print("Error: Debe ingresar un número válido.")
        return

    # Traigo todas las propiedades desde mysql
    propiedades = propiedadNegocio.obtenerPropiedades()

    if opcionPropiedad == 1:
        nombre = input("Ingrese el nombre de la propiedad: ").strip()
        direccion = input("Ingrese la dirección de la propiedad: ").strip()
        tipo = input("Ingrese el tipo de propiedad (Casa, Departamento, Local, etc.): ").strip()
        descripcion = input("Ingrese una descripción de la propiedad: ").strip()

        propiedad = propiedadNegocio.crearPropiedad(nombre, direccion, tipo, descripcion)
        if propiedad is None:
            print("\nError: El nombre y la dirección son obligatorios y el nombre no puede estar repetido.")
        else:
            print("\nPropiedad creada correctamente:")
            print(propiedadNegocio.obtenerPropiedad(propiedad))

    elif opcionPropiedad == 2:
        nombreActualizar = input("Ingrese el nombre de la propiedad que desea actualizar: ").strip()
        propiedad = propiedadNegocio.buscarPropiedadPorNombre(nombreActualizar)

        if propiedad is None:
            print(f"No se encontró ninguna propiedad con el nombre '{nombreActualizar}'.")
            return

        print("Propiedad encontrada. Ingrese los nuevos datos (deje en blanco para mantener el valor actual):")
        nombre = input(f"Nombre ({propiedad.getNombre()}): ").strip() or propiedad.getNombre()
        direccion = input(f"Dirección ({propiedad.getDireccion()}): ").strip() or propiedad.getDireccion()
        tipo = input(f"Tipo ({propiedad.getTipo()}): ").strip() or propiedad.getTipo()
        observaciones = input(f"Observaciones ({propiedad.getObservaciones()}): ").strip() or propiedad.getObservaciones()

        propiedadNegocio.actualizarPropiedad(propiedad, nombre, direccion, tipo, observaciones)
        print("Propiedad actualizada:")
        print(propiedadNegocio.obtenerPropiedad(propiedad))

    elif opcionPropiedad == 3:
        nombreEliminar = input("Ingrese el nombre de la propiedad que desea eliminar: ").strip()
        if propiedadNegocio.eliminarPropiedad(nombreEliminar):
            print(f"Propiedad '{nombreEliminar}' eliminada.")
        else:
            print(f"No se encontró ninguna propiedad con el nombre '{nombreEliminar}'.")

    elif opcionPropiedad == 4:
        print("\n------ Registrar Estadía ------")
        if len(propiedades) == 0:
            print("No hay propiedades cargadas.")
            return
        for i, propiedad in enumerate(propiedades):
            print(f"{i + 1}. {propiedad}")
        try:
            eleccion = int(input("Seleccione la propiedad (ingrese el número): ").strip())
            if not (1 <= eleccion <= len(propiedades)):
                print("Error: Número de propiedad fuera de rango.")
                return
            propiedadSeleccionada = propiedades[eleccion - 1]
        except ValueError:
            print("Error: Debe ingresar un número válido.")
            return

        fechaInicio = input("Fecha de ingreso (AAAA-MM-DD): ").strip()
        fechaFin = input("Fecha de salida (AAAA-MM-DD): ").strip()
        montoTotal = input("Monto total de la estadía (en USD): ").strip()
        plataforma = input("Plataforma (Airbnb, Booking, etc.): ").strip()

        estadia = estadiaNegocio.crearEstadia(fechaInicio, fechaFin, montoTotal, plataforma, propiedadSeleccionada)
        if estadia is None:
            print("\nError: Verifique que las fechas sean reales (AAAA-MM-DD), la salida no sea anterior al ingreso y el monto sea numérico mayor a 0.")
        else:
            print("\nEstadía registrada correctamente:")
            print(estadiaNegocio.obtenerDatos(estadia))

    elif opcionPropiedad == 5:
        print("\n------ Registrar Egreso ------")
        if len(propiedades) == 0:
            print("No hay propiedades cargadas.")
            return
        for i, propiedad in enumerate(propiedades):
            print(f"{i + 1}. {propiedad}")
        try:
            eleccion = int(input("Seleccione la propiedad (ingrese el número): ").strip())
            if not (1 <= eleccion <= len(propiedades)):
                print("Error: Número de propiedad fuera de rango.")
                return
            propiedadSeleccionada = propiedades[eleccion - 1]
        except ValueError:
            print("Error: Debe ingresar un número válido.")
            return

        fecha = input("Fecha del gasto (AAAA-MM-DD): ").strip()
        montoPesos = input("Monto del gasto (en Pesos ARS): ").strip()
        descripcion = input("Descripción del gasto (ej. Plomería, Electricista): ").strip()

        egreso = egresoNegocio.crearEgreso(fecha, montoPesos, descripcion, propiedadSeleccionada, cotizacionActual)
        if egreso is None:
            print("\nError: Verifique que la fecha sea real (AAAA-MM-DD), el monto sea numérico mayor a 0 y tenga descripción.")
        else:
            print(f"\nEgreso registrado y convertido a USD (Cotización: ${cotizacionActual.getValor()}):")
            print(egresoNegocio.obtenerDatos(egreso))

    elif opcionPropiedad == 6:
        return

    else:
        print("Opción no válida. Por favor, ingrese una opción válida.")


# Menu por consola para calcular y mostrar la liquidacion de una propiedad
def menuLiquidaciones():
    print("\n------ Consultar Liquidación ------")
    # Traigo todas las propiedades para elegir cual liquidar
    propiedades = propiedadNegocio.obtenerPropiedades()
    if len(propiedades) == 0:
        print("No hay propiedades cargadas.")
        return
    for i, propiedad in enumerate(propiedades):
        print(f"{i + 1}. {propiedad}")

    try:
        eleccion = int(input("Seleccione la propiedad (ingrese el número): ").strip())
        if not (1 <= eleccion <= len(propiedades)):
            print("Error: Número de propiedad fuera de rango.")
            return
        propiedadSeleccionada = propiedades[eleccion - 1]
    except ValueError:
        print("Error: Debe ingresar un número válido.")
        return

    fechaDesde = input("Ingrese fecha desde (AAAA-MM-DD, ej. 2026-01-01): ").strip()
    fechaHasta = input("Ingrese fecha hasta (AAAA-MM-DD, ej. 2026-01-31): ").strip()

    liquidacion = liquidacionNegocio.crearLiquidacion(propiedadSeleccionada, fechaDesde, fechaHasta)
    if liquidacion is None:
        print("\nError: Verifique que las fechas sean reales (AAAA-MM-DD) y que la fecha hasta no sea anterior a la fecha desde.")
        return

    resumen = liquidacionNegocio.obtenerResumen(liquidacion)

    print("\n========== RESUMEN DE LIQUIDACIÓN ==========")
    print(f"Propiedad:             {resumen['propiedad']}")
    print(f"Período:               {resumen['fechaDesde']} al {resumen['fechaHasta']}")
    print(f"Estadías en período:   {resumen['cantidadEstadias']}")
    print(f"Egresos en período:    {resumen['cantidadEgresos']}")
    print("--------------------------------------------")
    print(f"Total Ingresos (USD):  ${resumen['totalIngresosUsd']}")
    print(f"Gasto Limpieza (USD):  ${resumen['gastoLimpiezaUsd']} ({resumen['cantidadEstadias']} x $25)")
    print(f"Total Egresos (USD):   ${resumen['totalEgresosUsd']} (incluye limpieza)")
    print(f"Comisión 15% (USD):    ${resumen['comisionInmobiliariaUsd']}")
    print("--------------------------------------------")
    print(f"GANANCIA NETA (USD):   ${resumen['gananciaNetaUsd']}")
    print("============================================\n")



