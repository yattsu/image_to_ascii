import glob
import os
import time
import sys

delay = 0.07

if len(sys.argv) > 2:
  if sys.argv[1] == 's':
    delay = float(sys.argv[2])

def show():
  file_count = sum([len(files) for r, d, files in os.walk('frames')])
  while True:
    files = glob.glob('frames/*')
    files.sort(key = lambda x: float(x.strip('frames/output')))

    for f in files:
      with open(f, 'r') as content:
        os.system('clear')
        print(f)
        print(content.read())
      if file_count == 1:
        return
      time.sleep(delay)

show()