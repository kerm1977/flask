# DB MYSQL
# VIDEOS DE REFERENCIA------------------------
# https://www.youtube.com/watch?v=-tgA40Ia9X8
#https://www.youtube.com/watch?v=QvArhNUPMRg&t=27s
#--------------------------------------------

import mysql.connector
opt=input("1-Crear, 2-Mostrar, 3-Borrar Bases de datos, 4-Salir: ")

while opt.isalpha():
	print("Solo debe ingresar números")
	opt=input("Digite nuevamente: 1-Crear, 2-Mostrar, 3-Borrar Bases de datos, 4-Salir: ")

if opt.isdigit():
	while 0<int(opt)<=3:
		#Importa el conector de prueba
		# import pymssql 
		# Objeto para conectar con el servidor
		mydb = mysql.connector.connect(
			# Argumentos de clave
			host = "localhost", 	#"LaTribuHiking.mysql.pythonanywhere-services.com",
			user = "root", 			#"LaTribuHiking",
			password = "root"  		#"latribu1977",
			# database = "db"  		#"LaTribuHiking$db"
			)

		cursor = mydb.cursor()
		cursor.execute("SHOW DATABASES") #Muestra las db de mysql
		# Procesa los resultados de las consultas que se hagan al servidor
		# y va recorriendo cada línea de la DB
		for db in cursor:
			print(db)
		opt=int(opt)
		if opt==1:
			try:
				creator = input("Digite un nombre para CREAR la base de datos: ")
				cursor = mydb.cursor()
				cursor.execute(f"CREATE DATABASE {creator}") #Crea las bases de datos
				cursor.execute("SHOW DATABASES") #Muestra las db de mysql
				print(f"Creaste una Base de datos llamada {creator}")
				opt=int(input("1-Crear, 2-Mostrar, 3-Borrar Bases de datos, 4-Salir: "))
			except:
				print(f"Error al crear base de datos. Puede que la base de datos {creator} ya exista.")
				opt=int(input("1-Crear, 2-Mostrar, 3-Borrar Bases de datos, 4-Salir: "))
		
		elif opt==2:
			cursor = mydb.cursor()
			cursor.execute("SHOW DATABASES") #Muestra las db de mysql
			opt=int(input("1-Crear, 2-Mostrar, 3-Borrar Bases de datos, 4-Salir: "))
		

		elif opt==3:
			try:
				drop = input("Digite un nombre para BORRAR la base de datos: ")
				cursor = mydb.cursor()
				cursor.execute(f"DROP DATABASE {drop}") #Elimina las bases de datos
				print(f"Eliminaste la base de datos: {drop}")
				cursor.execute("SHOW DATABASES") #Muestra las db de mysql
				opt=int(input("1-Crear, 2-Mostrar, 3-Borrar Bases de datos, 4-Salir: "))
			except:
				print(f"Es posible que la base de datos {drop} haya sido borrada o no exita.")
				opt=int(input("1-Crear, 2-Mostrar, 3-Borrar Bases de datos, 4-Salir: "))
		elif opt==4:	
			break


print("Saliste del programa")




# CON EL SIGUIENTE CÓDIGO FUNCIONO EN pythonanywhere

# # DB MYSQL
# # VIDEOS DE REFERENCIA------------------------
# # https://www.youtube.com/watch?v=-tgA40Ia9X8
# #https://www.youtube.com/watch?v=QvArhNUPMRg&t=27s
# #--------------------------------------------

# import mysql.connector
# opt=int(input("1-Crear, 2-Mostrar, 3-Borrar Bases de datos, 4-Salir: "))
# while 0<opt<=3:

# 	#Importa el conector de prueba
# 	# import pymssql


# 	# Objeto para conectar con el servidor
# 	mydb = mysql.connector.connect(
# 		# Argumentos de clave
# 		host = "LaTribuHiking.mysql.pythonanywhere-services.com",
# 		user = "LaTribuHiking",
# 		password = "latribu1977",
# 		database = "LaTribuHiking$db"
# 		)
# 	cursor = mydb.cursor()
# 	cursor.execute("SHOW DATABASES") #Muestra las db de mysql
# 	# Procesa los resultados de las consultas que se hagan al servidor
# 	# y va recorriendo cada línea de la DB
# 	for db in cursor:
# 		print(db)

# 	if opt==1:
# 		try:
# 			creator = input("Digite un nombre para CREAR la base de datos: ")
# 			cursor = mydb.cursor()
# 			cursor.execute(f"CREATE DATABASE {creator}") #Crea las bases de datos
# 			cursor.execute("SHOW DATABASES") #Muestra las db de mysql
# 			print(f"Creaste una Base de datos llamada {creator}")
# 			opt=int(input("1-Crear, 2-Mostrar, 3-Borrar Bases de datos, 4-Salir: "))
# 		except:
# 			print(f"Error al crear base de datos. Puede que la base de datos {creator} ya exista.")
# 	elif opt==2:
# 		cursor = mydb.cursor()
# 		cursor.execute("SHOW DATABASES") #Muestra las db de mysql
# 		opt=int(input("1-Crear, 2-Mostrar, 3-Borrar Bases de datos, 4-Salir: "))
# 	elif opt==3:
# 		try:
# 			drop = input("Digite un nombre para BORRAR la base de datos: ")
# 			cursor = mydb.cursor()
# 			cursor.execute(f"DROP DATABASE {drop}") #Elimina las bases de datos
# 			print(f"Eliminaste la base de datos: {drop}")
# 			cursor.execute("SHOW DATABASES") #Muestra las db de mysql
# 			opt=int(input("1-Crear, 2-Mostrar, 3-Borrar Bases de datos, 4-Salir: "))
# 		except:
# 			print(f"Es posible que la base de datos {drop} no exita.")
# 	elif opt==4:
# 		break
# print("Saliste del programa")