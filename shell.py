#!/usr/bin/env python3

"""psh: a simple shell written in Python"""

import os
import subprocess


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
                    print("psh: command not found: {}".format(cmd.strip()))

            # restaurar stdout y stdin
            os.dup2(s_in, 0)
            os.dup2(s_out, 1)
            os.close(s_in)
            os.close(s_out)
        else:
            subprocess.run(command.split(" "))
    except Exception:
        print("psh: command not found: {}".format(command))


def psh_cd(path):
    """convert to absolute path and change directory"""
    try:
        os.chdir(os.path.abspath(path))
    except Exception:
        print("cd: no such file or directory: {}".format(path))


def psh_help():
    print("""psh: shell implementation in Python.
          Supports all basic shell commands.""")


def main():
    while True:
        inp = input("$ ")
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