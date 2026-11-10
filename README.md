# Gestion de Alquileres Temporarios (GAT)

Este proyecto es un sistema desarrollado en Python para administrar propietarios, propiedades en alquiler temporario, estadias en dolares (USD), egresos en pesos argentinos (que se convierten automaticamente a USD consultando la cotizacion oficial en DolarAPI) y el calculo de liquidaciones para cada propiedad.

## Como funciona la aplicacion

El programa esta dividido en cuatro capas para que el codigo sea ordenado y cada archivo tenga su propia responsabilidad:

* **Presentacion**: Es la parte que interactua con el usuario. Pide los datos y muestra los resultados (por consola en menu.py o por ventana grafica en interfazVisual.py).
* **Negocio**: Contiene la logica del sistema. Se encarga de validar que los datos ingresados sean correctos, convertir los gastos de pesos a dolares, crear los objetos y hacer las cuentas de las liquidaciones.
* **Clases**: Contiene los moldes de los objetos del sistema (Propietario, Propiedad, Estadia, Egreso, Liquidacion y Cotizacion) con sus atributos, getters y setters.
* **Datos**: Es la unica capa que se conecta con la base de datos MySQL. Ejecuta las consultas SQL para guardar, buscar, modificar o borrar registros.

### Versiones del proyecto

* **version_hardcodeada_memoria**: Version inicial por consola donde los datos se guardan temporalmente en listas en memoria mientras el programa esta abierto.
* **version_con_persistencia**: Version por consola conectada a la base de datos MySQL para que los datos queden guardados de forma permanente.
* **Proyecto principal (raiz)**: Version con interfaz grafica hecha en Flet y conectada a la misma base de datos MySQL.

## Ejemplo del recorrido de un Propietario en la version con persistencia (Consola)

Cuando se crea un propietario nuevo desde el menu por consola y se le asigna una propiedad, los datos hacen el siguiente recorrido:

* **1. Ingreso de datos en la capa de presentacion (menu.py)**: El programa le pide al usuario que escriba por teclado el nombre, apellido, telefono, email y DNI mediante input, y le pide que elija un numero de la lista de propiedades disponibles. Esos datos se envian a la funcion crearPropietario de la capa de negocio.
* **2. Validacion y armado del objeto en la capa de negocio (propietarioNegocio.py)**: Antes de guardar nada, el sistema verifica con validacionNegocio.py que el DNI tenga entre 7 y 9 numeros, que el telefono sea numerico y que el email sea valido. Tambien comprueba que no exista otro propietario con el mismo DNI. Si todo esta bien, crea el objeto Propietario en memoria con sus datos y su propiedad asignada, y se lo pasa a la capa de datos.
* **3. Guardado en MySQL en la capa de datos (propietarioDatos.py)**: La funcion insertarPropietario abre la conexion con MySQL y hace un INSERT en la tabla propietarios. Luego toma el ID que le asigno la base de datos y hace un UPDATE en la tabla propiedades para vincularle ese id_propietario a la propiedad elegida.
* **4. Muestra del resultado en consola**: La capa de negocio recibe el ID generado, se lo asigna al objeto Propietario y se lo devuelve al menu, que muestra por pantalla los datos cargados usando print.

## Ejemplo del mismo objeto Propietario en la version con interfaz grafica

En la version con interfaz grafica, el objeto Propietario, las validaciones de negocio y el guardado en MySQL funcionan exactamente igual que en la version por consola. Lo unico que cambia es la capa de presentacion:

* **1. Ingreso de datos en la ventana grafica (interfazVisual.py)**: En lugar de escribir en la consola, el usuario completa los campos de texto en la ventana (Nombre, Apellido, Telefono, Email y DNI), selecciona la propiedad en una lista desplegable y presiona el boton Crear Propietario.
* **2. Llamada a la misma capa de negocio (propietarioNegocio.py)**: El evento del boton toma los valores escritos en las cajas de texto y llama a la misma funcion crearPropietario que usa la consola.
* **3. Mismo objeto y misma base de datos (clases y datos)**: La capa de negocio valida los datos, crea el mismo objeto Propietario y llama a propietarioDatos.py para hacer el INSERT en la tabla propietarios y el UPDATE en la tabla propiedades dentro de MySQL.
* **4. Respuesta visual en la ventana**: Si algun dato era incorrecto (por ejemplo un DNI con letras), la funcion devuelve None y la ventana muestra un aviso en color rojo. Si se guardo bien, limpia los campos de texto y muestra un mensaje en color verde con los datos del objeto Propietario creado.
