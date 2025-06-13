"# flask" 
"# flaskapp" 
*NECESITO UNA APP CONSTRUIDA EN flask
QUE SE CONECTE A UNA BASE DE DATOS LLAMADA db.db con mysql que se van a guardar en el root de la app donde se va a encontrar app.py*

Todas las contraseñas incluyendo la secre key de la *app.py* deben estar encriptada  con bcrypt

debes utilizar únicamente bootstrap como framework

Todas las imagenes se van a guardar en *db.db* y en la carpeta static/images

Debes darme  las vistas y los controladores las librerías que voy a utilizar para instalar con pip

Nunca vas a darme los estilos dentro de las vistas. Todo va a estar en un css con el nombre de cada vistas llamados desde base.html

Guardar toda la lógica de conexión a la base de datos en  *db.py* y esta va a contener toda la conexion de las bases de datos pero para empezar únicamente la de sqlite Pero va a tener la base de datos mysql comentado Pero 100 funcional

MUY IMPORTANTE.. TODOS LOS BOTONES QUE PERMITAN BORRAR UN REGISTRO O USUARIO O LO QUE SEA dentro de esta app SE VAN A MANEJAR CON FLASK y FLASH. OSEA SE BORRARÁ DESDE EL BACKEND PARA NO USAR JAVASCRIPT


LOS PASOS:
1. vas a crear un archivo llamado *app.py*  que va a contener la lógica de arranque. Va a trabajar con el puerto 3030

Y cuando te diga OK me das el siguiente paso

2. vas a crear un archivo llamado *home.py*  y las correspondientes vistas relacionadas a
 Home y dentro un *navbar* compatible con mobile,  responsiva con logo y los  enlaces a cada uno de las siguiente vistas: 

	login con enlace a Registro	
	Inicio <- home

	*NO CREAR LAS VISTAS SOLO LOS ENLACES en el navbar*
	contactos
	Cotización
	Caminatas
	Calendario
	Inventario
	Notas
  	Info de la Tribu
	Sistema de rifas
	Gestor de proyectos
	Tabla de pagos
	Perfil
	Mail



Y cuando te diga OK me das el siguiente paso



3.crear un archivo llamado *login.py* va contener el 
*Formulario para loguarse*
	usuario
	password y ojo para mostrar el password
	recordar contraseña y preservar los datos
	recuperar contraseña (si lógica)
	Enlace para ir a registro


Y cuando te diga OK me das el siguiente paso

4.crear un archivo llamado *registro.py* va a contener lo siguiente:
*Formulario para crear registro*
	Avatar Imagen e imagen Default<- opcional
	nombre, 
	primer apellido, 
	segundo apellido, <- opcional 
	usuario de Registro, 
	password 
	confirmar password, 
	telefono,
	teléfono de Emergencia, <- opcional
	Nombre Emergencia, <-opcional
	Empresa 	<- opcional
	Cédula 		<- opcional
	Dirección 	<- opcional
	Email		<- opcional
	select llamado Actividad(No Aplica, La Tribu, Senderista, Enfermería, Cocina, Confección y Diseño, Confección y Diseño, Restaurante, Transporte Terrestre, Transporte Terrestre, Transporte Acuatico, Transporte Acuatico, Transporte Aereo, Transporte Aereo, Migración, Parque Nacional, Refugio Silvestre, Refugio Silvestre, Centro de Atracción, Lugar para Caminata, Acarreo, Oficina de trámite, Primeros Auxilios, Farmacia, Taller,  Abobado, Mensajero, Tienda, Polizas, Aerolínea, Guía, Banco, Otros) <- opcional
	
	selet llamado Capacidad(Seleccionar Capacidad, Rápido, Intermedio, Básico, Iniciante) <- opcional
	
	selet llamado Participación(No Aplica, Solo de La Tribu, Constante, inconstante, El Camino de Costa Rica, Parques Nacionales, Paseo | Recreativo, Revisar/Eliminar)
	fecha automática cuando se registra


Y cuando te diga OK me das el siguiente paso









5.crear un archivo que tenga toda la lógica de un crud, llamado *contactos.py*  Esta debe contener todos los contactos ingresados a través de  *registro.html*

Crear Las vistas:
*editar_contacto.html* <- permite editar y borrar contacto 

*ver_contacto.html* <- aqui se ven el nombre y apellido y teléfono con un botón a la par que dice VER MÁS que va a ir a otra vista llamada  *detalle_contacto.html*

También dentro de *ver_contacto.html* debe contener  un boton que me lleve a registrar nuevo contacto dentro de *registro.html*

*detalle_contacto.html* <- Aquí muestra el contenido del contacto con todos los datos del usuario seleccionado además que permita  exportar a vcard, excel, jpg, txt


Y cuando te diga OK me das el siguiente paso

6. vas a crear y leer un archivo  llamado *perfil.py*   que tenga toda la lógica y toda la información del contacto registrado, además de permitir editar la información de perfil y  borrar el perfil

7.vas a crear un archivo llamado *notas.py*  que tenga toda la lógica de un crud con: vistas   *crear_nota.html*  que tenga un título, un campo que diga creado por el usuario que está registrado y un campo llamado Nota: que pueda poner el texto en negrita, alinear, crear lista, viñeta, subrayar, tachar, itálica, code, poner en titulo y subtítulo,
Contacto que crea la nota
autofecha de creación

*editar_nota.html* que permita editar toda la información ingresada y borrar la nota con flask y flash 

*ver_nota.html* permite ve la nota el título el avatar y un botón que diga ver más que vaya a *detalle_nota.html*

*detalle_nota.html* va a contener toda la información de la nota creada y abajo exportar a PDF, JPG, Txt


Y cuando te diga OK me das el siguiente paso



