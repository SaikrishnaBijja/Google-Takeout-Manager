import hashlib
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def remove_duplicates(folder: Path, media_exts=None):
    if media_exts is None:
        media_exts = None
    hashes = {}
    deleted = 0
    for f in folder.iterdir():
        if f.is_file():
            if media_exts and f.suffix.lower() not in media_exts:
                continue
            try:
                h = file_hash(f)
                if h in hashes:
                    logger.info('Deleting duplicate %s', f)
                    f.unlink()
                    deleted += 1
                else:
                    hashes[h] = f
            except Exception:
                logger.exception('Error hashing %s', f)
    logger.info('Deleted %d duplicates', deleted)


def file_hash(path: Path, chunk_size=8192):
    import hashlib
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        while True:
            b = fh.read(chunk_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()