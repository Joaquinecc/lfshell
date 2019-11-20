#!/usr/bin/env python3

"""psh: a simple shell written in Python"""

import os
import subprocess
import getpass
import shutil
import itertools
from datetime import datetime

class tcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#1 comando para copiar (sin usar llamada al sistema)
def psh_copiar(src_dst):
    if src_dst == "--ayuda":
        print("""Uso: copiar <PATH_ARCHIVO> <PATH_DESTINO>
Copia el archivo o directorio especificado en <PATH_ARCHIVO> en <PATH_DESTINO>
""")
    else:
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
            except Exception:
                print(tcolors.WARNING + "copiar: no such file or directory" + tcolors.ENDC)
                print(src + " " + dst)


#2 comando para mover
def psh_mover(inp):
    if inp == "mover --ayuda":
        print("""Uso: mover <PATH_ARCHIVO> <PATH_DESTINO>
Mueve el archivo o directorio especificado en <PATH_ARCHIVO> a <PATH_DESTINO>
""")
    else:
        inp = inp.replace("mover", "mv", 1)
        execute_command(inp)


#3 comando para renombrar
def psh_renombrar(inp):
    if inp == "renombrar --ayuda":
        print("""Uso: renombrar <PATH_ARCHIVO> <NUEVO_NOMBRE>
Renombra el archivo o directorio especificado en <PATH_ARCHIVO> a <NUEVO_NOMBRE>
""")
    else:
        inp = inp.replace("renombrar", "mv", 1)
        execute_command(inp)


#4 comando para listar un directorio
def psh_listar(path):
    if path == "--ayuda":
        print("""Uso: listar <PATH_DIRECTORIO>
Lista en pantalla los directorios ubicados dentro del directorio especificado en <PATH_DIRECTORIO>
""")
    else:
        #path = command.replace("listar ", "", 1)
        path = path_formater(path)
        try:
            dl = os.listdir(path)
            for t in itertools.zip_longest(dl[::2],dl[1::2],fillvalue=""):
              print(("{:<35} {:<35}").format(*t))
        except Exception:
            print(tcolors.WARNING + "listar: no such file or directory: "+path+ tcolors.ENDC)


#5 comando para crear un directorio
def psh_creardir(inp):
    if inp == "creardir --ayuda":
        print("""Uso: creardir <PATH_DIRECTORIO>
Crea un nuevo directorio <PATH_DIRECTORIO>
""")
    else:
        inp = inp.replace("creardir", "mkdir", 1)
        execute_command(inp)


#6 comando para cambiar de directorio (sin usar llamada al sistema)
def psh_ir(path):
    if path == "--ayuda":
        print("""Uso: ir <PATH_DIRECTORIO>
Cambia el directorio donde se encuentra al directorio <PATH_DIRECTORIO>
""")
    else:
        #path = command.replace("ir ", "", 1)
        path = path_formater(path)
        try:
            os.chdir(path)
        except Exception:
            print(tcolors.WARNING + "ir: no such file or directory: " + path + tcolors.ENDC)


#7 comando para cambiar los permisos de uno o mas archivos
def psh_permisos(inp):
    if inp == "permisos --ayuda":
        print("""Uso: permisos <PERMISOS>[,<PERMISOS>]... <ARCHIVO>...
Cambia los permisos de cada archivo <ARCHIVO> a <PERMISOS>
""")
    else:
        inp = inp.replace("permisos", "chmod", 1)
        execute_command(inp)


#8 comando para cambiar los propietarios de uno o mas archivos
def psh_propietario(inp):
    if inp == "propietario --ayuda":
        print("""Uso: propietario <PROPIETARIO_O_GRUPO> <ARCHIVO>...
Cambia el propietario o grupo de cada archivo <ARCHIVO> a <Propietario_O_GRUPO>
""")
    else:
        inp = inp.replace("propietario", "chown", 1)
        execute_command(inp)


#9 comando para cambiar la contrasena
def psh_contrasena(inp):
    if inp == "contrasena --ayuda":
        print()
    else:
        inp = inp.replace("contrasena", "passwd", 1)
        execute_command(inp)


#10 comando para agregar un usuario
def psh_usuario(inp):
    if inp == "usuario --ayuda":
        print("""Uso: contrasena
Cambia la contrasenha del usuario actual
""")
    else:
        inp = inp.replace("usuario", "useradd", 1)
        execute_command(inp)


#def service_daemons_command():
def write_shell_log(inp):
    info = datetime.now().strftime("(%Y-%m-%d %H:%M:%S)")+" "+inp
    f = open("/var/log/shell_log.log","a")
    f.write(info+"\n")
    f.close()


def write_errores_sistema_log(inp):
    info = datetime.now().strftime("(%Y-%m-%d %H:%M:%S)")+" "+inp
    f = open("/var/log/errores_sistema.log","a")
    f.write(info+"\n")
    f.close()


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
                    if(retaux.returncode != 0):
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
    print("""
   __    ___  __ _          _ _ 
  / /   / __\/ _\ |__   ___| | |
 / /   / _\  \ \| '_ \ / _ \ | |
/ /___/ /    _\ \ | | |  __/ | |
\____/\/     \__/_| |_|\___|_|_|
                                v1.0.2

psh: shell implementation in Python3
Creado por Lucas Martinez & Erik Wasmosy.
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


def main():
    while True:
        inp = input(tcolors.BOLD+tcolors.OKGREEN+getpass.getuser()+tcolors.ENDC+tcolors.BOLD+":"+tcolors.OKBLUE+virgulilla_path()+tcolors.ENDC+"$ ")
        if inp == "exit" or inp == "salir":
            break
        elif inp == "cd":
            psh_cd(os.environ['HOME'])
        elif inp[:3] == "cd ":
            psh_cd(inp[3:])
        elif inp == "help" or inp == "ayuda":
            psh_help()
        elif inp[:3] == "ir ":
            psh_ir(inp[3:])
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
        else:
           ret = execute_command(inp)
           if ret == 0:
             write_shell_log(inp)
           else:
             write_errores_sistema_log(inp)


if '__main__' == __name__:
    main()
