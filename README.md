# LFShell

LFShell es un shell simple escrito completamente en Python3. Este soporta los comandos basicos de un shell Linux junto con otros comandos "especificos".

##Directorios necesarios:
LFShell necesita que el directorio /var/log se enceuntre creado ya que en dicho directorio se guardaran los diferentes .log del shell.
Por defecto los sistemas Linux ya cuentan con este directorio.

En caso de no contar con el directorio /var/log, crearemos uno con el siguiente comando:
sudo mkdir /var/log/

##Archivos a crear:
Como se ha mencionado antes, el LFShell registra logs en archivos en el directorio /var/log/ , por lo que para que este funcione correctamente debemos crear los siguientes archivos en dicho directorio: errores_sistema.log , shell_log.log , personal_horarios_log.log , usuarios_datos.log , Shell_transferencias.log (tenga en cuenta que en este ultimo archivo la palabra Shell cuenta con una S mayuscula)

Los podemos crear con los siguientes comandos:
sudo touch /var/log/errores_sistema.log
sudo touch /var/log/shell_log.log
sudo touch /var/log/personal_horarios_log.log
sudo touch /var/log/usuarios_datos.log
sudo touch /var/log/Shell_transferencias.log

##Instalacion

Para instalar LFShell y que este funcione como shell en un sistema Linux es necesario agregarlo al archivo /etc/ALGO

###Como agregar LFShell al /etc/fstab

##Licencia

MIT


Instalar: (AL FINAL NO)
sudo apt install pip3
sudo pip3 install python-daemon
