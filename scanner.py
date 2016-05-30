#!/usr/bin/python
import sys, sane
from PIL import Image
from PIL.ImageDraw import Draw
import datetime
import time

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

INTERVAL = 60

sane.init()
devices = sane.get_devices()
scanners = [d for d in devices if d[2] == sys.argv[1]]
if len(scanners) < 1:
    raise Exception('Scanner %s not found. Available: %s' % (sys.argv[1], ', '.join([d[2] for d in devices])))
scanner = sane.open(scanners[0][0])
scanner.resolution = DPI
scanner.mode = MODE
scanner.depth = DEPTH

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

out_dir = sys.argv[2]

with open(out_dir + '/config.csv') as labels_file:
    labels = ''.join(labels_file.readlines()).split()

today = datetime.datetime.now().isoformat()[:10]

im=scan((0, 0, 209.55, 295.91)) # wake-up call :)
im.save('%s/whole_%s.tiff' % (out_dir, today))

last_scan_time = None
for r, region in enumerate(REGIONS):
    for take in range(1, NUM_TAKES+1):
        if last_scan_time:
            elapsed = time.time() - last_scan_time
            time.sleep(max(0, INTERVAL - elapsed))
        last_scan_time = time.time()
        im = scan(region)
        # left
        dish = im.crop((0,0,im.size[1],im.size[1]))
        dish = crop_dish(dish)
        dish.save('%s/%s_%s_%d.tiff' % (out_dir, labels[2*r], today, take))
        # right
        dish = im.crop((im.size[0]-im.size[1],0,im.size[0],im.size[1]))
        dish = crop_dish(dish)
        dish.save('%s/%s_%s_%d.tiff' % (out_dir, labels[2*r+1], today, take))

