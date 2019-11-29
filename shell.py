#!/usr/bin/env python3

"""psh: a simple shell written in Python"""

#imports para los diferentes comandos
import os
import subprocess
import getpass
import shutil
import itertools
import signal
import socket
from datetime import datetime
from subprocess import check_output


#imports para el historial y autocompletado
import readline
import rlcompleter
import atexit

welcomemsg = """
   __    ___  __ _          _ _ 
  / /   / __\/ _\ |__   ___| | |
 / /   / _\  \ \| '_ \ / _ \ | |
/ /___/ /    _\ \ | | |  __/ | |
\____/\/     \__/_| |_|\___|_|_|
                                v1.1.1

psh: shell implementation in Python3
Creado por Lucas Martinez & Erik Wasmosy."""

#una clase con los valores de string para ponerle color al texto en la consola (si la consola admite color)
class tcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#COMANDOS ESPECIFICOS DEL TRABAJO

#1 comando para copiar (sin usar la llamada al sistema cp)
def psh_copiar(src_dst): #src_dts: el source y el destino ejemplo: copiar hola /root/chau --> hola es source y /root/chau es destino
    if src_dst == "--ayuda": #si el parametro es --ayuda entonces mostramos menu de ayuda
        print("""Uso: copiar <PATH_ARCHIVO> <PATH_DESTINO>
Copia el archivo o directorio especificado en <PATH_ARCHIVO> en <PATH_DESTINO>
""")
    else:
        msg_ok = "copiar "+src_dst #mensaje para escribir en el log del shell si se ejecuto correctamente el comando
        msg_err = "copiar: no such file or directory, or directory already exists: "+src_dst #mensaje para escribir en el log de errores si NO se ejecuto correctamente el comando
        paths = src_dst.split(" ") #separamos src_dest en src y dst

        #da el formato adecuado a los path (funcion explicada mas adelante)
        src = path_formater(paths[0])
        dst = path_formater(paths[1])
        try: #realiza la copia del archivo
            shutil.copy(src, dst)
            print("copiar: "+src+" -> "+dst)
            write_shell_log(msg_ok) #escribimos en el historial
        except Exception:
            try: #si no se pudo, puede que sea un directorio entonces prueba copiar el directorio
                if os.path.isdir(dst): #si no se especifica el nombre con el que se va ancopiar entonces le agrega el nombre original
                    name = src.rsplit("/", 1)
                    dst = dst + "/" + name[1]
                shutil.copytree(src, dst)
                print("copiar: " + src + " -> " + dst)
                write_shell_log(msg_ok) #escribe en el log del shell
            except Exception:
                print(tcolors.WARNING + "copiar: no such file or directory:" + tcolors.ENDC)
                print(src + " " + dst)
                write_errores_sistema_log(msg_err) #escribe en el log de errores


#2 comando para mover
def psh_mover(inp): #inp es el input (comando completo) que recibe
    if inp == "mover --ayuda":
        print("""Uso: mover <PATH_ARCHIVO> <PATH_DESTINO>
Mueve el archivo o directorio especificado en <PATH_ARCHIVO> a <PATH_DESTINO>
""")
    else:
        msg_ok = inp #mensaje para escribir en el log del shell si se ejecuto correctamente el comando
        msg_err = "mover: no existe el archivo o directorio: " + inp.replace("mover", "", 1) #mensaje para escribir en el log de errores si NO se ejecuto correctamente el comando
        inp = inp.replace("mover", "mv", 1) #formateamos el input para que coincida con el comando original mv
        ret = os.system(inp) #se realiza mv
        if ret == 0:
            write_shell_log(msg_ok) #escribe en el log del shell
        else:
            write_errores_sistema_log(msg_err) #escribe en el log de errores


#3 comando para renombrar
def psh_renombrar(inp): #inp es el input (comando completo) que recibe
    if inp == "renombrar --ayuda":
        print("""Uso: renombrar <PATH_ARCHIVO> <NUEVO_NOMBRE>
Renombra el archivo o directorio especificado en <PATH_ARCHIVO> a <NUEVO_NOMBRE>
""")
    else:
        msg_ok = inp #mensaje para escribir en el log del shell si se ejecuto correctamente el comando
        msg_err = "renombrar: no existe el archivo o directorio: "+ inp.replace("renombrar", "", 1) #mensaje para escribir en el log de errores si NO se ejecuto correctamente el comando
        inp = inp.replace("renombrar", "mv", 1) #formateamos el input para que coincida con el comando original mv
        ret = os.system(inp) #se realiza mv
        if ret == 0:
            write_shell_log(msg_ok) #escribe en el log del shell
        else:
            write_errores_sistema_log(msg_err) #escribe en el log de errores


