# LFShell

LFShell es un shell simple creado por Lucas Martinez y Erik Wasmosy, escrito completamente en Python3. Este soporta los comandos basicos de un shell Linux junto con otros comandos "especificos". Mas informacion sobre estos comandos "especificos" se encuentra al final de este documento.

## Requisitos

### Directorios necesarios:

LFShell necesita que el directorio /var/log se enceuntre creado ya que en dicho directorio se guardaran los diferentes .log del shell.<br/>
Por defecto los sistemas Linux ya cuentan con este directorio.<br/>

En caso de no contar con el directorio /var/log, crearemos uno con el siguiente comando:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sudo mkdir /var/log<br/>


### Archivos para crear:

Como se ha mencionado antes, el LFShell registra logs en archivos en el directorio /var/log , por lo que para que este funcione correctamente debemos crear los siguientes archivos en dicho directorio:<br/>errores_sistema.log , shell_log.log , personal_h.log , personal_horarios_log.log , usuarios_datos.log , Shell_transferencias.log (tenga en cuenta que en este ultimo archivo la palabra Shell cuenta con una S mayuscula)<br/>

Los podemos crear con los siguientes comandos:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sudo touch /var/log/errores_sistema.log<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sudo touch /var/log/shell_log.log<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sudo touch /var/log/personal_h.log<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sudo touch /var/log/personal_horarios_log.log<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sudo touch /var/log/Shell_transferencias.log

## Permisos:

Luego, debemos asegurarnos que el directorio /var/log , y los archivos contenidos en el, sean accesibles por el shell (lfshell) debido que este debe poder escribir en dicho directorio. Cambiaremos sus permisos con el siguiente comando:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sudo chmod -R 777 /var/log<br/>

## Instalacion

Primero: Descargar la carpeta lfshell ubicada en https://gitlab.com/martinezlucas98/lfshell.git.<br/>
Si su sistema Linux cuenta con el comando 'git', entonces ejecute los siguientes comandos:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sudo cd /<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sudo git clone https://gitlab.com/martinezlucas98/lfshell.git<br/>
En caso de no poseer el comando git, usted puede (desde otro sistema operativo) descargar el archivo ya sea directamente desde la web o con el comando git mencionado anteriormente y almacenarlo en un disco externo (por ejemplo un pendrive)<br/>
Una vez que cuente con el archivo en su disco externo, puede montarlo en su sistema Linux (en el cual desea instalar lfshell).<br/>
Una vez montado, falta simplemente copiar el archivo al directorio /, lo hacemos con el siguiente comando:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sudo cp -r [UBICACION_DEL_ARCHVIVO_EN_EL_DISCO_MONTADO] /<br/>

Segundo: Para instalar LFShell y que este funcione como shell en un sistema Linux es necesario agregarlo al archivo /etc/profile :<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sudo echo "bash /lfshell/lfshell.sh" >> /etc/profile<br/>

Tercero: Reiniciamos el sistema Linux con el comando:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sudo shutdown -r now

LFShell ya se encuentra instalado y funcionando!!!


## Comandos especificos incluidos con LFShell:

copiar&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;		Equivalente a 'cp'. Copia un archivo o un directorio completo a la ubicacion especificada<br/>
mover&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;		Equivalente a 'mv'. Mueva la ubicacion de un archivo o de un directorio completo<br/>
renombrar&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	Renombra un archivo.<br/>
listar&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;		Equivalente a 'ls'. Lista todos los directorios que se encuentran edentro de cierto directorio mencionado<br/>
creardir&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	Equivalente a 'mkdir'. Crea un directorio en un lugar especificado.<br/>
ir&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;		Equivalente a 'cd'. Cambia de directorio al directorio especificado<br/>
permisos&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	Equivalente a 'chmod'. Cambia los permisos de uno o mas archivos<br/>
propietario&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	Equivalente a 'chown'. Cambia el usuario duenho de un archivo<br/>
contrasena&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	Equivalente a 'passwd'. Cambia la contrasenha del usuario<br/>
usuario&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	Equivalente a 'useradd' pero tambien agrega horario e ip's esperadas del usuario<br/>
ayuda&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;		Equivalente a 'help'. Despliega un menu de ayuda (el que se encuentra viendo actualmente)<br/>
salir&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;		Equivalente a 'exit'. Cierra/termina la linea de comando (usar solo si tiene interfaz grafica)<br/>
demonio&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;		Permite levantar o apagar un demonio<br/>
scp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;		Transferencia scp<br/>
ftp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;		Transferencia ftp<br/>
