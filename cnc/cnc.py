# OPS = OpenPrompter Software

from socket import *
import json
import time

import requests

conf = json.load(open("cncsets.json", "r"))

act = None
cm = 0
fla = True

insmap = {
    "lo": "127.0.0.1"
}

def ping(q: list[str]):
    print(requests.get(f"http://{insmap[q[1]]}:{conf['appport']}/identify").json())

def detect(q: list[str]):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    sock.settimeout(conf["timeout"])
    fail = True
    try:
        print("Sending UDP discov request...")
        sock.sendto(conf["challenge"].encode(), (conf["network_broadcast"], conf["discovport"]))
        print("Sent, awaiting response...")
        dat, sinfo = sock.recvfrom(1024)
        if dat.decode("UTF-8") == conf["resp"]:
            ip = str(sinfo[0])
            print(f"Confirmation recieved! IP: {ip}")
            tn = requests.get(f"http://{ip}:{conf['appport']}/identify").json()
            ta = input(f"Name of server: {tn}. Name [default]: ")
            if ta == "":
                ta = tn
            insmap[ta] = ip
            fail = False
    finally:
        if fail:
            print("Something went wrong. Please try again.")
        sock.close()

def sel(q: list[str]):
    global act
    if act is not None:
        requests.get(f"http://{insmap[act]}:{conf['appport']}/setmode?mode=0")
    act = q[1]
    if act == "None":
        act = None
        return
    requests.get(f"http://{insmap[act]}:{conf['appport']}/setmode?mode=1")
    zero([""])
    
def zero(q: list[str]):
    if act is None:
        return
    a = requests.get(f"http://{insmap[act]}:{conf['appport']}/absmod?n=0")
    for n in a.json():
        print(n.strip())

def ops_q(q: list[str]):
    global fla
    fla = False

def conns(q: list[str]):
    print("Connected devices:")
    for n in insmap:
        print(f"{n}: {insmap[n]}")

def flush(q: list[str]):
    global act
    for n in insmap:
        requests.get(f"http://{insmap[n]}:{conf['appport']}/setmode?mode=0")
    print("Flush successful")
    act = None

def drop(q: str):
    del insmap[q[1]]

adv_tbl = {
    "d": 1,
    "u": -1
}

def advance(q: list[str]):
    if act is None:
        return
    a = requests.get(f"http://{insmap[act]}:{conf['appport']}/modposrel?n={int(q[1]) * adv_tbl[q[0]]}")
    print("\n\n\n")
    for i in a.json():
        print(i.strip())
    print("\n\n\n")

def adv_continuous(q: list[str]):
    for i in range(int(q[1])):
        time.sleep(float(q[2]))
        advance(["d", "1"])

def down_single(q: list[str]):
    advance(["d", "1"])

def up_single(q: list[str]):
    advance(["u", "1"])

def create_script(q: list[str]):
    f = open(q[2], "r")
    requests.post(f"http://{insmap[q[1]]}:{conf['appport']}/createscript?file={q[2]}", data=f.read())
    f.close()

def load_script(q: list[str]):
    requests.get(f"http://{insmap[q[1]]}:{conf['appport']}/loadscript?name={q[2]}")

fnmap = {
    "q": ops_q,
    "quit": ops_q,
    "discov": detect,
    "detect": detect,
    "select": sel,
    "sel": sel,
    "s": sel,
    "p": conns,
    "conns": conns,
    "showdev": conns,
    "flush": flush,
    "drop": drop,
    "delink": drop,
    "d": advance,
    "u": advance,
    "mt": adv_continuous,
    "z": zero,
    "1": down_single,
    "2": up_single,
    "ping": ping,
    "csc": create_script,
    "lsc": load_script
}

while fla:
    q = input(f"[cnc@ops {act}]$ ")
    try:
        a = q.split()
        fnmap[a[0]](a)
    except Exception as e:
        print("An error occurred:", e)
