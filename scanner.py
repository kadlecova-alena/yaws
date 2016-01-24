#!/usr/bin/python
import sys, sane
from PIL import Image
from PIL.ImageDraw import Draw

DPI = 1200
MODE = 'Gray'
DEPTH = 8

REGIONS = [
    (0    , 0     , 158.75, 56.30),
    (48.89, 25.40 , 209.55, 85.51),
    (0    , 55.46 , 158.75, 115.57),
    (48.89, 85.51 , 209.55, 145.62),
    (0    , 115.57, 158.75, 175.68),
    (48.89, 145.62, 209.55, 205.74),
    (0    , 175.68, 158.75, 235.80),
    (48.89, 205.74, 209.55, 265.85),
    (0    , 235.80, 158.75, 295.91),
]
CANVAS_WIDTH  = int(6.325 * DPI)
CANVAS_HEIGHT = int(2.365 * DPI)

CUT_X = 0.268
CUT_Y = 0.366

NUM_TAKES = 3

#sane.init()
#devices = sane.get_devices()
#epsons = [d for d in devices if d[1] == 'Epson']
#if len(epsons) < 1:
#    raise Exception('No supported scanner found.')
#scanner = sane.open(epsons[0][0])
#scanner.resolution = DPI
#scanner.mode = MODE
#scanner.depth = DEPTH

def scan(region):
    scanner.tl_x = region[0]
    scanner.tl_y = region[1]
    scanner.br_x = region[2]
    scanner.br_y = region[3]
    scanner.start()
    image = scanner.snap()
    canvas = Image.new(image.mode, (CANVAS_WIDTH, CANVAS_HEIGHT))
    canvas.paste(image, (CANVAS_WIDTH-image.size[0], CANVAS_HEIGHT-image.size[1]))
    return canvas

def crop_dish(image):
    width, height = image.size
    Draw(image).polygon([(0,0),(int(width*CUT_X),0),(0,int(height*CUT_Y))], fill=1)
    Draw(image).polygon([(width,0),(int(width*(1-CUT_X)),0),(width,int(height*CUT_Y))], fill=1)
    Draw(image).polygon([(0,height),(int(width*CUT_X),height),(0,int(height*(1-CUT_Y)))], fill=1)
    Draw(image).polygon([(width,height),(int(width*(1-CUT_X)),height),(width,int(height*(1-CUT_Y)))], fill=1)
    return image

with open(sys.argv[1]) as config:
    labels = ''.join(config.readlines()).split()

whole = Image.open('sample1200.tif') #
for r, region in enumerate(REGIONS):
    for frame in range(1, NUM_TAKES+1):
        im = whole.crop((int(region[0]*47.2), int(region[1]*47.2), int(region[2]*47.2), int(region[3]*47.2)))
        #im = scan_region(region)
        # left
        dish = im.crop((0,0,im.size[1],im.size[1]))
        dish = crop_dish(dish)
        dish.save('test_%s.tiff' % labels[2*r-2])
        # right
        dish = im.crop((im.size[0]-im.size[1],0,im.size[0],im.size[1]))
        dish = crop_dish(dish)
        dish.save('test_%s.tiff' % labels[2*r-1])

