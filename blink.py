#!/usr/bin/python
import sys, sane

DPI = 300
MODE = 'Gray'
DEPTH = 8

sane.init()
devices = sane.get_devices()
scanner_id = int(sys.argv[1])
if scanner_id >= len(devices):
    raise Exception('Invalid device id, only %d devices available.' % len(devices))
scanner = sane.open(devices[scanner_id][0])

scanner.resolution = DPI
scanner.mode = MODE
scanner.depth = DEPTH
scanner.tl_x = 0
scanner.tl_y = 0
scanner.br_x = 209.55
scanner.br_y = 295.91
scanner.start()
scanner.snap()


