#!/usr/bin/env python

"""
Based of flames.py - Realtime Fire Effect Demo
Pete Shinners, April 3, 2001

Extended by M. Barth
27.11.2019
"""


import pygame, pygame.transform
from pygame.surfarray import *
from pygame.locals import *
import numpy as np
import datetime


RES = np.array((280, 200))
MAX = 246
RESIDUAL = 86
HSPREAD, VSPREAD = 26, 78
VARMIN, VARMAX = -2, 3

RED=(255,0,0)

def main():
    today = datetime.datetime.now().date()
    print (today)

    dates = get_sunday_in_advent(today.year)
    # print (dates)
    #today = datetime.date(today.year, 12, 25)

    if today < dates[0]:
       print ("Too early- Bye")
       exit()

    # main function called when the script is run
    # first we just init pygame and create some empty arrays to work with    
    pygame.init()

    f_list = []
    t1 = Rect (10, 0, 40, 100)
    t2 = Rect (80, 0, 40, 100)
    t3 = Rect (140, 0 , 40, 100)
    t4 = Rect (210, 0, 40, 100)

    c_list = []
    c1 = Rect (10, 100, 40, 100)
    c2 = Rect (80,100, 40, 100)
    c3 = Rect (140, 100, 40, 100)
    c4 = Rect (210, 100, 40, 100)

    if today >= dates[0]:
       f_list.append (t1)
       c_list.append (c1)

    if today >= dates[1]:
       f_list.append (t2)
       c_list.append (c2)

    if today >= dates[2]:
       f_list.append (t3)
       c_list.append (c3)

    if today >= dates[3]:
       f_list.append (t4)
       c_list.append (c4)


    screen = pygame.display.set_mode(RES, 0, 8)
    setpalette(screen)
    flame = np.zeros(RES / 2 + (0,3), dtype=int)
    miniflame = pygame.Surface((RES[0]/2, RES[1]/2), 0, 8)
    miniflame.set_palette(screen.get_palette())
    randomflamebase(flame)

    while 1:
        for e in pygame.event.get():
            if e.type in (QUIT,KEYDOWN,MOUSEBUTTONDOWN):
                return

        modifyflamebase(flame)
        processflame(flame)
        blitdouble(screen, flame, miniflame)

        pygame.draw.rect (screen,RED, c1)
        pygame.draw.rect (screen,RED, c2)
        pygame.draw.rect (screen,RED, c3)
        pygame.draw.rect (screen,RED, c4)

        # pygame.display.flip()
        pygame.display.update(f_list)
        pygame.display.update(c_list)


def setpalette(screen):
    # here we create a numeric array for the colormap
    gstep, bstep = 75, 150
    cmap = np.zeros((256, 3))
    cmap[:,0] = np.minimum(np.arange(256)*3, 255)
    cmap[gstep:,1] = cmap[:-gstep,0]
    cmap[bstep:,2] = cmap[:-bstep,0]
    screen.set_palette(cmap)

def randomflamebase(flame):
    # just set random values on the bottom row
    flame[:,-1] = np.random.randint(0, MAX, flame.shape[0])


def modifyflamebase(flame):
    # slightly change the bottom row with random values
    bottom = flame[:,-1]
    mod = np.random.randint(VARMIN, VARMAX, bottom.shape[0])
    np.add(bottom, mod, bottom)
    np.maximum(bottom, 0, bottom)
    #if values overflow, reset them to 0
    bottom[:] = np.choose(np.greater(bottom,MAX), (bottom,0))

def processflame(flame):
    # this function does the real work, tough to follow
    notbottom = flame[:,:-1]

    #first we multiply by about 60%
    np.multiply(notbottom, 146, notbottom)
    np.right_shift(notbottom, 8, notbottom)

    #work with flipped image so math accumulates.. magic!
    flipped = flame[:,::-1]

    #all integer based blur, pulls image up too
    tmp = flipped * 20
    np.right_shift(tmp, 8, tmp)
    tmp2 = tmp >> 1
    np.add(flipped[1:,:], tmp2[:-1,:], flipped[1:,:])
    np.add(flipped[:-1,:], tmp2[1:,:], flipped[:-1,:])
    np.add(flipped[1:,1:], tmp[:-1,:-1], flipped[1:,1:])
    np.add(flipped[:-1,1:], tmp[1:,:-1], flipped[:-1,1:])

    tmp = flipped * 80
    np.right_shift(tmp, 8, tmp)
    np.add(flipped[:,1:], tmp[:,:-1]>>1, flipped[:,1:])
    np.add(flipped[:,2:], tmp[:,:-2], flipped[:,2:])

    #make sure no values got too hot
    np.minimum(notbottom, MAX, notbottom)

def blitdouble(screen, flame, miniflame):
    # double the size of the data, and blit to screen
    blit_array(miniflame, flame[:,:-3])
    # s2 = pygame.transform.scale(miniflame, screen.get_size())
    s2 = pygame.transform.scale(miniflame, (280, 100))
    screen.blit(s2, (0,0))

def get_sunday_in_advent(year):
    christmas = datetime.date(year, 12, 25)
    offset = datetime.timedelta(days = christmas.isoweekday())
    sundays = [christmas - offset - datetime.timedelta(weeks=week) for week in xrange(4)]
    sundays.sort()
    return sundays

if __name__ == '__main__': main()

