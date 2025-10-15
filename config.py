from pathlib import Path


# Edit these to match your system
BASE = Path(r"Provide Base Path")
INPUT_FOLDER = BASE / 'Final' # initial input folder (or where you copy files to process)
ALL_FOLDER = BASE / 'All' # extracted takeout contents
IMAGE_OUTPUT = BASE / 'Images'
VIDEO_OUTPUT = BASE / 'Videos'
PHOTOS_FOLDER = BASE / 'Photos'
AUDIOS_FOLDER = BASE / 'Audios'
ERROR_FOLDER = BASE / 'Error'
ALL_FILES = BASE / 'All Files'
PHOTOS_ZIP_OUTPUT = BASE / 'Photos Zip'


for p in [IMAGE_OUTPUT, VIDEO_OUTPUT, PHOTOS_FOLDER, AUDIOS_FOLDER, ERROR_FOLDER, ALL_FILES, PHOTOS_ZIP_OUTPUT]:
    p.mkdir(parents=True, exist_ok=True)