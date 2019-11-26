#!/usr/bin/env python3

"""psh: a simple shell written in Python"""

import os
import subprocess
import getpass
import shutil
import itertools
#import daemon
import signal
import socket
from datetime import datetime


# imports para el historial y autocompletado
import readline
import rlcompleter
import atexit

welcomemsg = """
   __    ___  __ _          _ _ 
  / /   / __\/ _\ |__   ___| | |
 / /   / _\  \ \| '_ \ / _ \ | |
/ /___/ /    _\ \ | | |  __/ | |
\____/\/     \__/_| |_|\___|_|_|
                                v1.0.12

psh: shell implementation in Python3
Creado por Lucas Martinez & Erik Wasmosy."""

class tcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#1 comando para copiar (sin usar la llamada al sistema cp)
def psh_copiar(src_dst):
    if src_dst == "--ayuda":
        print("""Uso: copiar <PATH_ARCHIVO> <PATH_DESTINO>
Copia el archivo o directorio especificado en <PATH_ARCHIVO> en <PATH_DESTINO>
""")
    else:
        msg_ok = "copiar "+src_dst
        msg_err = "copiar: no such file or directory, or directory already exists: "+src_dst
        paths = src_dst.split(" ")

        src = path_formater(paths[0])
        dst = path_formater(paths[1])
        try:
            shutil.copy(src, dst)
            print("copiar: "+src+" -> "+dst)
        except Exception:
            try:
                if os.path.isdir(dst):
                    name = src.rsplit("/", 1)
                    dst = dst + "/" + name[1]
                shutil.copytree(src, dst)
                print("copiar: " + src + " -> " + dst)
                write_shell_log(msg_ok)
            except Exception:
                print(tcolors.WARNING + "copiar: no such file or directory:" + tcolors.ENDC)
                print(src + " " + dst)
                write_errores_sistema_log(msg_err)


#2 comando para mover
def psh_mover(inp):
    if inp == "mover --ayuda":
        print("""Uso: mover <PATH_ARCHIVO> <PATH_DESTINO>
Mueve el archivo o directorio especificado en <PATH_ARCHIVO> a <PATH_DESTINO>
""")
    else:
        msg_ok = inp
        msg_err = "mover: no existe el archivo o directorio: " + inp.replace("mover", "", 1)
        inp = inp.replace("mover", "mv", 1)
        ret = execute_command(inp)
        if ret == 0:
            write_shell_log(msg_ok)
        else:
            write_errores_sistema_log(msg_err)


#3 comando para renombrar
def psh_renombrar(inp):
    if inp == "renombrar --ayuda":
        print("""Uso: renombrar <PATH_ARCHIVO> <NUEVO_NOMBRE>
Renombra el archivo o directorio especificado en <PATH_ARCHIVO> a <NUEVO_NOMBRE>
""")
    else:
        msg_ok = inp
        msg_err = "renombrar: no existe el archivo o directorio: "+ inp.replace("renombrar", "", 1)
        inp = inp.replace("renombrar", "mv", 1)
        ret = execute_command(inp)
        if ret == 0:
            write_shell_log(msg_ok)
        else:
            write_errores_sistema_log(msg_err)


#4 comando para listar un directorio
def psh_listar(path):
    if path == "--ayuda":
        print("""Uso: listar <PATH_DIRECTORIO>
Lista en pantalla los directorios ubicados dentro del directorio especificado en <PATH_DIRECTORIO>
""")
    else:
        msg_ok = "listar "+path
        msg_err = "listar: no existe el directorio: " + path
        #path = command.replace("listar ", "", 1)
        path = path_formater(path)
        try:
            dl = os.listdir(path)
            for t in itertools.zip_longest(dl[::2],dl[1::2],fillvalue=""):
              print(("{:<35} {:<35}").format(*t))
            write_shell_log(msg_ok)
        except Exception:
            print(tcolors.WARNING + "listar: no such file or directory: "+path+ tcolors.ENDC)
            write_errores_sistema_log(msg_err)