8. vas a crear un archivo llamado *evento.py* y las correspondientes vistas relacionadas al nombre de la función que estás creando que tenga toda la lógica de un crud que me permita crear, (ver, con un botón de crear evento), actualizar y borrar con flask y flash un Evento. Debe contener los siguientes campos.

*crear_evento.html*
	*Formulario para crear evento*

Título
Lugar,
Precio, 
Fecha datapicker, 
hora, 
notificar cada(1, 3, 5) días antes
autofecha de creado
Descripción,
registrado por: usuario registrado

editar_evento.html
Permite editar absolutamente  toda la información del evento y registrar la fecha de modificación 

detalle_evento.html
Permite ver absolutamente toda la información ingresada por medio de crear_evento.html con opciones de exportar a pdf, jpg, txt aquí mismo el botón de editar y botón de borrar el evento con flask y flash.

ver_evento.html 
Permite ver los eventos creados con titulo y fecha y hora  además de un botón que diga ver más y lleve a detalle_evento.html

Y cuando te diga OK me das el siguiente paso





9. vas a crear un archivo llamado *proyecto.py*  que tenga toda la lógica de un crud que me permita crear  actualizar y borrar un proyecto. Debe contener los siguientes campos.
	
*crear_proyecto.py*
	*Formulario para crear proyecto*

	Nombre del Proyecto:,
	Imagen del Proyecto:,
	Lugar:,
	selet llamado Provincias:(Alajuela,Cartago,Heredia,Limón,Puntarenas'Guanacaste,San José)
	selet llamado Cantón: (Que contenga los cantones de Costa Rica según la provincia seleccionada)
	Distancia desde Casa:,
	Distancia de Recorrido:,
	Contacto Lugar:,
	Fecha:,
	Presupuesto ¢:,
	selet llamado  dificultad(No Aplica, Paseo,Básico,Intermedio,Dificil,Avanzado,Técnico),
	selet llamado Propuesta Por (Kenneth Ruiz Matamoros, Jenny Ceciliano Cordoba, Invitado),
	selet llamado Transporte(No aplica, Moto, Lancha, Barco, Aereo, Buseta, Auto, Bus),
	Trasporte Varios Indique:,
	selet llamado  Tipo de Terreno(No aplica, Asfalto, Lastre, Montaña, Arena),
	Otro Terreno Indique:,
	notas_adicionales:,
	Un botón de Agregar opciones( to-do list )
	
*editar_proyecto.html*, permite editar absolutamente toda la información ingresada por medio de crear_proyecto.html
y registrar la fecha de modificación 

*detalle_proyecto.html*
Permite ver absolutamente toda la información ingresada por medio de crear_proyecto.html con opciones de exportar a pdf, jpg, txt aquí mismo el botón de editar y botón de borrar el evento con flask y flash

*ver_proyecto.html*
Permite ver los proyectos creados con Nombre del Proyecto, Imagen del Proyecto,   fecha y lugar. además de un botón que diga ver más y lleve a detalle_proyecto.html

Y cuando te diga OK me das el siguiente paso







10. vas a crear un archivo llamado caminatas.py  que tenga toda la lógica de un crud que me permita crear, actualizar y borrar una caminata que se van agregado a través de un botón  Para eso va existir los siguientes campos:
	
*crear_caminata.html*
	*Formulario para crear_caminata*

Avatar:
selet llamado Actividad(El Camino de Costa Rica, Parques Nacionales, Paseo, Iniciante, Básico, Intermedio, Avanzado, Técnico, Producto, Servicio, Internacional, Convivio)
Nombre:
Precio:
Reserva con
fecha:
Nota:
Distancia:
Provincia:
Hora Salida:
selet llamado  Incluye(No aplica, Transporte, Transporte + Alimentación, Transporte + Entrada + Alimentación, Todo)
Descripción
selet llamado Capacidad(12,14,17,26,28,31,42,Más)
	selet llamado sinpe(86227500-Kenneth Ruiz Matamoros, 87984232-Jenny Ceciliano Cordoba, 8652 9837-Jenny Ceciliano Cordoba)
	Otra Forma de Pago:
	Exporta jpg y .TxT


*editar_caminata.html*
Permite editar absolutamente  toda la información de la caminata y registrar la fecha de modificación 

*detalle_caminata.html*
Permite ver absolutamente toda la información ingresada por medio de crear_camianta.html 
Va a existir un botón para agregar usuarios  registrados previamente en contactos a la lista,  cada registro agregado va a tener  un botón de eliminar usuarios y otro contenga un select(pendiente(color rojo), reservado(color amarillo), cancelado(color verde))  y otro botón que diga ver más que va a ir a una vista llamada abonos.html

*abonos.html* contendrá un sistema de pagos por usuario y muestre el total y faltante. Cuando el usuario registrado cancela el total el usuario de la lista de detalle_caminata.html se pone en fondo color verde ligero

En *detalle_caminata.html*
Va a tener las opciones de exportar a pdf, jpg, txt 
aquí mismo el botón de editar y botón de borrar caminata con flask y flash.

*ver_caminata.html*
Permite ver las caminatas  creadas con avatar, actividad, nombre y fecha, precio,   además de un botón que diga ver más y lleve a detalle_evento.html

Y cuando te diga OK me das el siguiente paso

	
No me entregues toda la información de un solo. Me vas a MOSTRAR COMO VA A QUEDAR LA RAIZ DEL PROYECTO Y ME VAS A INDICAR SI ENTENDISTE...  

Ojo no invente más vistas y vas a demostrarme que solo creaste las vistas que te pedí.
Y me vas dar cada fragmento cada vez que te diga ok



***CRUD DE NUESTRAS CAMINATAS***