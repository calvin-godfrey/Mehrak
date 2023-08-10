#!/usr/bin/env python
# Import default python modules.
import time
import sys
import threading

# Import third-party Python modules which must be installed.
from sshkeyboard import listen_keyboard
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

# Read in the images from the command line arguments.
# sys.argv[0] always contains the name of the program,
# so the file names start with sys.argv[1]. This program
# assumes that the files exist and will crash if they do not.
if len(sys.argv) < 7:
    sys.exit("Expecting 4 images and 1 gif (last)")
else:
    image_file1 = sys.argv[1]
    image_file2 = sys.argv[2]
    image_file3 = sys.argv[3]
    image_file4 = sys.argv[4]
    gif_file = sys.argv[5]

# Read the images at the provided paths.
image1 = Image.open(image_file1)
image2 = Image.open(image_file2)
image3 = Image.open(image_file3)
image4 = Image.open(image_file4)
images = [image1, image2, image3, image4]
gif = Image.open(gif_file)
image_count = len(images)
image_index = 0

# Verify that the final provided image path is a gif.
try:
    num_frames = gif.n_frames
except Exception:
    sys.exit("The last file provided is not a gif")

# Configure the options for the RGB Matrix board.
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.gpio_slowdown = 4
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
matrix = RGBMatrix(options = options)

# Preprocess the gif by loading each frame into memory.
gif_frames = []
for frame_index in range(0, num_frames):
    gif.seek(frame_index)
    frame = gif.copy()
    frame.thumbnail((matrix.width, matrix.height), Image.NEAREST)
    canvas = matrix.CreateFrameCanvas()
    canvas.SetImage(frame.convert("RGB"))
    gif_frames.append(canvas)
gif.close()

# A function that is called when any key is pressed.
# The 'key' parameter will take on the character that has been pressed.
# This code uses 'a' and 'b' to swap between static images, and any
# other character to play or pause the gif.
def keys(key):
    global image_index
    global image_count

    if key == 'a':
        # Find the next valid image index to display.
        image_index = 0 if image_index == -1 else image_index
        image_index = (image_index + 1) % image_count
    elif key == 'b':
        # Find the previous valid image index to display.
        image_index = 0 if image_index == -1 else image_index
        image_index = (image_index + image_count - 1) % image_count
    else:
        # Either play the gif (if it is not being played)
        # or pause the gif (if it is already being played).
        if image_index == -1:
            image_index = -2
        else:
            image_index = -1

# A function that draws one of several images to the RGB matrix.
def draw():
    global image_index
    global images
    global gif_frames
    global num_frames
    frame_index = 0
    # This function runs infinitely.
    while True:
        # Since there are two things happening simultaneously
        # (reading user input and drawing to the RGB matrix)
        # it is necessary to make a copy of which image to draw
        # so that its value does not change while this function runs.
        local_index = image_index
        print(local_index)
        # A value of -2 indicates that the gif is being paused; do nothing.
        if local_index == -2:
            time.sleep(0.05)
            continue
        # A value of -1 indicates that the gif is being played.
        # Select the appropriate frame of the gif to displa.
        elif local_index == -1:
            matrix.SwapOnVSync(gif_frames[frame_index])
            frame_index += 1
            if frame_index == num_frames:
                frame_index = 0
        else:
            # Any other value indicates that the static image with the
            # corresponding index is being displayed. 
            frame_index = 0
            matrix.SetImage(images[local_index].convert('RGB'), unsafe = False)
        # This value determines how long between each frame when the gif
        # is played.
        time.sleep(0.3)

# Start a thread that repeatedly draws to the RGB matrix.
draw_thread = threading.Thread(target=draw)
draw_thread.start()

# A function that sets up a listener for keys being pressed.
def poll():
    listen_keyboard(
        on_press=keys,
        debug=True
    )

# Start a thread that listens for keys being pressed.
poll_thread = threading.Thread(target=poll)
poll_thread.start()

# Wait forever. If this main thread exists, all other threads will
# be killed and the program will exit immediately.
while True:
    continue
