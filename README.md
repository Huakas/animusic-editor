# Animusic-Editor
Animusic-Editor is planned to be a graphical user interface that allows you to easily create animated music videos with beautiful audio-reactive visual effects. In it's final form it is supposed to be an editor for Animusic where you can easily create your own music videos with applying different effects to different videos or images that can be imported, moved on the canvas and configured to suit your needs.

## Features
* Uses [**librosa**](https://librosa.org/) to filter and process the audio in order to translate the beats and sounds into visual effect intensity.
* Uses different effects for different frequencies to create more dynamic and responsive animations.
* Can animate both images and videos.
* Supports all major image, video, and audio formats.
* Easy tweaking possible - create your own custom animated music video with custom effects to make the video yours.

## Showcase
**Note:** You may need to unmute the videos in order to hear the audio.

https://user-images.githubusercontent.com/1664699/156676898-90b04c29-b27a-413e-a678-5aef7daa5546.mp4

https://user-images.githubusercontent.com/1664699/117237477-0fe41580-adf9-11eb-834f-7ed80f4f703c.mp4

https://user-images.githubusercontent.com/1664699/156676750-2ec8a965-e857-4de1-a92f-25ebc3c8e345.mp4

## Requirements
This package requires [**ffmpeg**](https://www.ffmpeg.org/) to be installed in order to work.

### Linux
```sudo apt install ffmpeg```

### macOS
```brew install ffmpeg```

### Windows
A Windows binary of **ffmpeg** is already included with this package for convenience, so there is no need for you to install it.

## Installation
Clone the repository onto your local machine:
`git clone https://github.com/Huakas/animusic-editor.git`
Create a Python virtual environment:
`cd animusic-editor`
`python -m venv venv`
Activate Python virtual environment:
`source venv/bin/activate` (Linux)
`venv\Scripts\activate.bat` (Windows)
Install required Python packages:
`pip install -r requirements.txt`

## Usage
With activated Python virtual environment, run:
`python start.py`
