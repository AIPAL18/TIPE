# Source - https://superuser.com/a/1410801
# Posted by Eduard Florinescu, modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-14, License - CC BY-SA 4.0

import sys

from Levenshtein import *

txt1 = open("libc.so.5.hex").read()
txt2 = open("libc.so.6.hex").read()

print("distance:", distance(txt1,txt2))
