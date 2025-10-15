
from pathlib import Path
import subprocess
from datetime import datetime
from parser import parse_filename_date
from .utils import move_to_error
import logging

logger = logging.getLogger(__name__)


def process_video(src: Path, out_dir: Path, json_folder: Path, error_folder: Path):
    dt = parse_filename_date(src.name, json_sidecar_folder=json_folder)
    if dt is None:
        logger.error('Could not parse date for video %s', src)
        move_to_error(src, error_folder)
        return

    iso = dt.isoformat(timespec='seconds')
    out_path = out_dir / src.name

    cmd = [
        'ffmpeg', '-y', '-i', str(src), '-metadata', f'creation_time={iso}', '-c', 'copy', str(out_path)
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info('Wrote creation_time to %s', out_path)
    except subprocess.CalledProcessError as e:
        logger.error('FFmpeg error for %s: %s', src, e)
        move_to_error(src, error_folder)