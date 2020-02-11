from PIL import Image
import requests
import glob
import os
import io

class ImageConverter:
  source_path = False
  options = False
  last_saved = 0

  def __init__(self, source_path, options):
    self.source_path = source_path
    self.options = options
    self.delete_frames()

  def delete_frames(self):
    files = glob.glob('frames/*')
    for f in files:
      os.remove(f)

  def is_link(self):
    if 'http' == self.source_path[0:4].lower():
      return True

    return False

  def image_type(self):
    extension = self.source_path[-4:].lower()
    type = extension.strip('.')

    return type

  def get_image(self):
    if self.is_link():
      r = requests.get(self.source_path)
      image = Image.open(io.BytesIO(r.content))
    else:
      image = Image.open(self.source_path)

    return image

  def process_image(self):
    image = self.get_image()
    image_type = self.image_type()
    scale = self.options['scale']

    frames = []
    if image_type == 'gif':
      for frame in range(image.n_frames - 1):
        image.seek(image.tell() + 1)
        frames.append(image.resize((int((scale / 100) * image.size[0]), int((scale / 100) * image.size[1]))))
    else:
      frames.append(image.resize((int((scale / 100) * image.size[0]), int((scale / 100) * image.size[1]))))

    return frames

  def convert_image(self):
    frames = self.process_image()
    specter = ' .:;+=xX$&'
    wide = self.options['wide']

    chars = self.options['chars']
    if chars != False:
      specter = chars

    if self.options['contrast'] == True:
      specter = ' ░▒▓█'

    if self.options['reverse'] == True:
      specter = specter[::-1]

    for image in frames:
      os.system('clear')
      print('Converting ' + str(len(frames)) + ' frames...')
      print(str(frames.index(image) + 1) + '/' + str(len(frames)))

      image = image.convert('RGB')
      string = ''
      width, height = image.size
      last_row = 0
      contrast_levels = []
      contrast_gap = 255 / len(specter)
      for gap in range(len(specter)):
        contrast_levels.append(contrast_gap * gap)

      for y in range(height):
        for x in range(width):
          if y != last_row:
            string += '\n'
            last_row += 1
          try:
            r, g, b = image.getpixel((x, y))
          except:
            r, g, b, a = image.getpixel((x, y))
          pixel_value = (r * 0.3 + g * 0.59 + b * 0.11)
          levels = []
          for level in contrast_levels:
            levels.append(abs(pixel_value - level))
          character = specter[levels.index(min(levels))] * wide
          string += character

      if self.options['rotate'] != False:
        orientation = 1 if self.options['rotate'] == 'left' else -1
        rotated = zip(*string.split('\n')[::orientation])
        string = []
        for row in rotated:
          string.append(''.join(list(row)))

        string = '\n'.join(string)

      self.save_image(string)

  def save_image(self, string):
    path = 'frames/output' + str(self.last_saved)
    with open(path, 'w') as f:
      f.write(string)

    self.last_saved += 1