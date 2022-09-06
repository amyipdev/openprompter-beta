import pygame as p
import pygame.locals as k
import cv2

import sys
import json
import os.path
import time

RGB_BLACK = (0, 0, 0)
RGB_WHITE = (0xff, 0xff, 0xff)

PSL = "pygsets.json"

def retime() -> int:
    return os.path.getmtime(PSL)

def reconf():
    return json.load(open(PSL, "r"))

conf = reconf()
lmd = retime()

def get_fs_fl():
    if conf["fullscreen"]:
        #return p.FULLSCREEN
        return 0
    else:
        return 0

# TODO: support manually choosing the camera in config
cam = cv2.VideoCapture(0)
cam.set(3, conf["dimA_x"])
cam.set(4, conf["dimA_y"])
p.init()
cl = p.time.Clock()
p.display.set_caption("OpenPrompter POC")
screen = p.display.set_mode((conf["dim_x"], conf["dim_y"]), flags=get_fs_fl())

font = p.font.Font(conf["fontfile"], conf["fontsize"])
script = open(conf["scriptfile"]).read().splitlines()

while True:
    if lmd != retime():
        lmd = retime()
        conf = reconf()
        time.sleep(0.1 / conf["fps"])
        with open(conf["scriptfile"], "r") as f:
            script = f.read().splitlines()
            f.close()
    screen.fill(RGB_BLACK)
    mode = conf["mode"]
    if mode == 0:
        r, fe = cam.read()
        fe = cv2.cvtColor(fe, cv2.COLOR_BGR2RGB)
        fe = fe.swapaxes(0, 1)
        fe = cv2.resize(fe, (conf["dim_y"], conf["dim_x"]))
        p.surfarray.blit_array(screen, fe)
    elif mode == 1:
        for n in range(conf["lpos"], min(conf["lpos"] + (
            int((conf["dim_y"] - conf["inset"]) / (1.25 * conf["fontsize"]))
            ), len(script))):
            a1 = font.render(script[n], True, RGB_WHITE)
            a2 = a1.get_rect()
            a2.centerx = conf["dim_x"] >> 1
            a2.y = conf["inset"] + ((conf["fontsize"] * 1.25) * (n-conf["lpos"]))
            screen.blit(a1, a2)
    else:
        pass
        #screen.fill(RGB_WHITE)
    p.display.update()
    for event in p.event.get():
        if event.type == p.QUIT:
            sys.exit(0)
        elif event.type == k.KEYDOWN:
            if event.key == k.K_q:
                sys.exit(0)
    cl.tick(conf["fps"])