#4 comando para listar un directorio
def psh_listar(path): #path es el path que recibe el comando como parametro
    if path == "--ayuda":
        print("""Uso: listar <PATH_DIRECTORIO>
Lista en pantalla los directorios ubicados dentro del directorio especificado en <PATH_DIRECTORIO>
""")
    else:
        msg_ok = "listar "+path #mensaje para escribir en el log del shell si se ejecuto correctamente el comando
        msg_err = "listar: no existe el directorio: " + path #mensaje para escribir en el log de errores si NO se ejecuto correctamente el comando
        #path = command.replace("listar ", "", 1)
        path = path_formater(path) #da el formato adecuado al path (funcion explicada mas adelante)
        try:
            dl = os.listdir(path) #dl: directory list, lista de los directorios en el path
            #imprime dl en dos columnas
            for t in itertools.zip_longest(dl[::2],dl[1::2],fillvalue=""):
              print(("{:<35} {:<35}").format(*t))
            write_shell_log(msg_ok) #escribe en el log del shell
        except Exception:
            print(tcolors.WARNING + "listar: no such file or directory: "+path+ tcolors.ENDC)
            write_errores_sistema_log(msg_err) #escribe en el log de errores


#5 comando para crear un directorio
def psh_creardir(inp): #inp es el input (comando completo) que recibe
    if inp == "creardir --ayuda":
        print("""Uso: creardir <PATH_DIRECTORIO>
Crea un nuevo directorio <PATH_DIRECTORIO>
""")
    else:
        msg_ok = inp #mensaje para escribir en el log del shell si se ejecuto correctamente el comando
        msg_err = "creardir: el directorio ya existe: "+ inp.replace("creardir", "", 1) #mensaje para escribir en el log de errores si NO se ejecuto correctamente el comando
        inp = inp.replace("creardir", "mkdir", 1) #formateamos el input para que coincida con el comando original mkdir
        ret = os.system(inp) #se realiza mkdir
        if ret == 0:
            write_shell_log(msg_ok) #escribe en el log del shell
        else:
            write_errores_sistema_log(msg_err) #escribe en el log de errores


#6 comando para cambiar de directorio (sin usar la llamada al sistema cd)
def psh_ir(path): #path es el path que recibe el comando como parametro
    if path == "--ayuda":
        print("""Uso: ir <PATH_DIRECTORIO>
Cambia el directorio donde se encuentra al directorio <PATH_DIRECTORIO>
""")
    else:
        msg_ok = "ir: " + path #mensaje para escribir en el log del shell si se ejecuto correctamente el comando
        msg_err = "ir: no existe el directorio o es un archivo: " + path #mensaje para escribir en el log de errores si NO se ejecuto correctamente el comando
        #path = command.replace("ir ", "", 1)
        path = path_formater(path) #da el formato adecuado al path (funcion explicada mas adelante)
        try:
            os.chdir(path) #cambia el directorio actual por el directorio del path
            write_shell_log(msg_ok) #escribe en el log del shell
        except Exception:
            print(tcolors.WARNING + "ir: no such file or directory: " + path + tcolors.ENDC)
            write_errores_sistema_log(msg_err) #escribe en el log de errores


#7 comando para cambiar los permisos de uno o mas archivos
def psh_permisos(inp): #inp es el input (comando completo) que recibe
    if inp == "permisos --ayuda":
        print("""Uso: permisos <PERMISOS>[,<PERMISOS>]... <ARCHIVO>...
permisos -R <PERMISOS>[,<PERMISOS>]... <ARCHIVO>...
Cambia los permisos de cada archivo <ARCHIVO> a <PERMISOS>
La opcion -R : cambia de forma recursiva los permisos de los archivos contenido dentro del directorio 
""")
    else:
        msg_ok = inp #mensaje para escribir en el log del shell si se ejecuto correctamente el comando
        msg_err = "permisos: ha ocurrido un error: " + inp #mensaje para escribir en el log de errores si NO se ejecuto correctamente el comando
        inp = inp.replace("permisos", "chmod", 1) #formateamos el input para que coincida con el comando original chmod
        ret = os.system(inp) #se realiza chmod
        if ret == 0:
            write_shell_log(msg_ok) #escribe en el log del shell
        else:
            write_errores_sistema_log(msg_err) #escribe en el log de errores


