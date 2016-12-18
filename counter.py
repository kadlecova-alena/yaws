#!/usr/bin/python
import sys, datetime
from itertools import combinations
from subprocess import check_output

FIJI=['/home/alena/bin/Fiji.app/ImageJ-linux64', '--headless', './fiji_macro.py']
NUM_TAKES = 3

exp_dir = sys.argv[1]
with open('%s/config.csv' % exp_dir) as labels_file:
    labels = ''.join(labels_file.readlines()).split()
first = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
last = datetime.datetime.strptime(sys.argv[3], "%Y-%m-%d").date()

sys.stdout.write(' ')
for label in labels:
    sys.stdout.write('\t')
    for take_a, take_b in combinations(range(1, NUM_TAKES+1),2):
        sys.stdout.write('\t%s(%s) & %s(%s)' % (label, take_a, label, take_b))
sys.stdout.write('\n')
sys.stdout.flush()

for i in range(int((last-first).days)+1):
    day = (first+datetime.timedelta(i)).strftime("%Y-%m-%d")
    sys.stdout.write(day)
    for label in labels:
        sys.stdout.write('\t')
        for take_a, take_b in combinations(range(1, NUM_TAKES+1),2):
            file_a = '%s/%s_%s_%d.tiff' % (exp_dir, label, day, take_a)
            file_b = '%s/%s_%s_%d.tiff' % (exp_dir, label, day, take_b)
	    result = check_output(FIJI + [file_a, file_b])
	    sys.stdout.write('\t%s' % result)
            sys.stdout.flush()
    sys.stdout.write('\n')

