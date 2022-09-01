from flask import Flask, Response, request

import json
import os
import sys

RESP_OK = 200
RESP_TEAPOT = 418

conf = {}
adjconf = {}
ADJCN = "pygsets.json"
ACK = "openprompter:ack"
num = None

app = Flask(__name__)

def gen_resp(msg, n: int) -> Response:
    return Response(json.dumps(msg), status=n, mimetype="application/json")

def flush():
    json.dump(adjconf, open(ADJCN, "w"))

@app.route("/identify")
def ident():
    return gen_resp(f"openprompter:{conf['pid']}", RESP_OK)

@app.route("/")
def test():
    return gen_resp("This is an OpenPrompter instance. This is NOT a coffee pot. All interactios with this server should happen through TCP:HTTP:OPCP, not through any other protocol such as TCP:HTCPCP or TCP:HTCPCP-TEA.\n", RESP_TEAPOT)

@app.route("/ping")
def ping():
    return gen_resp("openprompter:pong", RESP_OK)

@app.route("/getall")
def dumpinfo():
    return json.dumps(adjconf)

@app.route("/setmode")
def setmode():
    global adjconf
    adjconf["mode"] = int(request.args.get("mode"))
    flush()
    return gen_resp(ACK, RESP_OK)

@app.route("/getpid")
def getpid():
    return gen_resp(num, RESP_OK)

@app.route("/updatepid")
def updatepid():
    global conf
    conf["pid"] = request.args.get("pid")
    json.dump("appsets.json")
    return gen_resp(ACK, RESP_OK)

@app.route("/setfps")
def setfps():
    global adjconf
    adjconf["fps"] = int(request.args.get("fps"))
    flush()
    return gen_resp(ACK, RESP_OK)

@app.route("/loadscript")
def ldscript():
    global adjconf
    adjconf["scriptfile"] = request.args.get("name")
    npo = request.args.get("np")
    if npo is None:
        npo = 0
    adjconf["lpos"] = npo
    flush()
    # TODO: gen_ack()
    return gen_resp(ACK, RESP_OK)

@app.route("/createscript", methods=["POST"])
def cscript():
    f = open(request.args.get("file"), "w")
    f.write(request.get_data().decode("UTF-8"))
    f.close()
    return gen_resp(ACK, RESP_OK)

@app.route("/modposrel")
def modpos():
    global adjconf
    adjconf["lpos"] += int(request.args.get("n"))
    if adjconf["lpos"] < 0:
        adjconf["lpos"] = 0
    flush()
    n = adjconf["lpos"]
    f = open(adjconf["scriptfile"])
    s = f.readlines()[n:n+conf["prev_lines"]]
    f.close()
    return gen_resp(s, RESP_OK)

@app.route("/absmod")
def absmod():
    global adjconf
    n = int(request.args.get("n"))
    adjconf["lpos"] = n
    flush()
    f = open(adjconf["scriptfile"])
    s = f.readlines()[n:n+conf["prev_lines"]]
    f.close()
    return gen_resp(s, RESP_OK)

if __name__ == "__main__":
    # TODO: make these a single file handle(?)
    conf = json.load(open("appsets.json", "r"))
    adjconf = json.load(open(ADJCN, "r"))
    app.run(host=conf["host"], port=conf["port"])
