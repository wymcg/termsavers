import noise as n
import numpy as np
import random
import curses
import math
import threading
import argparse

#default args
scale = 100
octaves = 6
xspeed = 1
yspeed = .75
adjust = .1
colors = [17, 18, 19, 20, 21, 228, 41, 40, 34, 28, 22, 245, 244, 243, 242, 241, 240]

#argument parser
parser = argparse.ArgumentParser(description='Fly over a randomly generated landmass')

parser.add_argument("-s", "--scale", type=float, help="Set size of islands. Defaults to 50")
parser.add_argument("-o", "--octaves", type=int, help="Set level of detail for islands. Defaults to 6")
parser.add_argument("--hspeed", type=float, help="Set x component of flyover speed. Defaults to .1")
parser.add_argument("--vspeed", type=float, help="Set y component of flyover speed. Defaults to .1")
parser.add_argument("-S", "--size", type=float, help="Set the size of landmasses. Defaults to .1. Values higher than .3 are not reccomended.")

args = parser.parse_args()

#set args if necessary
if args.scale:
    scale = args.scale
if args.octaves:
    octaves = args.octaves
if args.vspeed:
    xspeed = args.vspeed
if args.hspeed:
    yspeed = args.hspeed
if args.size:
    adjust = args.size

#curses setup
screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)
curses.start_color()
curses.use_default_colors()


#get rows and columns
rows = curses.LINES
columns = curses.COLS-1

#setup colors
for i in range(len(colors)):
    curses.init_pair(i+1, 0, colors[i])

#setup array
arr = np.zeros((rows, columns))

#setup offsets
xoff = random.randint(0, 1000)
yoff = random.randint(0, 1000)

#other constants
perlinMax = math.sqrt(3)/4
ncolors = len(colors)
gap = perlinMax / ncolors

#main loop
while True:
    try:

        #assign values to array
        for x in range(rows):
            for y in range(columns):
                arr[x][y] = n.pnoise2((x+xoff)/scale, (y+yoff)/(2*scale), octaves) + adjust

        xoff += xspeed
        yoff += yspeed

        #draw
        for x in range(rows):
            for y in range(columns):
                setcolor = 1
                for i in range(ncolors + 1):
                    if gap * i + 1 >= arr[x][y] > gap * i:
                        setcolor = i + 2
                screen.addch(x, y, ' ', curses.color_pair(setcolor))

        screen.refresh()

    except KeyboardInterrupt:
        curses.curs_set(1)
        exit()
