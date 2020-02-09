import sys
import os
import glob
import requests
import io
from PIL import Image

specter = ['  ', '::', 'cc', 'oo', '@@']
# specter = list(' .\'`^",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$')

def is_link():
  if 'http' in sys.argv[1]:
    return True

  return False

def is_gif():
  if '.gif' in sys.argv[1]:
    return True

  return False

def get_image():
  if len(sys.argv) == 1:
    return False

  image_path = sys.argv[1]
  if is_link():
    r = requests.get(image_path)
    image_path = r.content
    image = Image.open(io.BytesIO(image_path))
  else:
    if not os.path.exists(image_path):
      return False
    image = Image.open(image_path)

  resize_value = 100
  if len(sys.argv) >= 3:
    resize_value = int(sys.argv[2])

  if len(sys.argv) == 4:
    if sys.argv[3] == 'reverse':
      global specter
      specter = specter[::-1]

  frames = []
  if is_gif():
    for frame in range(0, image.n_frames - 1):
      image.seek(image.tell() + 1)
      frames.append(image.resize((int((resize_value / 100) * image.size[0]), int((resize_value / 100) * image.size[1]))))
  else:
    frames.append(image.resize((int((resize_value / 100) * image.size[0]), int((resize_value / 100) * image.size[1]))))

  return frames

def ascii():
  frames = get_image()
  output_counter = 0
  output_files = glob.glob('frames/*')
  for f in output_files:
    os.remove(f)
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
        character = specter[levels.index(min(levels))]
        string += character

    with open('frames/output' + str(output_counter), 'w') as f:
      f.write(string)

    output_counter += 1

ascii()