import flet as ft
from negocio import propietarioNegocio
from negocio import propiedadNegocio
from negocio import estadiaNegocio
from negocio import egresoNegocio
from negocio import liquidacionNegocio
from negocio import validacionNegocio


def iniciarInterfaz(cotizacionActual):

    def main(page: ft.Page):
        # Configuro la ventana principal de Windows
        page.title = "Sistema GAT - Gestión de Alquileres Temporarios"
        page.window.width = 850
        page.window.height = 700
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 25

        # Uso este texto para mostrar los avisos de exito o error arriba de cada pantalla
        txtMensaje = ft.Text(value="", size=15, weight=ft.FontWeight.BOLD)

        # En este contenedor voy cambiando la pantalla segun el boton del menu que toque
        contenedorPantalla = ft.Column(spacing=15)

        # Pantalla 1: Gestion de Propietarios (Crear, Buscar, Actualizar y Eliminar)
        def mostrarPantallaPropietarios(e=None):
            txtMensaje.value = ""
            # Traigo todas las propiedades para cargarlas en el desplegable
            propiedades = propiedadNegocio.obtenerPropiedades()

            txtDni = ft.TextField(label="DNI (7 a 9 números)", width=200)
            txtNombre = ft.TextField(label="Nombre", width=200)
            txtApellido = ft.TextField(label="Apellido", width=200)
            txtTelefono = ft.TextField(label="Teléfono (solo números)", width=200)
            txtEmail = ft.TextField(label="Email (ej. correo@mail.com)", width=250)

            opcionesPropiedades = [ft.dropdown.Option(p.getNombre()) for p in propiedades]
            ddPropiedad = ft.Dropdown(label="Asignar Propiedad (opcional)", width=300, options=opcionesPropiedades)

            # Valido los campos y guardo un propietario nuevo en mysql
            def clickCrearPropietario(e):
                if not txtNombre.value.strip() or not txtApellido.value.strip():
                    txtMensaje.value = "Error: Nombre y Apellido son obligatorios."
                    page.update()
                    return
                if not validacionNegocio.esDniValido(txtDni.value):
                    txtMensaje.value = "Error: El DNI debe tener entre 7 y 9 dígitos numéricos (sin letras ni puntos)."
                    page.update()
                    return
                if not validacionNegocio.esTelefonoValido(txtTelefono.value):
                    txtMensaje.value = "Error: El teléfono debe contener solo números (mínimo 6 dígitos)."
                    page.update()
                    return
                if not validacionNegocio.esEmailValido(txtEmail.value):
                    txtMensaje.value = "Error: Ingrese un email válido (debe contener '@' y '.')."
                    page.update()
                    return

                propiedadesSeleccionadas = []
                if ddPropiedad.value:
                    prop = propiedadNegocio.buscarPropiedadPorNombre(ddPropiedad.value)
                    if prop:
                        propiedadesSeleccionadas.append(prop)

                propietario = propietarioNegocio.crearPropietario(
                    txtNombre.value,
                    txtApellido.value,
                    txtTelefono.value,
                    txtEmail.value,
                    txtDni.value,
                    propiedadesSeleccionadas
                )
                if propietario is None:
                    txtMensaje.value = "Error: Ya existe un propietario registrado con ese DNI."
                else:
                    txtMensaje.value = f"Propietario creado en MySQL: {propietarioNegocio.obtenerDatos(propietario)}"
                page.update()

            # Traigo al propietario por su DNI y completo las cajas de texto con sus datos
            def clickBuscarPropietario(e):
                if not validacionNegocio.esDniValido(txtDni.value):
                    txtMensaje.value = "Error: El DNI debe tener entre 7 y 9 dígitos numéricos (sin letras)."
                    page.update()
                    return

                propietario = propietarioNegocio.buscarPropietarioPorDni(txtDni.value)
                if propietario is None:
                    txtMensaje.value = "No existe un propietario con ese DNI."
                else:
                    txtNombre.value = propietario.getNombre()
                    txtApellido.value = propietario.getApellido()
                    txtTelefono.value = propietario.getTelefono()
                    txtEmail.value = propietario.getEmail()
                    if propietario.getPropiedades():
                        ddPropiedad.value = propietario.getPropiedades()[0].getNombre()
                    else:
                        ddPropiedad.value = None
                    txtMensaje.value = f"Propietario encontrado: {propietarioNegocio.obtenerDatos(propietario)}. Modifique los campos y toque Actualizar."
                page.update()

            # Traigo al propietario por DNI y actualizo sus datos en mysql con lo que escribi en pantalla
            def clickActualizarPropietario(e):
                if not validacionNegocio.esDniValido(txtDni.value):
                    txtMensaje.value = "Error: El DNI debe tener entre 7 y 9 dígitos numéricos."
                    page.update()
                    return

                propietario = propietarioNegocio.buscarPropietarioPorDni(txtDni.value)
                if propietario is None:
                    txtMensaje.value = "Primero busque un DNI existente para actualizar."
                    page.update()
                    return

                if not txtNombre.value.strip() or not txtApellido.value.strip():
                    txtMensaje.value = "Error: Nombre y Apellido no pueden quedar vacíos."
                    page.update()
                    return
                if not validacionNegocio.esTelefonoValido(txtTelefono.value):
                    txtMensaje.value = "Error: El teléfono debe contener solo números."
                    page.update()
                    return
                if not validacionNegocio.esEmailValido(txtEmail.value):
                    txtMensaje.value = "Error: Ingrese un email válido."
                    page.update()
                    return

                propiedadesSeleccionadas = propietario.getPropiedades()
                if ddPropiedad.value:
                    prop = propiedadNegocio.buscarPropiedadPorNombre(ddPropiedad.value)
                    if prop:
                        propiedadesSeleccionadas = [prop]

                propietarioNegocio.actualizarPropietario(
                    propietario,
                    txtNombre.value,
                    txtApellido.value,
                    txtTelefono.value,
                    txtEmail.value,
                    txtDni.value,
                    propiedadesSeleccionadas
                )
                txtMensaje.value = f"Propietario actualizado correctamente en MySQL: {propietarioNegocio.obtenerDatos(propietario)}"
                page.update()

            # Elimino al propietario de mysql usando su DNI y limpio los campos
            def clickEliminarPropietario(e):
                if not validacionNegocio.esDniValido(txtDni.value):
                    txtMensaje.value = "Error: El DNI debe tener entre 7 y 9 dígitos numéricos."
                    page.update()
                    return

                if propietarioNegocio.eliminarPropietario(txtDni.value):
                    txtMensaje.value = "Propietario eliminado correctamente de MySQL."
                    txtNombre.value = ""
                    txtApellido.value = ""
                    txtTelefono.value = ""
                    txtEmail.value = ""
                else:
                    txtMensaje.value = "No se encontró un propietario con ese DNI."
                page.update()

            contenedorPantalla.controls = [
                ft.Text("Menú Propietarios", size=22, weight=ft.FontWeight.BOLD),
                ft.Text("Ingrese el DNI para buscar/eliminar, o complete los datos para crear uno nuevo:"),
                ft.Row([txtDni, ft.Button(content="Buscar por DNI", on_click=clickBuscarPropietario)]),
                ft.Row([txtNombre, txtApellido]),
                ft.Row([txtTelefono, txtEmail]),
                ddPropiedad,
                ft.Row([
                    ft.Button(content="1. Crear Propietario", on_click=clickCrearPropietario),
                    ft.Button(content="2. Actualizar Propietario", on_click=clickActualizarPropietario),
                    ft.Button(content="3. Eliminar por DNI", on_click=clickEliminarPropietario),
                ]),
            ]
            page.update()

        # Pantalla 2: Gestion de Propiedades, registro de Estadias y registro de Egresos
        def mostrarPantallaPropiedades(e=None):
            txtMensaje.value = ""
            # Traigo todas las propiedades desde mysql para los desplegables de estadias y egresos
            propiedades = propiedadNegocio.obtenerPropiedades()
            opcionesPropiedades = [ft.dropdown.Option(p.getNombre()) for p in propiedades]

            txtNombreProp = ft.TextField(label="Nombre de la Propiedad", width=250)
            txtDireccionProp = ft.TextField(label="Dirección", width=250)
            txtTipoProp = ft.TextField(label="Tipo (Casa, Depto, Local)", width=200)
            txtObsProp = ft.TextField(label="Observaciones", width=300)

            # Guardo una propiedad nueva en mysql y recargo los desplegables
            def clickCrearPropiedad(e):
                if not txtNombreProp.value.strip() or not txtDireccionProp.value.strip():
                    txtMensaje.value = "Error: El nombre y la dirección de la propiedad son obligatorios."
                    page.update()
                    return

                prop = propiedadNegocio.crearPropiedad(
                    txtNombreProp.value,
                    txtDireccionProp.value,
                    txtTipoProp.value,
                    txtObsProp.value
                )
                if prop is None:
                    txtMensaje.value = "Error: Ya existe una propiedad con ese nombre en MySQL."
                    page.update()
                    return

                mostrarPantallaPropiedades()
                txtMensaje.value = f"Propiedad creada en MySQL: {propiedadNegocio.obtenerPropiedad(prop)}"
                page.update()

            # Traigo una propiedad buscando por su nombre y lleno los campos en pantalla
            def clickBuscarPropiedad(e):
                if not txtNombreProp.value.strip():
                    txtMensaje.value = "Error: Ingrese el nombre de la propiedad a buscar."
                    page.update()
                    return
                prop = propiedadNegocio.buscarPropiedadPorNombre(txtNombreProp.value.strip())
                if prop is None:
                    txtMensaje.value = "No se encontró una propiedad con ese nombre."
                else:
                    txtDireccionProp.value = prop.getDireccion()
                    txtTipoProp.value = prop.getTipo()
                    txtObsProp.value = prop.getObservaciones()
                    txtMensaje.value = "Propiedad encontrada. Puede modificar sus datos y tocar Actualizar."
                page.update()

            # Actualizo en mysql los datos de la propiedad que busque por nombre
            def clickActualizarPropiedad(e):
                prop = propiedadNegocio.buscarPropiedadPorNombre(txtNombreProp.value.strip())
                if prop is None:
                    txtMensaje.value = "No existe una propiedad con ese nombre para actualizar."
                    page.update()
                    return
                if not txtDireccionProp.value.strip():
                    txtMensaje.value = "Error: La dirección no puede quedar vacía."
                    page.update()
                    return
                propiedadNegocio.actualizarPropiedad(
                    prop,
                    txtNombreProp.value.strip(),
                    txtDireccionProp.value.strip(),
                    txtTipoProp.value.strip(),
                    txtObsProp.value.strip()
                )
                txtMensaje.value = f"Propiedad actualizada: {propiedadNegocio.obtenerPropiedad(prop)}"
                page.update()

            # Elimino la propiedad de mysql buscando por su nombre
            def clickEliminarPropiedad(e):
                nombre = txtNombreProp.value.strip()
                if not nombre:
                    txtMensaje.value = "Error: Ingrese el nombre de la propiedad a eliminar."
                    page.update()
                    return
                if propiedadNegocio.eliminarPropiedad(nombre):
                    mostrarPantallaPropiedades()
                    txtMensaje.value = f"Propiedad '{nombre}' eliminada de MySQL."
                else:
                    txtMensaje.value = f"No se encontró la propiedad '{nombre}'."
                page.update()

            # Controles y funcion para guardar una estadia en USD asociada a la propiedad elegida
            ddPropEstadia = ft.Dropdown(label="Propiedad", width=250, options=opcionesPropiedades)
            txtFechaInicio = ft.TextField(label="Ingreso (AAAA-MM-DD)", width=180)
            txtFechaFin = ft.TextField(label="Salida (AAAA-MM-DD)", width=180)
            txtMontoUsd = ft.TextField(label="Monto Total (USD)", width=150)
            txtPlataforma = ft.TextField(label="Plataforma (Airbnb/Booking)", width=200)

            def clickRegistrarEstadia(e):
                if not ddPropEstadia.value:
                    txtMensaje.value = "Error: Seleccione una propiedad para la estadía."
                    page.update()
                    return
                if not validacionNegocio.esFechaValida(txtFechaInicio.value):
                    txtMensaje.value = "Error: La fecha de ingreso no es una fecha real válida (use formato AAAA-MM-DD, ej. 2026-09-09)."
                    page.update()
                    return
                if not validacionNegocio.esFechaValida(txtFechaFin.value):
                    txtMensaje.value = "Error: La fecha de salida no es una fecha real válida (use formato AAAA-MM-DD, ej. 2026-09-15)."
                    page.update()
                    return
                if not validacionNegocio.esRangoFechasValido(txtFechaInicio.value, txtFechaFin.value):
                    txtMensaje.value = "Error: La fecha de salida no puede ser anterior a la fecha de ingreso."
                    page.update()
                    return
                if not validacionNegocio.esMontoValido(txtMontoUsd.value):
                    txtMensaje.value = "Error: El monto total debe ser un número positivo válido (sin letras)."
                    page.update()
                    return
                if not txtPlataforma.value.strip():
                    txtMensaje.value = "Error: Ingrese la plataforma (ej. Airbnb, Booking)."
                    page.update()
                    return

                prop = propiedadNegocio.buscarPropiedadPorNombre(ddPropEstadia.value)
                estadia = estadiaNegocio.crearEstadia(
                    txtFechaInicio.value,
                    txtFechaFin.value,
                    txtMontoUsd.value,
                    txtPlataforma.value,
                    prop
                )
                if estadia is None:
                    txtMensaje.value = "Error: Datos inválidos, no se guardó la estadía."
                else:
                    txtMensaje.value = f"Estadía registrada en MySQL: {estadiaNegocio.obtenerDatos(estadia)}"
                page.update()

            # Controles y funcion para guardar un egreso en pesos ARS (se pasa a USD con la cotizacion del dia)
            ddPropEgreso = ft.Dropdown(label="Propiedad", width=250, options=opcionesPropiedades)
            txtFechaEgreso = ft.TextField(label="Fecha (AAAA-MM-DD)", width=180)
            txtMontoPesos = ft.TextField(label="Monto (Pesos ARS)", width=160)
            txtDescEgreso = ft.TextField(label="Descripción (Plomería, etc.)", width=250)

            def clickRegistrarEgreso(e):
                if not ddPropEgreso.value:
                    txtMensaje.value = "Error: Seleccione una propiedad para el egreso."
                    page.update()
                    return
                if not validacionNegocio.esFechaValida(txtFechaEgreso.value):
                    txtMensaje.value = "Error: La fecha del gasto no es una fecha real válida (use formato AAAA-MM-DD)."
                    page.update()
                    return
                if not validacionNegocio.esMontoValido(txtMontoPesos.value):
                    txtMensaje.value = "Error: El monto del gasto debe ser un número positivo válido (sin letras)."
                    page.update()
                    return
                if not txtDescEgreso.value.strip():
                    txtMensaje.value = "Error: Ingrese una descripción para el gasto."
                    page.update()
                    return

                prop = propiedadNegocio.buscarPropiedadPorNombre(ddPropEgreso.value)
                egreso = egresoNegocio.crearEgreso(
                    txtFechaEgreso.value,
                    txtMontoPesos.value,
                    txtDescEgreso.value,
                    prop,
                    cotizacionActual
                )
                if egreso is None:
                    txtMensaje.value = "Error: Datos inválidos, no se guardó el egreso."
                else:
                    txtMensaje.value = f"Egreso convertido a USD (Cotización ${cotizacionActual.getValor()}) y guardado: {egresoNegocio.obtenerDatos(egreso)}"
                page.update()

            contenedorPantalla.controls = [
                ft.Text("Menú Propiedades", size=22, weight=ft.FontWeight.BOLD),
                ft.Row([txtNombreProp, ft.Button(content="Buscar por Nombre", on_click=clickBuscarPropiedad)]),
                ft.Row([txtDireccionProp, txtTipoProp, txtObsProp]),
                ft.Row([
                    ft.Button(content="1. Crear Propiedad", on_click=clickCrearPropiedad),
                    ft.Button(content="2. Actualizar Propiedad", on_click=clickActualizarPropiedad),
                    ft.Button(content="3. Eliminar Propiedad", on_click=clickEliminarPropiedad),
                ]),
                ft.Divider(),
                ft.Text("4. Registrar Estadía (en USD)", size=18, weight=ft.FontWeight.BOLD),
                ft.Row([ddPropEstadia, txtFechaInicio, txtFechaFin]),
                ft.Row([txtMontoUsd, txtPlataforma, ft.Button(content="Guardar Estadía", on_click=clickRegistrarEstadia)]),
                ft.Divider(),
                ft.Text(f"5. Registrar Egreso (en Pesos ARS -> se guarda en USD a ${cotizacionActual.getValor()})", size=18, weight=ft.FontWeight.BOLD),
                ft.Row([ddPropEgreso, txtFechaEgreso, txtMontoPesos]),
                ft.Row([txtDescEgreso, ft.Button(content="Guardar Egreso", on_click=clickRegistrarEgreso)]),
            ]
            page.update()

        # Pantalla 3: Consultar Liquidacion de una propiedad en un rango de fechas
        def mostrarPantallaLiquidaciones(e=None):
            txtMensaje.value = ""
            # Traigo todas las propiedades para elegir cual quiero liquidar
            propiedades = propiedadNegocio.obtenerPropiedades()
            opcionesPropiedades = [ft.dropdown.Option(p.getNombre()) for p in propiedades]

            ddPropLiquidacion = ft.Dropdown(label="Seleccione Propiedad", width=300, options=opcionesPropiedades)
            txtDesde = ft.TextField(label="Fecha Desde (AAAA-MM-DD)", value="2026-01-01", width=200)
            txtHasta = ft.TextField(label="Fecha Hasta (AAAA-MM-DD)", value="2026-01-31", width=200)
            txtResultadoLiquidacion = ft.Text(value="", size=16, selectable=True)

            # Traigo las estadias y egresos del periodo y calculo el resumen de liquidacion
            def clickCalcularLiquidacion(e):
                txtResultadoLiquidacion.value = ""
                if not ddPropLiquidacion.value:
                    txtMensaje.value = "Error: Seleccione una propiedad de la lista."
                    page.update()
                    return
                if not validacionNegocio.esFechaValida(txtDesde.value):
                    txtMensaje.value = "Error: La 'Fecha Desde' no es una fecha real válida (use AAAA-MM-DD)."
                    page.update()
                    return
                if not validacionNegocio.esFechaValida(txtHasta.value):
                    txtMensaje.value = "Error: La 'Fecha Hasta' no es una fecha real válida (use AAAA-MM-DD)."
                    page.update()
                    return
                if not validacionNegocio.esRangoFechasValido(txtDesde.value, txtHasta.value):
                    txtMensaje.value = "Error: La 'Fecha Hasta' no puede ser anterior a la 'Fecha Desde'."
                    page.update()
                    return

                propiedadSeleccionada = propiedadNegocio.buscarPropiedadPorNombre(ddPropLiquidacion.value)
                liquidacion = liquidacionNegocio.crearLiquidacion(
                    propiedadSeleccionada,
                    txtDesde.value.strip(),
                    txtHasta.value.strip()
                )
                resumen = liquidacionNegocio.obtenerResumen(liquidacion)

                txtResultadoLiquidacion.value = (
                    f"========== RESUMEN DE LIQUIDACIÓN ==========\n"
                    f"Propiedad:             {resumen['propiedad']}\n"
                    f"Período:               {resumen['fechaDesde']} al {resumen['fechaHasta']}\n"
                    f"Estadías en período:   {resumen['cantidadEstadias']}\n"
                    f"Egresos en período:    {resumen['cantidadEgresos']}\n"
                    f"--------------------------------------------\n"
                    f"Total Ingresos (USD):  ${resumen['totalIngresosUsd']}\n"
                    f"Gasto Limpieza (USD):  ${resumen['gastoLimpiezaUsd']} ({resumen['cantidadEstadias']} x $25)\n"
                    f"Total Egresos (USD):   ${resumen['totalEgresosUsd']} (incluye limpieza)\n"
                    f"Comisión 15% (USD):    ${resumen['comisionInmobiliariaUsd']}\n"
                    f"--------------------------------------------\n"
                    f"GANANCIA NETA (USD):   ${resumen['gananciaNetaUsd']}\n"
                    f"============================================"
                )
                txtMensaje.value = ""
                page.update()

            contenedorPantalla.controls = [
                ft.Text("Consultar Liquidación", size=22, weight=ft.FontWeight.BOLD),
                ddPropLiquidacion,
                ft.Row([txtDesde, txtHasta, ft.Button(content="Calcular Liquidación", on_click=clickCalcularLiquidacion)]),
                ft.Divider(),
                txtResultadoLiquidacion,
            ]
            page.update()

        # Armo la barra de navegacion superior con los 3 botones del menu principal
        barraMenuPrincipal = ft.Row(
            controls=[
                ft.Button(content="1. Menú Propietarios", on_click=mostrarPantallaPropietarios),
                ft.Button(content="2. Menú Propiedades / Estadías / Egresos", on_click=mostrarPantallaPropiedades),
                ft.Button(content="3. Traer Liquidaciones", on_click=mostrarPantallaLiquidaciones),
            ],
            spacing=15
        )

        # Agrego a la ventana el titulo, la cotizacion del dolar del dia, los botones del menu y el contenedor de pantallas
        page.add(
            ft.Text("Sistema GAT - Gestión de Alquileres Temporarios", size=26, weight=ft.FontWeight.BOLD),
            ft.Text(f"Cotización Dólar Oficial: ${cotizacionActual.getValor()} ARS (Fecha: {str(cotizacionActual.getFecha())[:10]})", size=16),
            barraMenuPrincipal,
            ft.Divider(),
            txtMensaje,
            contenedorPantalla
        )

        # Cuando abre la app por primera vez, muestro directamente la pantalla de Liquidaciones
        mostrarPantallaLiquidaciones()

    ft.run(main)