#8 comando para cambiar los propietarios de uno o mas archivos
def psh_propietario(inp): #inp es el input (comando completo) que recibe
    if inp == "propietario --ayuda":
        print("""Uso: propietario <PROPIETARIO_O_GRUPO> <ARCHIVO>...
propietario -R <PROPIETARIO_O_GRUPO> <ARCHIVO>...
Cambia el propietario o grupo de cada archivo <ARCHIVO> a <PROPIETARIO_O_GRUPO>
La opcion -R : cambia de forma recursiva el propietario de los archivos contenido dentro del directorio 
""")
    else:
        msg_ok = inp #mensaje para escribir en el log del shell si se ejecuto correctamente el comando
        msg_err = "propietario: ha ocurrido un error: " + inp #mensaje para escribir en el log de errores si NO se ejecuto correctamente el comando
        inp = inp.replace("propietario", "chown", 1) #formateamos el input para que coincida con el comando original chown
        ret = os.system(inp) #se realiza chown
        if ret == 0:
            write_shell_log(msg_ok) #escribe en el log del shell
        else:
            write_errores_sistema_log(msg_err) #escribe en el log de errores


#9 comando para cambiar la contrasena
def psh_contrasena(inp): #inp es el input (comando completo) que recibe
    if inp == "contrasena --ayuda":
        print("""Uso: contrasena
Cambia la contrasenha del usuario actual
""")
    else:
        msg_ok = inp #mensaje para escribir en el log del shell si se ejecuto correctamente el comando
        msg_err = "contrasena: ha ocurrido un error" #mensaje para escribir en el log de errores si NO se ejecuto correctamente el comando
        inp = inp.replace("contrasena", "passwd", 1) #formateamos el input para que coincida con el comando original passwd
        ret = os.system(inp) #se realiza passwd
        if ret == 0:
            write_shell_log(msg_ok) #escribe en el log del shell
        else:
            write_errores_sistema_log(msg_err) #escribe en el log de errores


#10 comando para agregar un usuario
def psh_usuario(inp): #inp es el input (comando completo) que recibe
    if inp == "usuario --ayuda":
        print("""Uso: usuario <HORA_ENTRADA> <HORA_SALIDA> <IP>[,<IP>]... <NOMBRE_USUARIO>
Agrega un usuario nuevo con horario y una o mas ip de acceso
<HORA_ENTRADA> y <HORA_SALIDA> en formato HH:MM
""")
    else:
        msg_ok = inp #mensaje para escribir en el log del shell si se ejecuto correctamente el comando
        msg_err = "usuario: ha ocurrido un error" #mensaje para escribir en el log de errores si NO se ejecuto correctamente el comando
        inp_arr = inp.split(" ")
        if len(inp_arr) == 5:
            #luego de separar el string : inp_arr[0] = usuario ; inp_arr[1] = hora inicio ;
            #la variable inp_arr[2] = hora de salida; inp_arr[3]... = las IPs ; inp_arr[N] = el nombre del usuario
            nip = len(inp_arr) - 1
            conjunto_ip = "" #string para almacenar las ip permitidas del usuario
            for ip in range(3,nip):
                conjunto_ip = conjunto_ip + inp_arr[ip] +","
            conjunto_ip = conjunto_ip[:-1]
            #da el formato adecuado al inp
            #inp = "useradd -c " + "\"Horario " + inp_arr[1].replace(":", "") +"-"+ inp_arr[2].replace(":", "") + " IPs " + conjunto_ip + "\" " + inp_arr[nip]
            inp = "useradd " + inp_arr[nip]
            ret = os.system(inp) #se realiza useradd
            #ret = os.system(inp)
            if ret == 0:
                personal_h = inp_arr[nip]+" Horario " + inp_arr[1].replace(":", "") + "-" + inp_arr[2].replace(":","") + " IPs " + conjunto_ip #string con los horarios e IPs del usuario
                write_personal_h_log(personal_h) #escribe los horarios e IPs del usuario en un log
                write_shell_log(msg_ok) #escribe en el log del shell
            else:
                write_errores_sistema_log(msg_err) #escribe en el log de errores
        else:
            print("usuario: formato ioncorrecto")
            write_errores_sistema_log(msg_err)  # escribe en el log de errores


