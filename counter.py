#!/usr/bin/python
import sys, os, datetime
from subprocess import check_output

FIJI=['/home/alena/bin/Fiji.app/ImageJ-linux64', '--headless', './fiji_macro.py']

exp_dir = sys.argv[1]
with open('%s/config.csv' % exp_dir) as labels_file:
    labels = ''.join(labels_file.readlines()).split()
timestamps = set()
for filename in os.listdir(exp_dir):
    if not filename.endswith('.tiff'):
        continue
    try:
        timestamp = filename.split('_')[1]
    except:
        continue
    timestamps.add(timestamp)
timestamps = sorted(timestamps)

with open('%s/results.csv' % exp_dir, mode='a') as results:
    results.write(' ')
    for label in labels:
        results.write('\t')
        results.write(label)
    results.write('\n')

first = None
for timestamp in timestamps:
    dt = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
    if not first:
        first = dt
    hours = round((dt - first).total_seconds() / 3600)
    with open('%s/results.csv' % exp_dir, mode='a') as results:
        results.write('%d' % hours)
        for label in labels:
            results.write('\t')
            take_1 = '%s/%s_%s_1.tiff' % (exp_dir, label, timestamp)
            take_2 = '%s/%s_%s_2.tiff' % (exp_dir, label, timestamp)
            result = check_output(FIJI + [take_1, take_2])
            results.write(result)
        results.write('\n')

