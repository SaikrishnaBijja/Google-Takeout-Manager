import shutil
from pathlib import Path
import logging
import time

logger = logging.getLogger(__name__)

def move_to_error(src: Path, error_folder: Path):
    dest = error_folder / src.name
    try:
        shutil.copy2(src, dest)
        logger.warning('Moved problematic file to error: %s', src)
    except PermissionError:
        logger.warning('PermissionError copying %s — retrying', src)
        time.sleep(1)
        try:
            shutil.copy2(src, dest)
        except Exception as e:
            logger.error('Failed to move %s to error after retry: %s', src, e)