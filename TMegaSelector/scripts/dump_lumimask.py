#!/usr/bin/env python
'''

Complements extract_meta_info.py

Reads a JSON file from stdin, extracts ['lumi_mask'], and dumps it to stdout

'''

import json
import sys

info = json.load(sys.stdin)
sys.stdout.write(json.dumps(info['lumi_mask']) + '\n')
