import sys
from ij import IJ, ImagePlus, ImageStack, WindowManager
from ij.plugin import ImageCalculator
from ij.process import ByteProcessor
from ij.plugin.filter import ParticleAnalyzer
from ij.plugin.filter.ParticleAnalyzer import SHOW_NONE
from ij.measure import ResultsTable

# PARAMETERS
HYST_HI = 17
HYST_LO = 5
DPI = float(1200)
MIN_SIZE = 0.03 * (DPI/25.4)**2
MAX_SIZE = 0.8 * (DPI/25.4)**2
MIN_CIRC = 0.03
MAX_CIRC = 0.9

# COPY OF HYSTERESIS TO AVOID DEALING WITH WINDOWS
def hyst(ima, T1, T2):
    la = ima.getWidth()
    ha = ima.getHeight()
    res = ByteProcessor(la, ha)
    for x in xrange(la):
        for y in xrange(ha):
            pix = ima.getPixelValue(x, y)
            if pix >= T1:
                res.putPixel(x, y, 255)
            elif pix >= T2:
                res.putPixel(x, y, 128)
    change = True
    while (change):
        change = False
        for x in xrange(1, la-1):
            for y in xrange(1, ha-1):
                if (res.getPixelValue(x, y) == 255):
                    if (res.getPixelValue(x + 1, y) == 128):
                        change = True
                        res.putPixelValue(x + 1, y, 255)
                    if (res.getPixelValue(x - 1, y) == 128):
                        change = True
                        res.putPixelValue(x - 1, y, 255)
                    if (res.getPixelValue(x, y + 1) == 128):
                        change = True
                        res.putPixelValue(x, y + 1, 255)
                    if (res.getPixelValue(x, y - 1) == 128):
                        change = True
                        res.putPixelValue(x, y - 1, 255)
                    if (res.getPixelValue(x + 1, y + 1) == 128):
                        change = True
                        res.putPixelValue(x + 1, y + 1, 255)
                    if (res.getPixelValue(x - 1, y - 1) == 128):
                        change = True
                        res.putPixelValue(x - 1, y - 1, 255)
                    if (res.getPixelValue(x - 1, y + 1) == 128):
                        change = True
                        res.putPixelValue(x - 1, y + 1, 255)
                    if (res.getPixelValue(x + 1, y - 1) == 128):
                        change = True
                        res.putPixelValue(x + 1, y - 1, 255)
        if (change):
            for x in xrange(la-2, 0, -1):
                for y in xrange(ha-2, 0, -1):
                    if (res.getPixelValue(x, y) == 255):
                        if (res.getPixelValue(x + 1, y) == 128):
                            change = True
                            res.putPixelValue(x + 1, y, 255)
                        if (res.getPixelValue(x - 1, y) == 128):
                            change = True
                            res.putPixelValue(x - 1, y, 255)
                        if (res.getPixelValue(x, y + 1) == 128):
                            change = True
                            res.putPixelValue(x, y + 1, 255)
                        if (res.getPixelValue(x, y - 1) == 128):
                            change = True
                            res.putPixelValue(x, y - 1, 255)
                        if (res.getPixelValue(x + 1, y + 1) == 128):
                            change = True
                            res.putPixelValue(x + 1, y + 1, 255)
                        if (res.getPixelValue(x - 1, y - 1) == 128):
                            change = True
                            res.putPixelValue(x - 1, y - 1, 255)
                        if (res.getPixelValue(x - 1, y + 1) == 128):
                            change = True
                            res.putPixelValue(x - 1, y + 1, 255)
                        if (res.getPixelValue(x + 1, y - 1) == 128):
                            change = True
                            res.putPixelValue(x + 1, y - 1, 255)
    for x in xrange(la):
        for y in xrange(ha):
            if (res.getPixelValue(x, y) == 128):
                res.putPixelValue(x, y, 0)
    return res

# ACTUAL SCRIPT
imp1 = IJ.openImage(sys.argv[1])
imp2 = IJ.openImage(sys.argv[2])
# stabilize
stack = ImageStack(imp1.width, imp1.height)
stack.addSlice('', imp1.getProcessor())
stack.addSlice('', imp2.getProcessor())
stackimp = ImagePlus('stack', stack)
WindowManager.setTempCurrentImage(stackimp)
IJ.run(stackimp, "Image Stabilizer", "transformation=Affine maximum_pyramid_levels=4 template_update_coefficient=0.90 maximum_iterations=20000 error_tolerance=0.0000001")
stack = stackimp.getImageStack()
stabilized1 = ImagePlus('stabilized1', stack.getProcessor(1))
stabilized2 = ImagePlus('stabilized2', stack.getProcessor(2))
# subtract
ic = ImageCalculator()
diff = ic.run('Subtract create', stabilized1, stabilized2)
# smudge
diff.getProcessor().blurGaussian(2)
# enhance ;)
hysteresis = ImagePlus('hysteresis', hyst(diff.getProcessor(), HYST_HI, HYST_LO))
# invert
hysteresis.getProcessor().invert()
# count worms
rt = ResultsTable()
pa = ParticleAnalyzer(SHOW_NONE, 0, rt, MIN_SIZE, MAX_SIZE, MIN_CIRC, MAX_CIRC)
pa.analyze(hysteresis)
sys.stdout.write('%d' % rt.size())
IJ.run('Quit')
