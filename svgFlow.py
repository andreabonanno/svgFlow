import drawSvg
import noise
import random
import math
import numpy as np

sizex = 950
sizey = 500
noisescale = 400
persistence = 0.5
lacunarity = 2
seed = random.randint(0, 100)
actorsnum = 1000
stepsnum = 50
steplenght = 2
noisemap = np.zeros((sizex, sizey))

for i in range(sizex):
    for j in range(sizey):
        noisemap[i][j] = noise.pnoise2(i / noisescale, j / noisescale, octaves=2, persistence=persistence,
                                       lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=seed)
map_max = np.max(noisemap)
map_min = np.min(noisemap)
map_range = map_max - map_min

for i in range(sizex):
    for j in range(sizey):
        k = noisemap[i][j]
        k = (k - map_min)/map_range
        noisemap[i][j] = k
map_max = np.max(noisemap)
map_min = np.min(noisemap)


def getnoise(x, y):
    return noisemap[math.floor(x)][math.floor(y)]


class Actor:
    def __init__(self):
        self.x = random.random() * sizex
        self.y = random.random() * sizey
        self.xn = self.x
        self.yn = self.y

    def step(self):
        t = getnoise(self.x, self.y) * 5 * math.pi
        self.x = self.xn
        self.y = self.yn
        self.xn += steplenght * math.cos(t)
        self.yn += steplenght * math.sin(t)
        if self.xn < 0 or self.xn > sizex or self.yn < 0 or self.yn > sizey:
            return None
        return self.xn, self.yn, self.x, self.y


canvas = drawSvg.Drawing(sizex, sizey, displayInline='False')

actors = []
for a in range(actorsnum):
    n = Actor()
    actors.append(n)
for s in range(stepsnum):
    for a in actors:
        p = a.step()
        if p:
            canvas.append(drawSvg.Line(p[2], p[3], p[0], p[1], stroke='black', stroke_width=1))
        else:
            actors.remove(a)

canvas.saveSvg('test.svg')