#5 comando para crear un directorio
def psh_creardir(inp):
    if inp == "creardir --ayuda":
        print("""Uso: creardir <PATH_DIRECTORIO>
Crea un nuevo directorio <PATH_DIRECTORIO>
""")
    else:
        msg_ok = inp
        msg_err = "creardir: el directorio ya existe: "+ inp.replace("creardir", "", 1)
        inp = inp.replace("creardir", "mkdir", 1)
        ret = execute_command(inp)
        if ret == 0:
            write_shell_log(msg_ok)
        else:
            write_errores_sistema_log(msg_err)


#6 comando para cambiar de directorio (sin usar la llamada al sistema cd)
def psh_ir(path):
    if path == "--ayuda":
        print("""Uso: ir <PATH_DIRECTORIO>
Cambia el directorio donde se encuentra al directorio <PATH_DIRECTORIO>
""")
    else:
        msg_ok = "ir: " + path
        msg_err = "ir: no existe el directorio o es un archivo: " + path
        #path = command.replace("ir ", "", 1)
        path = path_formater(path)
        try:
            os.chdir(path)
            write_shell_log(msg_ok)
        except Exception:
            print(tcolors.WARNING + "ir: no such file or directory: " + path + tcolors.ENDC)
            write_errores_sistema_log(msg_err)


#7 comando para cambiar los permisos de uno o mas archivos
def psh_permisos(inp):
    if inp == "permisos --ayuda":
        print("""Uso: permisos <PERMISOS>[,<PERMISOS>]... <ARCHIVO>...
Cambia los permisos de cada archivo <ARCHIVO> a <PERMISOS>
""")
    else:
        msg_ok = inp
        msg_err = "permisos: ha ocurrido un error: " + inp
        inp = inp.replace("permisos", "chmod", 1)
        ret = execute_command(inp)
        if ret == 0:
            write_shell_log(msg_ok)
        else:
            write_errores_sistema_log(msg_err)


#8 comando para cambiar los propietarios de uno o mas archivos
def psh_propietario(inp):
    if inp == "propietario --ayuda":
        print("""Uso: propietario <PROPIETARIO_O_GRUPO> <ARCHIVO>...
Cambia el propietario o grupo de cada archivo <ARCHIVO> a <Propietario_O_GRUPO>
""")
    else:
        msg_ok = inp
        msg_err = "propietario: ha ocurrido un error: " + inp
        inp = inp.replace("propietario", "chown", 1)
        ret = execute_command(inp)
        if ret == 0:
            write_shell_log(msg_ok)
        else:
            write_errores_sistema_log(msg_err)


#9 comando para cambiar la contrasena
def psh_contrasena(inp):
    if inp == "contrasena --ayuda":
        print("""Uso: contrasena
Cambia la contrasenha del usuario actual
""")
    else:
        msg_ok = inp
        msg_err = "contrasena: ha ocurrido un error"
        inp = inp.replace("contrasena", "passwd", 1)
        ret = execute_command(inp)
        if ret == 0:
            write_shell_log(msg_ok)
        else:
            write_errores_sistema_log(msg_err)


#10 comando para agregar un usuario
def psh_usuario(inp):
    if inp == "usuario --ayuda":
        print("""Uso: usuario <HORA_ENTRADA> <HORA_SALIDA> <IP>[,<IP>]... <NOMBRE_USUARIO>
Agrega un usuario nuevo con horario y una o mas ip de acceso
<HORA_ENTRADA> y <HORA_SALIDA> en formato HH:MM
""")
    else:
        msg_ok = inp
        msg_err = "usuario: ha ocurrido un error"
        inp_arr = inp.split(" ")
        #luego de separar la string : inp_arr[0] = usuario ; inp_arr[1] = hora inicio ;
        # inp_arr[2] = hora de salida; inp_arr[3]... = las IPs ; inp_arr[N] = el nombre del usuario
        nip = len(inp_arr) - 1
        conjunto_ip = ""
        for ip in range(3,nip):
            conjunto_ip = conjunto_ip + inp_arr[ip] +","
        conjunto_ip = conjunto_ip[:-1]
        inp = "useradd -c " + "\"Horario " + inp_arr[1].replace(":", "") +"-"+ inp_arr[2].replace(":", "") + " IPs " + conjunto_ip + "\" " + inp_arr[nip]
        #inp2 = inp2.replace("usuario", "useradd -c", 1)
        #print(inp)
        ret = os.system(inp)
        #ret = execute_command(inp)
        if ret == 0:
            personal_h = inp_arr[nip]+" Horario " + inp_arr[1].replace(":", "") + "-" + inp_arr[2].replace(":","") + " IPs " + conjunto_ip
            write_personal_h_log(personal_h)
            write_shell_log(msg_ok)
        else:
            write_errores_sistema_log(msg_err)


