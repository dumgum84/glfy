GLFY Tool

GLFY is a versatile tool for converting videos, images, and live streams into ASCII art. It supports video conversion, live video capture, virtual camera streaming, and screen capturing. GLFY is designed for efficiency and customization, making it ideal for artistic and fun applications.

Features

- Video to ASCII Art: Convert video files into ASCII art video files.
- Image to ASCII Art: Convert image files into ASCII art images.
- Live Video to ASCII Art: Capture live video from your webcam and display it as ASCII art.
- Virtual Camera Support: Stream ASCII art to a virtual camera for use in video applications.
- Screen Capture: Stream your screen as ASCII art in real-time.
- Customizable Parameters: Adjust brightness, contrast, vibrancy, gamma, and more.

# Installation

Install GLFY directly from PyPI:

pip install glfy

GLFY can be used from the command line or within a Python script.

Command Line Usage

- Convert an image to ASCII art:
  glfy image path/to/image.jpg

- Convert a video to ASCII art:
  glfy video path/to/video.mp4

- Start live video ASCII conversion:
  glfy live

- Start live video conversion from the screen:
  glfy live -src scr

# Python Script Usage

You can use GLFY’s CLI from within a Python script using the subprocess module:

import subprocess

Convert an image to ASCII art using the CLI
subprocess.run(['glfy', 'image', 'path/to/image.jpg'])

Convert a video to ASCII art using the CLI
subprocess.run(['glfy', 'video', 'path/to/video.mp4'])

Start live video ASCII conversion using the CLI
subprocess.run(['glfy', 'live'])

# Customizable Parameters

GLFY allows you to adjust various parameters to customize the ASCII art output:

- Brightness, Contrast, and Vibrancy Adjustments: Modify the appearance of the ASCII art.
- Gamma Correction: Fine-tune the brightness of the ASCII output.
- Background Manipulation: Adjust background vibrancy, brightness, and blur.
- ASCII Character Set: Use different ASCII characters for varied artistic effects.
- Virtual Camera Settings: Set resolution and frame rate for virtual camera streaming.

License

This project is licensed under the MIT License.

Enjoy creating ASCII art with GLFY!