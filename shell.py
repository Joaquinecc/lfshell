#!/usr/bin/env python3

"""psh: a simple shell written in Python"""

import os
import subprocess
import getpass


class tcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def execute_command(command):
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
                    subprocess.run(cmd.strip().split())
                except Exception:
                    print(tcolors.WARNING+"psh: command not found: {}".format(cmd.strip())+tcolors.ENDC)

            # restaurar stdout y stdin
            os.dup2(s_in, 0)
            os.dup2(s_out, 1)
            os.close(s_in)
            os.close(s_out)
        else:
            subprocess.run(command.split(" "))
    except Exception:
        print(tcolors.WARNING+"psh: command not found: {}".format(command)+tcolors.ENDC)


def psh_cd(path):
    """convert to absolute path and change directory"""
    try:
        os.chdir(os.path.abspath(path))
    except Exception:
        print(tcolors.WARNING+"cd: no such file or directory: {}".format(path)+tcolors.ENDC)


def psh_help():
    print("""psh: shell implementation in Python3 version 1.0.1.
Created by Lucas Martinez & Erik Wasmosy.
Supports all basic shell commands.
cd                      ls
mkdir                   rmdir
touch                   rm
help                    exit
""")


def virgulilla_path():
    fullpath=os.getcwd() # retorna el directorio actual
    homedir = os.environ['HOME'] # retorna el directorio home
    newpath = fullpath.replace(homedir,'~',1) # cambiamos el directorio home por ~
    return newpath


def main():
    while True:
        inp = input(tcolors.BOLD+tcolors.OKGREEN+getpass.getuser()+tcolors.ENDC+tcolors.BOLD+":"+tcolors.OKBLUE+virgulilla_path()+tcolors.ENDC+"$ ")
        if inp == "exit":
            break
        elif inp[:3] == "cd ":
            psh_cd(inp[3:])
        elif inp == "help":
            psh_help()
        else:
            execute_command(inp)


if '__main__' == __name__:
    main()
