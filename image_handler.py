
## File: `image_handler.py`

import piexif
from PIL import Image
from pathlib import Path
import rawpy
import imageio
from utils import move_to_error
from parser import parse_filename_date
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

SUPPORTED_NO_EXIF = {'.png', '.gif', '.bmp', '.webp'}


def write_exif_datetime(img_path: Path, dt: datetime, out_path: Path):
    # dt -> EXIF string
    exif_str = dt.strftime('%Y:%m:%d %H:%M:%S')
    exif_bytes = None

    try:
        img = Image.open(img_path)
    except Exception as e:
        raise

    try:
        if img.info.get('exif'):
            exif_dict = piexif.load(img.info.get('exif'))
        else:
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = exif_str
        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = exif_str
        exif_dict['0th'][piexif.ImageIFD.DateTime] = exif_str

        exif_bytes = piexif.dump(exif_dict)

        # Ensure RGB for saving as JPEG
        if img.mode != 'RGB':
            img = img.convert('RGB')

        img.save(out_path, format='JPEG', quality=95, subsampling=0, exif=exif_bytes)
    finally:
        try:
            img.close()
        except Exception:
            pass


def process_image(src: Path, out_dir: Path, json_folder: Path, error_folder: Path):
    ext = src.suffix.lower()
    try:
        # 1) get datetime
        dt = parse_filename_date(src.name, json_sidecar_folder=json_folder)
        if dt is None:
            logger.error('Could not parse date for %s', src)
            move_to_error(src, error_folder)
            return

        # 2) if RAW DNG: convert to JPG first
        if ext == '.dng':
            with rawpy.imread(str(src)) as raw:
                rgb = raw.postprocess()
            out_path = out_dir / (src.stem + '.jpg')
            imageio.imsave(str(out_path), rgb)
            write_exif_datetime(out_path, dt, out_path)
            logger.info('Converted DNG and wrote EXIF: %s', out_path)
            return

        # 3) if format without EXIF, convert to JPG and write EXIF
        if ext in SUPPORTED_NO_EXIF:
            out_path = out_dir / (src.stem + '.jpg')
            write_exif_datetime(src, dt, out_path)
            logger.info('Converted %s to JPG and wrote EXIF to %s', src.name, out_path)
            return

        # 4) JPEG or other EXIF-capable images
        out_path = out_dir / src.name
        write_exif_datetime(src, dt, out_path)
        logger.info('Wrote EXIF to %s', out_path)
    except Exception as e:
        logger.exception('Image processing failed for %s', src)
        move_to_error(src, error_folder)
