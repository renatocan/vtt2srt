#!/usr/bin/env python3

import io
import sys
import re

if len(sys.argv) < 2:
    print('Use {} <vtt file>'.format(sys.argv[0]))
    sys.exit()

filename = sys.argv[1]
vtt_text = ''

try:
    with io.open(filename, 'r') as f:
        vtt_text = f.read()
except:
    print('Could not open {}'.format(filename))
    sys.exit()

if len(vtt_text) == 0:
    print('File is empty')
    sys.exit()

vtt_text = re.sub(r'(\d\d:\d\d:\d\d).(\d\d\d) --> (\d\d:\d\d:\d\d).(\d\d\d)',
                  r'\1,\2 --> \3,\4', vtt_text)
vtt_list = vtt_text.split('\n')
srt_list = []
counter = 1
beginning = True

for n, line in enumerate(vtt_list):
    time_match = re.search(r'\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d',
                           line)
    if not time_match:
        if not beginning:
            srt_list.append(line)
    else:
        beginning = False
        srt_list.append(str(counter))
        counter = counter + 1
        srt_list.append(line)

srt_text = '\n'.join(srt_list)
srtfilename = filename + '.srt'
with open(srtfilename, 'w') as f:
    f.write(srt_text)