#11 levantar y apagar demonios (sin usar la llamada al sistema: service)
def psh_demonio(action_pid): #action_pid: str en formato <accion PID>, siendo la accion: levantar o apagar
    if action_pid == "--ayuda":
        print("""Uso: demonio levantar <ACCION>
demonio apagar <PID>
El primero: levanta o ejecuta <ACCION> como un demonio.
El segundo: termina el proceso con PID <PID>. 
""")
    else:
        msg_ok = "demonio " + action_pid #mensaje para escribir en el log del shell si se ejecuto correctamente el comando
        try:
            if action_pid[:9] == "levantar ":
                params = action_pid[9:] #el commando para ejecutar como demonio (en background)
                params_arr = params.split(" ") #separa el string de los comandos en una lista
                ret = subprocess.Popen(params_arr) #levanta demonio
                if ret == 0:
                    write_shell_log(msg_ok) #escribe en el log del shell
                else:
                    write_errores_sistema_log("Error: demonio " + action_pid) #escribe en el log de errores

            elif action_pid[:7] == "apagar ":
                pid = int(action_pid[7:]) #el PID deseado
                os.kill(pid, signal.SIGTERM) #manda una senhal term al PID
                os.kill(pid, signal.SIGKILL) #manda una senhal kill al PID
                write_shell_log(msg_ok)  # escribe en el log del shell

            else:
                print(tcolors.WARNING + "demonio: accion no encontrada: "+action_pid.split(" ", 1)[0] + tcolors.ENDC)
                write_errores_sistema_log("demonio: accion no encontrada: "+action_pid.split(" ", 1)[0]) #escribe en el log de errores
        except Exception as e:
            print(e)
            write_errores_sistema_log(e) #escribe en el log de errores


#14 transferencia ftp o scp y registrar en el Shell_transferencias.log
def psh_scp_ftp(inp): #inp es el input (comando completo) que recibe
    params = inp[4:] #string con los parametros del comando scp o ftp
    command = inp[:3] #string: el comando scp o ftp
    if params == "--ayuda":
        print("Uso: "+command+""" <PARAMS>
Ejecuta una transferencia """+command+""" de <PARAMS>
""")
    else:
        try:
            myArr = inp.split(" ")
            ret = subprocess.Popen(myArr) #se realiza el comando (ftp o scp)
            if ret == 0:
                write_shell_transferencias_log(inp)  # escribe en el log de transferencias
                write_shell_log(inp)
            else:
                write_errores_sistema_log("Error: " + inp)
        except Exception as e:
            write_errores_sistema_log(e) #escribe en el log de errores

#FUNCIONES PARA LA LECTURA Y ESCRITURA DE LOS LOGS

#escribe en el log /var/log/shell_log.log los comandos realizados por el usuario junto con el nombre del usuario que los realizo y la fecha y hora
def write_shell_log(inp):
    info = datetime.now().strftime("(%Y-%m-%d %H:%M:%S)")+" ["+getpass.getuser()+"] "+inp
    f = open("/var/log/shell_log.log","a")
    f.write(info+"\n")
    f.close()


#escribe en el log /var/log/errores_sistema.log los comandos realizados por el usuario que dieron algun error junto con el nombre del usuario que los realizo y la fecha y hora
def write_errores_sistema_log(inp):
    info = datetime.now().strftime("(%Y-%m-%d %H:%M:%S)")+" ["+getpass.getuser()+"] "+inp
    f = open("/var/log/errores_sistema.log","a")
    f.write(info+"\n")
    f.close()


#escribe en el log /var/log/Shell_transferencias.log el comando que realizo una transferencia ftp o scp junto con el nombre del usuario que los realizo y la fecha y hora
def write_shell_transferencias_log(inp):
    info = datetime.now().strftime("(%Y-%m-%d %H:%M:%S)") + " [" + getpass.getuser() + "] " + inp
    f = open("/var/log/Shell_transferencias.log", "a")
    f.write(info + "\n")
    f.close()


#escribe en el log /var/log/personal_h.log el usuario creado junto con su horario y sus IPs permitidas
def write_personal_h_log(inp):
    f = open("/var/log/personal_h.log", "a")
    f.write(inp + "\n")
    f.close()


#lee del log /var/log/personal_h.log y retorna la linea que contiene al usuario del cual se pidio el horario e IPs
def read_personal_h_log(usr): #usr: el nombre del usuario del cual se pide el horario y las IPs
    f = open("/var/log/personal_h.log", "r")
    content = f.readline()
    with f as openfileobject:
        for line in openfileobject:
            exists = line.find(usr)
            if exists != -1:
                return line
    return ""


