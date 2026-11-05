import flet as ft
from negocio import propietarioNegocio
from negocio import propiedadNegocio
from negocio import estadiaNegocio
from negocio import egresoNegocio
from negocio import liquidacionNegocio


def iniciarInterfaz(cotizacionActual):

    def main(page: ft.Page):
        # Configuración básica de la ventana de Windows
        page.title = "Sistema GAT - Gestión de Alquileres Temporarios"
        page.window.width = 850
        page.window.height = 700
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 25
 
        # Este texto sirve para mostrar mensajes de éxito o error en pantalla (reemplaza a los print de aviso)
        txtMensaje = ft.Text(value="", size=15, weight=ft.FontWeight.BOLD)

        # Contenedor principal donde vamos a ir cambiando la pantalla según el botón que toque el usuario
        contenedorPantalla = ft.Column(spacing=15)

        # =====================================================================
        # PANTALLA 1: GESTIÓN DE PROPIETARIOS (Crear, Buscar/Actualizar, Eliminar)
        # =====================================================================
        def mostrarPantallaPropietarios(e=None):
            txtMensaje.value = ""
            propiedades = propiedadNegocio.obtenerPropiedades()

            # Cajas de texto (reemplazan a los input())
            txtDni = ft.TextField(label="DNI", width=200)
            txtNombre = ft.TextField(label="Nombre", width=200)
            txtApellido = ft.TextField(label="Apellido", width=200)
            txtTelefono = ft.TextField(label="Teléfono", width=200)
            txtEmail = ft.TextField(label="Email", width=250)

            # Lista desplegable de propiedades
            opcionesPropiedades = [ft.dropdown.Option(p.getNombre()) for p in propiedades]
            ddPropiedad = ft.Dropdown(label="Asignar Propiedad (opcional)", width=300, options=opcionesPropiedades)

            # Función del botón "Crear Propietario"
            def clickCrearPropietario(e):
                if not txtNombre.value or not txtApellido.value or not txtDni.value:
                    txtMensaje.value = "Complete al menos Nombre, Apellido y DNI."
                    page.update()
                    return

                propiedadesSeleccionadas = []
                if ddPropiedad.value:
                    prop = propiedadNegocio.buscarPropiedadPorNombre(ddPropiedad.value)
                    if prop:
                        propiedadesSeleccionadas.append(prop)

                propietario = propietarioNegocio.crearPropietario(
                    txtNombre.value.strip(),
                    txtApellido.value.strip(),
                    txtTelefono.value.strip(),
                    txtEmail.value.strip(),
                    txtDni.value.strip(),
                    propiedadesSeleccionadas
                )
                txtMensaje.value = f"Propietario creado en MySQL: {propietarioNegocio.obtenerDatos(propietario)}"
                page.update()

            # Función del botón "Buscar por DNI" (para cargar sus datos en las cajas y poder actualizarlo)
            def clickBuscarPropietario(e):
                propietario = propietarioNegocio.buscarPropietarioPorDni(txtDni.value.strip())
                if propietario is None:
                    txtMensaje.value = "No existe un propietario con ese DNI."
                else:
                    txtNombre.value = propietario.getNombre()
                    txtApellido.value = propietario.getApellido()
                    txtTelefono.value = propietario.getTelefono()
                    txtEmail.value = propietario.getEmail()
                    txtMensaje.value = f"Propietario encontrado (ID {propietario.getId()}). Modifique los campos y toque Actualizar."
                page.update()

            # Función del botón "Actualizar Propietario"
            def clickActualizarPropietario(e):
                propietario = propietarioNegocio.buscarPropietarioPorDni(txtDni.value.strip())
                if propietario is None:
                    txtMensaje.value = "Primero busque un DNI existente para actualizar."
                    page.update()
                    return

                propietarioNegocio.actualizarPropietario(
                    propietario,
                    txtNombre.value.strip(),
                    txtApellido.value.strip(),
                    txtTelefono.value.strip(),
                    txtEmail.value.strip(),
                    txtDni.value.strip()
                )
                txtMensaje.value = f"Propietario actualizado correctamente en MySQL: {propietarioNegocio.obtenerDatos(propietario)}"
                page.update()

            # Función del botón "Eliminar Propietario"
            def clickEliminarPropietario(e):
                if propietarioNegocio.eliminarPropietario(txtDni.value.strip()):
                    txtMensaje.value = "Propietario eliminado correctamente de MySQL."
                    txtNombre.value = ""
                    txtApellido.value = ""
                    txtTelefono.value = ""
                    txtEmail.value = ""
                else:
                    txtMensaje.value = "No se encontró un propietario con ese DNI."
                page.update()

            # Armamos la vista en el contenedor
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

        # =====================================================================
        # PANTALLA 2: PROPIEDADES, ESTADÍAS Y EGRESOS
        # =====================================================================
        def mostrarPantallaPropiedades(e=None):
            txtMensaje.value = ""
            propiedades = propiedadNegocio.obtenerPropiedades()
            opcionesPropiedades = [ft.dropdown.Option(p.getNombre()) for p in propiedades]

            # --- Controles para Propiedad (Crear / Buscar / Actualizar / Eliminar) ---
            txtNombreProp = ft.TextField(label="Nombre de la Propiedad", width=250)
            txtDireccionProp = ft.TextField(label="Dirección", width=250)
            txtTipoProp = ft.TextField(label="Tipo (Casa, Depto, Local)", width=200)
            txtObsProp = ft.TextField(label="Observaciones", width=300)

            def clickCrearPropiedad(e):
                prop = propiedadNegocio.crearPropiedad(
                    txtNombreProp.value.strip(),
                    txtDireccionProp.value.strip(),
                    txtTipoProp.value.strip(),
                    txtObsProp.value.strip()
                )
                mostrarPantallaPropiedades()  # Recarga el desplegable con la nueva propiedad
                txtMensaje.value = f"Propiedad creada en MySQL: {propiedadNegocio.obtenerPropiedad(prop)}"
                page.update()

            def clickBuscarPropiedad(e):
                prop = propiedadNegocio.buscarPropiedadPorNombre(txtNombreProp.value.strip())
                if prop is None:
                    txtMensaje.value = "No se encontró una propiedad con ese nombre."
                else:
                    txtDireccionProp.value = prop.getDireccion()
                    txtTipoProp.value = prop.getTipo()
                    txtObsProp.value = prop.getObservaciones()
                    txtMensaje.value = "Propiedad encontrada. Puede modificar sus datos y tocar Actualizar."
                page.update()

            def clickActualizarPropiedad(e):
                prop = propiedadNegocio.buscarPropiedadPorNombre(txtNombreProp.value.strip())
                if prop is None:
                    txtMensaje.value = "No existe una propiedad con ese nombre para actualizar."
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

            def clickEliminarPropiedad(e):
                nombre = txtNombreProp.value.strip()
                if propiedadNegocio.eliminarPropiedad(nombre):
                    mostrarPantallaPropiedades()
                    txtMensaje.value = f"Propiedad '{nombre}' eliminada de MySQL."
                else:
                    txtMensaje.value = f"No se encontró la propiedad '{nombre}'."
                page.update()

            # --- Controles para Registrar Estadía ---
            ddPropEstadia = ft.Dropdown(label="Propiedad", width=250, options=opcionesPropiedades)
            txtFechaInicio = ft.TextField(label="Ingreso (AAAA-MM-DD)", width=180)
            txtFechaFin = ft.TextField(label="Salida (AAAA-MM-DD)", width=180)
            txtMontoUsd = ft.TextField(label="Monto Total (USD)", width=150)
            txtPlataforma = ft.TextField(label="Plataforma (Airbnb/Booking)", width=200)

            def clickRegistrarEstadia(e):
                prop = propiedadNegocio.buscarPropiedadPorNombre(ddPropEstadia.value)
                if prop is None:
                    txtMensaje.value = "Seleccione una propiedad para la estadía."
                    page.update()
                    return
                estadia = estadiaNegocio.crearEstadia(
                    txtFechaInicio.value.strip(),
                    txtFechaFin.value.strip(),
                    float(txtMontoUsd.value.strip()),
                    txtPlataforma.value.strip(),
                    prop
                )
                txtMensaje.value = f"Estadía registrada en MySQL: {estadiaNegocio.obtenerDatos(estadia)}"
                page.update()

            # --- Controles para Registrar Egreso ---
            ddPropEgreso = ft.Dropdown(label="Propiedad", width=250, options=opcionesPropiedades)
            txtFechaEgreso = ft.TextField(label="Fecha (AAAA-MM-DD)", width=180)
            txtMontoPesos = ft.TextField(label="Monto (Pesos ARS)", width=160)
            txtDescEgreso = ft.TextField(label="Descripción (Plomería, etc.)", width=250)

            def clickRegistrarEgreso(e):
                prop = propiedadNegocio.buscarPropiedadPorNombre(ddPropEgreso.value)
                if prop is None:
                    txtMensaje.value = "Seleccione una propiedad para el egreso."
                    page.update()
                    return
                egreso = egresoNegocio.crearEgreso(
                    txtFechaEgreso.value.strip(),
                    float(txtMontoPesos.value.strip()),
                    txtDescEgreso.value.strip(),
                    prop,
                    cotizacionActual
                )
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

        # =====================================================================
        # PANTALLA 3: CONSULTAR LIQUIDACIÓN
        # =====================================================================
        def mostrarPantallaLiquidaciones(e=None):
            txtMensaje.value = ""
            propiedades = propiedadNegocio.obtenerPropiedades()
            opcionesPropiedades = [ft.dropdown.Option(p.getNombre()) for p in propiedades]

            ddPropLiquidacion = ft.Dropdown(label="Seleccione Propiedad", width=300, options=opcionesPropiedades)
            txtDesde = ft.TextField(label="Fecha Desde (AAAA-MM-DD)", value="2026-01-01", width=200)
            txtHasta = ft.TextField(label="Fecha Hasta (AAAA-MM-DD)", value="2026-01-31", width=200)
            txtResultadoLiquidacion = ft.Text(value="", size=16, selectable=True)

            def clickCalcularLiquidacion(e):
                if not ddPropLiquidacion.value:
                    txtMensaje.value = "Seleccione una propiedad de la lista."
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

        # =====================================================================
        # BARRA DE NAVEGACIÓN SUPERIOR (Reemplaza al Menú Principal 1, 2, 3)
        # =====================================================================
        barraMenuPrincipal = ft.Row(
            controls=[
                ft.Button(content="1. Menú Propietarios", on_click=mostrarPantallaPropietarios),
                ft.Button(content="2. Menú Propiedades / Estadías / Egresos", on_click=mostrarPantallaPropiedades),
                ft.Button(content="3. Traer Liquidaciones", on_click=mostrarPantallaLiquidaciones),
            ],
            spacing=15
        )

        # Agregamos a la ventana el título, los 3 botones de menú, el área de pantalla y el texto de avisos
        page.add(
            ft.Text("Sistema GAT - Gestión de Alquileres Temporarios", size=26, weight=ft.FontWeight.BOLD),
            barraMenuPrincipal,
            ft.Divider(),
            txtMensaje,
            contenedorPantalla
        )

        # Al abrir la ventana por primera vez, mostramos la pantalla de Liquidaciones
        mostrarPantallaLiquidaciones()

    ft.run(main)