#11 levantar y apagar demonios (sin usar la llamada al sistema: service)
def psh_demonio(action_pid):
    if action_pid == "--ayuda":
        print("""Uso: demonio levantar <ACCION>
demonio apagar <PID>
El primero: levanta o ejecuta <ACCION> como un demonio.
El segundo: termina el proceso con PID <PID>. 
""")
    else:
        try:
            if action_pid[:9] == "levantar ":
                params = action_pid[9:]
                params_arr = params.split(" ")
                #with daemon.DaemonContext():
                subprocess.Popen(params_arr)

            elif action_pid[:7] == "apagar ":
                pid = int(action_pid[7:])
                os.kill(pid, signal.SIGTERM)
                os.kill(pid, signal.SIGKILL)
            else:
                print(tcolors.WARNING + "demonio: accion no encontrada: "+action_pid.split(" ", 1)[0] + tcolors.ENDC)
        except Exception as e:
            print(e)


#14 transferencia ftp o scp y registrar en el Shell_transferencias.log
def psh_scp_ftp(inp):
    params = inp[4:]
    command = inp[:3]
    write_shell_transferencias_log(inp)
    subprocess.Popen([command, params])


def write_shell_log(inp):
    info = datetime.now().strftime("(%Y-%m-%d %H:%M:%S)")+" ["+getpass.getuser()+"] "+inp
    f = open("/var/log/shell_log.log","a")
    f.write(info+"\n")
    f.close()


def write_errores_sistema_log(inp):
    info = datetime.now().strftime("(%Y-%m-%d %H:%M:%S)")+" ["+getpass.getuser()+"] "+inp
    f = open("/var/log/errores_sistema.log","a")
    f.write(info+"\n")
    f.close()


def write_shell_transferencias_log(inp):
    info = datetime.now().strftime("(%Y-%m-%d %H:%M:%S)") + " [" + getpass.getuser() + "] " + inp
    f = open("/var/log/Shell_transferencias.log", "a")
    f.write(info + "\n")
    f.close()


def write_personal_h_log(inp):
    f = open("/var/log/personal_h.log", "a")
    f.write(inp + "\n")
    f.close()


def read_personal_h_log(usr):
    f = open("/var/log/personal_h.log", "r")
    content = f.readline()
    with f as openfileobject:
        for line in openfileobject:
            exists = line.find(usr)
            if exists != -1:
                return line
    return ""


def write_personal_horario_log(log_in_out, usr):
    f = open("/var/log/personal_horarios_log.log", "a")
    now = datetime.now().strftime("%H:%M")
    curr_ip = socket.gethostbyname(socket.gethostname())
    usr_info = read_personal_h_log(usr)
    if usr_info == "" or usr_info == "\n":
        if log_in_out == "login":
            f.write("[" + usr + "] Ip: " + curr_ip + " Horas: " + now)
        else:
            f.write(" --> "+now + "\n")
    else:
        usr_info = usr_info.split(" ")
        h_entrada = int(usr_info[2].split("-")[0])
        h_salida = int(usr_info[2].split("-")[1])
        ips = usr_info[4].split(",")
        int_now = int(now.replace(":",""))
        info = ""
        if log_in_out == "login":
            info = info + "[" + usr + "] Ip: " + curr_ip + " "
            ip_match = False
            for ip in ips:
                if ip == curr_ip:
                    ip_match = True
                    break
            if not ip_match:
                info = info + "(La Ip no coincide con su lista de IPs permitidas) "

            if h_entrada <= int_now <= h_salida:
                info = info + "Horas: " + now
            else:
                info = info + "Horas: " + now + " (Login fuera de horario) "
            f.write(info)
        else:
            if h_entrada <= int_now <= h_salida:
                info = info +" --> "+ now
            else:
                info = info +" --> " + now + " (Logout fuera de horario)"
            f.write(info + "\n")
    f.close()


