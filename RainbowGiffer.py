import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageSequence
from PIL import Image
from PIL import GifImagePlugin


def color_fade(color1, color2, mix = 0):
    color1 = np.array(mpl.colors.to_rgb(color1))
    color2 = np.array(mpl.colors.to_rgb(color2))
    return mpl.colors.to_hex((1-mix)*color1 + mix*color2)


original_gif = Image.open(os.path.expanduser(filepath))
frames = [frame.copy().convert("RGBA") for frame in ImageSequence.Iterator(original_gif)]
mode = "foreground"
default_frame_count = 50

if len(frames) > 1:
    frame_count = len(frames)
else:
    frame_count = default_frame_count

repetitions = 5

color_list = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#8B00FF', '#FF0000']

color_density = 100

fades = []
for i in range(0, len(color_list)-1):
    c1 = color_list[i]
    c2 = color_list[i+1]

    for x in range(0, color_density):
        fades.append(color_fade(c1, c2, (x/color_density)))

indices = np.round(np.linspace(0, len(fades) - 1, frame_count / repetitions)).astype(int)

frame_colors = []
for i in range(0, repetitions):
    frame_colors.extend([fades[idx] for idx in indices])


frames_out = []
for i in range(0, frame_count):
    if len(frames) > 1:
        this_image = frames[i]
    else:
        this_image = frames[0]

    w, h = this_image.size
    color_image = Image.new("RGBA", (w, h), color=frame_colors[i])

    if mode == "foreground":
        merged_image = Image.blend(this_image, color_image, 0.5)

        pixels = merged_image.load()
        alpha_1 = this_image.split()[-1]
        for x in range(0, w):
            for y in range(0, h):
                if alpha_1.getpixel((x, y)) == 0:
                    pixels[x, y] = (230, 230, 230, 0)

    elif mode == "background":
        merged_image = Image.alpha_composite(color_image, this_image)

    frames_out.append(merged_image)

if mode == "foreground":
    frames_out[0].save('rainbow_foreground.gif', 'gif', save_all=True, append_images=frames_out[1:], duration=40, transparency=0, disposal=2, loop=0)
elif mode == "background":
    frames_out[0].save('rainbow_background.gif', 'gif', save_all=True, append_images=frames_out[1:], duration=40, loop=0)
