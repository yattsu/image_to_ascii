from image import ImageConverter
import sys

class Ascii:
  arguments = sys.argv
  source_path = False
  options = {'scale': 100, 'reverse': False}

  def __init__(self):
    if len(self.arguments) == 1:
      return

    self.set_source()
    self.set_options()

  def set_source(self):
    self.source_path = self.arguments[1]

  def set_options(self):
    for argument in self.arguments:
      if argument == 'scale':
        self.options[argument] = int(self.arguments[self.arguments.index(argument) + 1])

      if argument == 'reverse':
        self.options[argument] = True

  def convert(self):
    image = ImageConverter(self.source_path, self.options)
    image.convert_image()


if __name__ == '__main__':
  ascii = Ascii()
  ascii.convert()