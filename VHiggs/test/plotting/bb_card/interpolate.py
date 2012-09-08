#!/usr/bin/env python

import os

for i in range(110, 135):
    if i % 5 == 0:
        continue

    os.system('python scaleCards.py --xsbr --ddir . %i' % i)
