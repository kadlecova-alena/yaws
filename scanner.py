#!/usr/bin/python
import sys, sane
from PIL import Image
from PIL.ImageDraw import Draw

DPI = 1200
MM2PIX = float(DPI)/25.4 
MODE = 'Gray'
DEPTH = 8

DIAMETER = 1420
REGION_WIDTH = 3795
REGION_HEIGHT = DIAMETER
REGIONS = [
    (-45, -90),
    (1155, 600),
    (-45, 1310),
    (1155, 2020),
    (-45, 2730),
    (1155, 3440),
    (-45, 4150),
    (1155, 4860),
    (-45, 5570),
]

CUT_X = 380
CUT_Y = 520

NUM_FRAMES = 3

#sane.init()
#devices = sane.get_devices()
#epsons = [d for d in devices if d[1] == 'Epson']
#if len(epsons) < 1:
#    raise Exception('No supported scanner found.')
#scanner = sane.open(epsons[0][0])
#scanner.resolution = DPI
#scanner.mode = MODE
#scanner.depth = DEPTH

def scan(offset_x, offset_y):
    scanner.tl_x = max(0, offset_x/MM2PIX)
    scanner.tl_y = max(0, offset_y/MM2PIX)
    scanner.br_x = (offset_x+REGION_WIDTH)/MM2PIX
    scanner.br_y = (offset_y+REGION_HEIGHT)/MM2PIX
    scanner.start()
    image = scanner.snap()
    canvas = Image.new(image.mode, (REGION_WIDTH, REGION_HEIGHT))
    canvas.paste(image, (REGION_WIDTH-image.size[0], REGION_HEIGHT-image.size[1]))
    return canvas

def crop_dish(image, offset_x, offset_y):
    image = image.crop((offset_x, offset_y, offset_x+DIAMETER, offset_y+DIAMETER))
    Draw(image).polygon([(0,0),(CUT_X,0),(0,CUT_Y)], fill=1)
    Draw(image).polygon([(DIAMETER,0),(DIAMETER-CUT_X,0),(DIAMETER,CUT_Y)], fill=1)
    Draw(image).polygon([(0,DIAMETER),(CUT_X,DIAMETER),(0,DIAMETER-CUT_Y)], fill=1)
    Draw(image).polygon([(DIAMETER,DIAMETER),(DIAMETER-CUT_X,DIAMETER),(DIAMETER,DIAMETER-CUT_Y)], fill=1)
    return image

with open(sys.argv[1]) as config:
    labels = ''.join(config.readlines()).split()

whole = Image.open('out.tif') #
row = 0
for offset_x, offset_y in REGIONS:
    row += 1
    for frame in range(NUM_FRAMES):
        im = whole.crop((offset_x, offset_y, offset_x + REGION_WIDTH, offset_y + REGION_HEIGHT)) #im = scan_region(offset_x, offset_y)
        # left
        dish = crop_dish(im, 0, 0)
        n = 2*row-2
        dish.save('test_%s.tiff' % labels[n])
        # right
        dish = crop_dish(im, REGION_WIDTH-DIAMETER, 0)
        n = 2*row-1
        dish.save('test_%s.tiff' % labels[n])

