import zipfile
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def extract_all_from_folder(zip_folder: Path, dest_root: Path):
    for z in zip_folder.iterdir():
        if z.suffix.lower() == '.zip':
            out = dest_root / z.stem
            out.mkdir(parents=True, exist_ok=True)
            try:
                with zipfile.ZipFile(z, 'r') as zf:
                    zf.extractall(out)
                logger.info('Extracted %s -> %s', z, out)
            except Exception:
                logger.exception('Failed to extract %s', z)