#escribe en el log /var/log/personal_horarios.log el nombre del usuario que inicio sesion junto con la hora y tambien la hora de su logout
#tambien escribe si el usuario inicio o cerro sesion fuera de su horario establecido o desde una IP no permitida
def write_personal_horario_log(log_in_out, usr):
    f = open("/var/log/personal_horarios_log.log", "a")
    now = datetime.now().strftime("%H:%M") #hora actual
    curr_ip = socket.gethostbyname(socket.gethostname()) #ip actual del usuario
    usr_info = read_personal_h_log(usr) #string con el horario y las IPs permitidas del usuario
    if usr_info == "" or usr_info == "\n": #si el usuario no tiene un horario o IP registrada entonces simplemente se escribe sin ningun prpoblema en el log
        if log_in_out == "login":
            f.write("[" + usr + "] Ip: " + curr_ip + " Horas: " + now)
        else:
            f.write(" --> "+now + "\n")
    else:
        usr_info = usr_info.split(" ") #lista con el horario e IPs permitidas del usuario
        h_entrada = int(usr_info[2].split("-")[0]) #hora de entrada (obtenida de su horario)
        h_salida = int(usr_info[2].split("-")[1]) #hora de salida (obtenida de su horario)
        ips = usr_info[4].split(",") #lista con las IPs permitidas del usuario
        int_now = int(now.replace(":","")) #formatea la hora actual a un entero. Ej: 13:00 --> 1300, para comparar mas adelante con la hora de entrada y salida
        info = ""
        if log_in_out == "login": #caso login
            info = info + "[" + usr + "] Ip: " + curr_ip + " "
            ip_match = False
            for ip in ips: #busca si la IP actual se encuentra en la lista de IPs permitidas
                if ip == curr_ip:
                    ip_match = True #la IP se encuentra en la lista
                    break
            if not ip_match:
                info = info + "(La Ip no coincide con su lista de IPs permitidas) "

            if h_entrada <= int_now <= h_salida: #compara si la hora actual se encuentra dentro de su horario establecido
                info = info + "Horas: " + now
            else:
                info = info + "Horas: " + now + " (Login fuera de horario) "
            f.write(info)
        else: #caso logout
            if h_entrada <= int_now <= h_salida: #compara si la hora actual se encuentra dentro de su horario establecido
                info = info +" --> "+ now
            else:
                info = info +" --> " + now + " (Logout fuera de horario)"
            f.write(info + "\n")
    f.close()

#FUNCIONES EXTRAS

#permite utilizar las flechas del teclado para desplazarse de izquierda a derecha en el comando que se encuentra escribiendo
#y tambien permite utilizar las flechas arriba y abajo para ver los comandos realizados anteriormente/recientemente
def shell_autocomplete():
    #autocomletado utililzando la techa de tabulacion
    readline.parse_and_bind('tab: complete')
    #archivo que contiene el historial de comandos realizados
    histfile = os.path.join(os.environ['HOME'], '.pythonhistory')
    try:
        readline.read_history_file(histfile)
    except IOError:
        pass
    atexit.register(readline.write_history_file, histfile)
    del os, histfile, readline, rlcompleter



#cambia de directorio mediante el comando cd (similar a la funcion psh_ir)
def psh_cd(path): #path es el path al directorio al cual vamos a cambiar
    """convert to absolute path and change directory"""
    try:
        path = path_formater(path)
        os.chdir(os.path.abspath(path)) #cambia de direcotrio
    except Exception:
        print(tcolors.WARNING+"cd: no such file or directory: {}".format(path)+tcolors.ENDC)


#imprime en pantalla el menu de ayuda
def psh_help():
    print(welcomemsg + """
Soporta todos los comandos basicos de un shell de UNIX
Por ejemplo:
cd                      ls
mkdir                   rmdir
touch                   rm
help                    exit

Para mas ayuda con estos comandos: <comando> --help o <comando> -h

Tambien soporta algunos comandos personalizados:
copiar              Equivalente a 'cp'. Copia un archivo o un directorio completo a la ubicacion especificada
mover               Equivalente a 'mv'. Mueva la ubicacion de un archivo o de un directorio completo
renombrar           Renombra un archivo.
listar              Equivalente a 'ls'. Lista todos los directorios que se encuentran edentro de cierto directorio mencionado
creardir            Equivalente a 'mkdir'. Crea un directorio en un lugar especificado.
ir                  Equivalente a 'cd'. Cambia de directorio al directorio especificado
permisos            Equivalente a 'chmod'. Cambia los permisos de uno o mas archivos
propietario         Equivalente a 'chown'. Cambia el usuario duenho de un archivo
contrasena          Equivalente a 'passwd'. Cambia la contrasenha del usuario
usuario             Equivalente a 'useradd' pero tambien agrega horario e ip's esperadas del usuario 
ayuda               Equivalente a 'help'. Despliega un menu de ayuda (el que se encuentra viendo actualmente)
salir               Equivalente a 'exit'. Cierra/termina la linea de comando (usar solo si tiene interfaz grafica)
demonio             Permite levantar o apagar un demonio
scp                 Transferencia scp
ftp                 Transferencia ftp

Para mas ayuda con estos comandos: <comando> --ayuda
""")


