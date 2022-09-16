import subprocess
import socket
import time
import threading
import binascii
import shutil
import sys
import socketserver
import re
import os
import getpass
import functools
import http.server
from django.http import HttpResponseRedirect,HttpResponse
import json




try:
    HOSTNAME = socket.gethostname().lower()
    LOCAL_IP = socket.gethostbyname(HOSTNAME)
except socket.gaierror:
    LOCAL_IP = "127.0.0.1"

try:
    import _winreg as winreg
except ImportError:
    winreg = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ALL_IP = "0.0.0.0"
IP_REGEX = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
CALLBACK_REGEX = r"https?://" + IP_REGEX + r":\d+"
CMD_PATH = os.environ.get("COMSPEC")
USER_NAME = getpass.getuser().lower()

SUCCESS = 0
GENERAL_ERROR = 1
MISSING_DEPENDENCIES = 2
MISSING_PSEXEC = 3
UNSUPPORTED_RTA = 4
ACCESS_DENIED = 5

# Amount of seconds a command should take at a minimum.
# This can allow for arbitrary slow down of scripts
MIN_EXECUTION_TIME = 0

MAX_HOSTS = 64





def execute(command, hide_log=False, mute=False, timeout=30, wait=True, kill=False, drop=False, shell=True):
    """Execute a process and get the output."""




    if isinstance(command, list):

        command = subprocess.list2cmdline([arg.encode('utf-8') for arg in command])
        #command = subprocess.run(command,text=True,shell=True)
        #command = subprocess.run(command, text=True, shell=True, capture_output=True ,encoding='utf-8')
        #command=command.stdout
        #return command

    if not hide_log:
        print("%s > %s" % (HOSTNAME, command))

    stdin = subprocess.PIPE
    stdout = subprocess.PIPE
    stderr = subprocess.STDOUT

    if drop or kill:
        devnull = open(os.devnull, "w")
        stdout = devnull
        stderr = devnull

    start = time.time()
    p = subprocess.Popen(command, stdin=stdin, stdout=stdout, stderr=stderr, shell=True, text=True ,encoding='utf-8')



    if kill:

        delta = 0.5
        # Try waiting for the process to die
        for _ in range(int(timeout / delta) + 1):
            time.sleep(delta)
            if p.poll() is not None:
                return

        log("Killing process", str(p.pid))
        try:
            p.kill()
            time.sleep(0.5)
        except OSError:
            pass



    elif wait:
        print("test1")
        output = ''

        p.stdin.write(os.linesep)
        print("test2")
        while p.poll() is None:
            line = p.stdout.readline()
            if line:
                output += line
                if not (hide_log or mute):
                    print(line.rstrip())

        output += p.stdout.read()
        output = output.strip()

        # Add artificial sleep to slow down command lines
        end = time.time()
        run_time = end - start
        if run_time < MIN_EXECUTION_TIME:
            time.sleep(MIN_EXECUTION_TIME - run_time)

        if not (hide_log or mute):
            if p.returncode != 0:
                print("exit code = %d" % p.returncode)
            print("")
        return p.returncode, output
    else:
        return p




def log(message, log_type='+'):
    print("{} {}".format(log_type, message))
    pass



