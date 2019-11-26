# LFShell

LFShell es un shell simple creado por Lucas Martinez y Erik Wasmosy, escrito completamente en Python3. Este soporta los comandos basicos de un shell Linux junto con otros comandos "especificos". Mas informacion sobre estos comandos "especificos" se encuentra al final de este documento.

## Requisitos

### Directorios necesarios:

LFShell necesita que el directorio /var/log se enceuntre creado ya que en dicho directorio se guardaran los diferentes .log del shell.
Por defecto los sistemas Linux ya cuentan con este directorio.

En caso de no contar con el directorio /var/log, crearemos uno con el siguiente comando:
	sudo mkdir /var/log/

Luego, debemos asegurarnos que el directorio /var/log/ sea accesible por el shell debido que este debe poder escribir en dicho directorio. Cambiaremos sus permisos con el siguiente comando:
	sudo chmod 777 /var/log

### Archivos a crear:

Como se ha mencionado antes, el LFShell registra logs en archivos en el directorio /var/log/ , por lo que para que este funcione correctamente debemos crear los siguientes archivos en dicho directorio: errores_sistema.log , shell_log.log , personal_h.log , personal_horarios_log.log , usuarios_datos.log , Shell_transferencias.log (tenga en cuenta que en este ultimo archivo la palabra Shell cuenta con una S mayuscula)

Los podemos crear con los siguientes comandos:
	sudo touch /var/log/errores_sistema.log
	sudo touch /var/log/shell_log.log
	sudo touch /var/log/personal_h.log
	sudo touch /var/log/personal_horarios_log.log
	sudo touch /var/log/Shell_transferencias.log

## Instalacion

Primero: Sescargar la carpeta lfshell ubicada en https://gitlab.com/martinezlucas98/lfshell.git.
Si su sistema Linux cuenta con el comando 'git', entonces ejecute los siguientes comandos:
	sudo cd /
	sudo git clone https://gitlab.com/martinezlucas98/lfshell.git
En caso de no poseer el comando git, usted puede (desde otro sistema operativo) descargar el archivo ya sea directamente desde la web o con el comando git mencionado anteriormente y almacenarlo en un disco externo (por ejemplo un pendrive)
Una vez que cuente con el archivo en su disco externo, puede montarlo en su sistema linux (en el cual desea instalar lfshell).
Luego, falta simplemente copiar el archivo al directorio /, lo hacemos con el siguiente comando:
	sudo cp -r <UBICACION_DEL_DISCO_MONTADO> /

Segundo: Para instalar LFShell y que este funcione como shell en un sistema Linux es necesario agregarlo al archivo /etc/profile :
	sudo echo "bash /lfshell/lfshell.sh" >> /etc/profile

### Licencia

MIT

## Comandos especificos incluidos con LFShell:

copiar		Equivalente a 'cp'. Copia un archivo o un directorio completo a la ubicacion especificada
mover		Equivalente a 'mv'. Mueva la ubicacion de un archivo o de un directorio completo
renombrar	Renombra un archivo.
listar		Equivalente a 'ls'. Lista todos los directorios que se encuentran edentro de cierto directorio mencionado
creardir	Equivalente a 'mkdir'. Crea un directorio en un lugar especificado.
ir		Equivalente a 'cd'. Cambia de directorio al directorio especificado
permisos	Equivalente a 'chmod'. Cambia los permisos de uno o mas archivos
propietario	Equivalente a 'chown'. Cambia el usuario duenho de un archivo
contrasena	Equivalente a 'passwd'. Cambia la contrasenha del usuario
usuario		Equivalente a 'useradd' pero tambien agrega horario e ip's esperadas del usuario 
ayuda		Equivalente a 'help'. Despliega un menu de ayuda (el que se encuentra viendo actualmente)
salir		Equivalente a 'exit'. Cierra/termina la linea de comando (usar solo si tiene interfaz grafica)
demonio		Permite levantar o apagar un demonio
scp		Transferencia scp
ftp		Transferencia ftp

Instalar: (AL FINAL NO)
sudo apt install pip3
sudo pip3 install python-daemon
