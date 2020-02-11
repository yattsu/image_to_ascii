from image import ImageConverter
import sys

class Ascii:
  arguments = sys.argv
  source_path = False
  options = {'scale': 100, 'reverse': False, 'chars': False, 'wide': 2, 'rotate': False, 'contrast': False}

  def __init__(self):
    if len(self.arguments) == 1:
      return

    self.set_source()
    self.set_options()

  def set_source(self):
    self.source_path = self.arguments[1]

  def set_options(self):
    for argument in self.arguments:
      value = False
      if self.arguments.index(argument) < len(self.arguments) - 1:
        value = self.arguments[self.arguments.index(argument) + 1]

      if argument == 'scale':
        self.options[argument] = int(value)

      if argument == 'reverse':
        self.options[argument] = True

      if argument == 'chars':
        self.options[argument] = value

      if argument == 'wide':
        value = int(value)
        if value >= 1:
          self.options[argument] = value

      if argument == 'rotate':
        self.options['wide'] = 1
        if value == 'left':
          self.options[argument] = 'left'
        elif value == 'right':
          self.options[argument] = 'right'

      if argument == 'contrast':
        self.options[argument] = True

  def convert(self):
    image = ImageConverter(self.source_path, self.options)
    image.convert_image()


if __name__ == '__main__':
  ascii = Ascii()
  ascii.convert()