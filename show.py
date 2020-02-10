import glob
import time
import sys
import os

class Show:
  arguments = sys.argv
  delay = 0.07

  def __init__(self):
    if len(self.arguments) == 1:
      return

    self.set_delay()

  def set_delay(self):
    for argument in self.arguments:
      if argument == 's':
        self.delay = float(self.arguments[self.arguments.index(argument) + 1])

  def clear_screen(self):
    print("\033[H\033[J")

  def show(self):
    file_count = sum([len(files) for r, d, files in os.walk('frames')])
    while True:
      files = glob.glob('frames/*')
      files.sort(key = lambda x: float(x.strip('frames/output')))

      for f in files:
        with open(f, 'r') as content:
          self.clear_screen()
          print(content.read())
        if file_count == 1:
          return
        time.sleep(self.delay)

if __name__ == '__main__':
  show = Show()
  show.show()