import sys
import psutil
import subprocess
import time

def check_arguments():
    if len(sys.argv) != 2:
        print('Uso: python check_nodejs_server.py nombre_del_servidor.js')
        sys.exit(1)

def is_nodejs_server_running(server_name):
    for proc in psutil.process_iter(attrs=['cmdline']):
        if proc.info.get('cmdline') and server_name in ' '.join(proc.info['cmdline']):
            return True
    return False

def start_nodejs_server(server_name):
    try:
        subprocess.Popen(['node', server_name])
    except Exception as e:
        print(f"No se pudo iniciar el servidor {server_name}: {e}")

if __name__ == '__main__':
    check_arguments()
    server_name = sys.argv[1]

    while True:
        if not is_nodejs_server_running(server_name):
            start_nodejs_server(server_name)
        time.sleep(60)
