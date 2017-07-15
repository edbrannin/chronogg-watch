import sys
import os
import json

import json_delta
# import pushbullet_cli
# import requests

CACHE_DIR="cache"

def read_cache(name):
    with open(os.path.join(CACHE_DIR, name)) as in_file:
        return json.load(in_file)

new, old = read_cache('result.json'), read_cache('result-old.json')
if new == old:
    sys.exit(0)

diff = json_delta.diff(new, old, minimal=True, verbose=False)

udiff = json_delta.udiff(new, old, patch=diff, indent=2)

for line in udiff:
    print line

if udiff:
    sys.exit(1)
else:
    sys.exit(0)