#FUNCIONES PARA FORMATEAR PATH

#retorna el path actual luego de sustituir el directorio home en el path por la virgulilla (~)
def virgulilla_path():
    fullpath=os.getcwd() #el directorio actual
    homedir = os.environ['HOME'] #el directorio home
    newpath = fullpath.replace(homedir,'~',1) # cambiamos el directorio home por ~
    return newpath


#da el formato adecuado al path
def path_formater(path):
    homedir = os.environ['HOME']  #el directorio home
    newpath = path.replace('~',homedir, 1) #remplace la virgulilla (~) por el directorio home
    if newpath[:1] != "/": # si el path no empieza con el caracter '/' entonces agrega al comienzo del path el directorio actual
        newpath = os.getcwd() + "/"+ newpath
    return newpath


#FUNCION MAIN

def main():
    username = getpass.getuser()

    write_personal_horario_log("login",username) #escribe en el log que el usuario ha iniciado sesion junto con la hora e IP
    exit = False

    print(welcomemsg + """
Ejecute el comando ayuda para obtener mas informacion.    
""")
    while True: #ciclo para evaluar el input del usuario
        inp = input(tcolors.BOLD+tcolors.OKGREEN+getpass.getuser()+tcolors.ENDC+tcolors.BOLD+":"+tcolors.OKBLUE+virgulilla_path()+tcolors.ENDC+"$ ") #input (comando) ingresado por el usuario
        if inp == "exit" or inp == "salir":
            write_personal_horario_log("logout", username) #escribe en el log que el usuario ha cerrado sesion junto con la hora e IP
            exit = True
            break
        elif inp == "cd":
            psh_cd(os.environ['HOME'])
        elif inp[:3] == "cd ":
            psh_cd(inp[3:])
        elif inp == "help" or inp == "ayuda":
            psh_help()
        elif inp[:3] == "ir ":
            psh_ir(inp[3:])
        elif inp == "ir":
            psh_cd(os.environ['HOME'])
        elif inp == "listar":
            psh_listar(os.getcwd())
        elif inp[:7] == "listar ":
            psh_listar(inp[7:])
        elif inp[:7] == "copiar ":
            psh_copiar(inp[7:])
        elif inp[:6] == "mover ":
            psh_mover(inp)
        elif inp[:10] == "renombrar ":
            psh_renombrar(inp)
        elif inp[:9] == "creardir ":
            psh_creardir(inp)
        elif inp[:9] == "permisos ":
            psh_permisos(inp)
        elif inp[:12] == "propietario ":
            psh_propietario(inp)
        elif inp[:11] == "contrasena ":
            psh_contrasena(inp)
        elif inp[:8] == "usuario ":
            psh_usuario(inp)
        elif inp[:4] == "scp " or inp[:4] == "ftp ":
            psh_scp_ftp(inp)
        elif inp[:8] == "demonio ":
            psh_demonio(inp[8:])
        elif inp == "":
            #para que no diga "comando no encontrado" cuando el usuario solamente presiona enter
            fghjlfkhjg = 1 #no hace nada, esta puesto para cumplir con la sintaxis de python
        elif inp[:3] == "su " or inp[:9] == "shutdown ":
            write_personal_horario_log("logout", username)  # escribe en el log que el usuario ha cerrado sesion junto con la hora e IP
            ret = os.system(inp)  # ejecuta el comando inp
            if ret == 0:
                exit = True
                write_shell_log(inp)  # escribe en el log del shell
                break;
            else:
                write_errores_sistema_log(inp)  # escribe en el log de errores
        else:
            ret = os.system(inp) #ejecuta el comando inp
            if ret == 0:
                write_shell_log(inp) #escribe en el log del shell
            else:
                write_errores_sistema_log(inp) #escribe en el log de errores
    if exit: #sale hasta la pantalla de login
        os.system("fuser -k "+ os.ttyname(1)) #kill todos los procesos del tty actual



if '__main__' == __name__:
    main()
