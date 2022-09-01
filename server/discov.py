import socket
import sys
import json

# This system is heavily derived from jholtmann's ip_discovery.
# Check it out at github.com/jholtmann/ip_discovery

# allow to be used as a utility module
def main():
    # TODO: support dynamic conf file location
    conf = json.load(open("discovsets.json", "r"))
    # creates the basic socket object (AF_INET + SOCK_DGRAM = UDP)
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # bind takes (host, port)
    sck.bind((conf["host"], conf["port"]))

    # leave lock handling to http server
    # keep going - no need to reset to redeliver
    while True:
        d, a = sck.recvfrom(1024)
        d = str(d.decode('UTF-8')).strip()
        if d == conf["trigger"]:
            sent = sck.sendto(conf["response"].encode(), a)

if __name__ == "__main__":
    main()