def shell_autocomplete():
    # tab completion
    readline.parse_and_bind('tab: complete')
    # history file
    histfile = os.path.join(os.environ['HOME'], '.pythonhistory')
    try:
        readline.read_history_file(histfile)
    except IOError:
        pass
    atexit.register(readline.write_history_file, histfile)
    del os, histfile, readline, rlcompleter

def execute_command(command):
    ret = 0
    """execute commands and handle piping"""
    try:
        if "|" in command:
            # guardamos copia para restaurar mas tarde
            s_in, s_out = (0, 0)
            s_in = os.dup(0)
            s_out = os.dup(1)

            # el primer comando toma commandut de stdin
            fdin = os.dup(s_in)

            # iterar todos los comandos en los que hay pipe
            for cmd in command.split("|"):
                # fdin va a ser stdin si es la primera iteracion
                # y la parte final del pipe si no.
                os.dup2(fdin, 0)
                os.close(fdin)

                # restaurar stdout si este es el ultimo comando
                if cmd == command.split("|")[-1]:
                    fdout = os.dup(s_out)
                else:
                    fdin, fdout = os.pipe()

                # redireccionar stdout al pipe
                os.dup2(fdout, 1)
                os.close(fdout)

                try:
                    retaux = subprocess.run(cmd.strip().split())
                    if retaux.returncode != 0:
                      ret = 1
                except Exception:
                    print(tcolors.WARNING+"psh: command not found: {}".format(cmd.strip())+tcolors.ENDC)
                    ret = 1

            # restaurar stdout y stdin
            os.dup2(s_in, 0)
            os.dup2(s_out, 1)
            os.close(s_in)
            os.close(s_out)
        else:
            retaux = subprocess.run(command.split(" "))
            if retaux.returncode != 0:
              ret = 1

    except Exception:
        print(tcolors.WARNING+"psh: command not found: {}".format(command)+tcolors.ENDC)
        ret = 1
    return ret


def psh_cd(path):
    """convert to absolute path and change directory"""
    try:
        os.chdir(os.path.abspath(path))
    except Exception:
        print(tcolors.WARNING+"cd: no such file or directory: {}".format(path)+tcolors.ENDC)


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


def virgulilla_path():
    fullpath=os.getcwd() # retorna el directorio actual
    homedir = os.environ['HOME'] # retorna el directorio home
    newpath = fullpath.replace(homedir,'~',1) # cambiamos el directorio home por ~
    return newpath

def path_formater(path):
    homedir = os.environ['HOME']  # retorna el directorio home
    newpath = path.replace('~',homedir, 1)
    if newpath[:1] != "/":
        newpath = os.getcwd() + "/"+ newpath
    return newpath

def login():
    user = input("User: ")
    #pwd = getpass.getpass(prompt="Contrasena: ")
    #ret = subprocess.Popen(["su", "-", user, "&"])
    ret = os.system("su - " + user + " &")
    print(ret)
    return ret


def main():
    username = getpass.getuser()

    write_personal_horario_log("login",username)


    print(welcomemsg + """
Ejecute el comando ayuda para obtener mas informacion.    
""")
    while True:
        inp = input(tcolors.BOLD+tcolors.OKGREEN+getpass.getuser()+tcolors.ENDC+tcolors.BOLD+":"+tcolors.OKBLUE+virgulilla_path()+tcolors.ENDC+"$ ")
        if inp == "exit" or inp == "salir":
            write_personal_horario_log("logout", username)
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
        else:
            if inp[:3] == "su " or inp[:9] == "shutdown ":
                write_personal_horario_log("logout", username)

            ret = os.system(inp)
            #ret = execute_command(inp)
            if ret == 0:
                write_shell_log(inp)
            else:
                write_errores_sistema_log(inp)


if '__main__' == __name__:
    main()
