from pathlib import Path
import shutil

IMG_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.heic', '.heif', '.raw', '.cr2', '.nef', '.orf', '.sr2', '.arw', '.dng'}
VID_EXT = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.wmv', '.flv', '.mpeg', '.mpg', '.3gp', '.m4v', '.ts', '.mts', '.m2ts'}
AUD_EXT = {'.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma', '.m4a', '.alac', '.aiff', '.opus'}


def collect_media(src_root: Path, all_files_folder: Path):
    all_files_folder.mkdir(parents=True, exist_ok=True)
    for p in src_root.rglob('*'):
        if p.is_file():
            if p.suffix.lower() in IMG_EXT.union(VID_EXT).union(AUD_EXT):
                dst = all_files_folder / p.name
                if not dst.exists():
                    shutil.move(str(p), str(dst))