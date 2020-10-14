import curses as c
import noise as n
import numpy as np
import math
import argparse
import random

#default params
scale = 50
octaves = 2
speed = .001
colors = [0, 124, 125, 126, 127, 128, 129]

#argument parser
parser = argparse.ArgumentParser(description="Stay groovy with a virtual lava lamp")

parser.add_argument("-s", "--scale", type=float, help="Set size of blobs. Defaults to 50")
parser.add_argument("-o", "--octaves", type=int, help="Set level of detail when generating blobs. Defaults to 2")
parser.add_argument("-S", "--speed", type=float, help="Set speed of blobs. defaults to .001")

args = parser.parse_args()

#apply args
if args.scale:
    scale = args.scale
if args.octaves:
    octaves = args.octaves
if args.speed:
    speed = args.speed

#setup curses
screen = c.initscr()
c.noecho()
c.cbreak()
c.curs_set(0)
c.start_color()
c.use_default_colors()

#get screen size
rows = c.LINES
columns = c.COLS - 1

#setup color pairs
for i in range(len(colors)):
    c.init_pair(i+1, 0, colors[i])

#setup array
arr = np.zeros((rows, columns))

z = 0
xoff = random.uniform(0, 1000)
yoff = random.uniform(0, 1000)
ncolors = len(colors)
perlinMax = math.sqrt(3)/4
gap = perlinMax / ncolors

#main loop
while True:
    try:
        #assign values to array
        for x in range(rows):
            for y in range(columns):
                arr[x][y] = n.snoise3((x+xoff)/scale, (y+yoff)/(2*scale), z, octaves)

        #draw to screen
        for x in range(rows):
            for y in range(columns):
                setcolor = 1
                for i in range(ncolors - 1):
                    if gap * i+1 >= arr[x][y] > gap * i:
                        setcolor = i + 2
                screen.addch(x, y, ' ', c.color_pair(setcolor))


        screen.refresh()
        z += speed 
    except KeyboardInterrupt:
        c.curs_set(1)
        exit()
