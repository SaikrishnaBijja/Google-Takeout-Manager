import logging
from pathlib import Path
from config import INPUT_FOLDER, ALL_FOLDER, IMAGE_OUTPUT, VIDEO_OUTPUT, ERROR_FOLDER, ALL_FILES, PHOTOS_ZIP_OUTPUT
from extractor import extract_all_from_folder
from organizer import collect_media
from image_handler import process_image
from video_handler import process_video
from dedupe import remove_duplicates
from zip_split import split_into_zips


def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def run_pipeline():
    # 1) Extract any zips in INPUT_FOLDER to ALL_FOLDER
    extract_all_from_folder(Path(INPUT_FOLDER), Path(ALL_FOLDER))

    # 2) Collect media into ALL_FILES (move)
    collect_media(Path(ALL_FOLDER), Path(ALL_FILES))

    # 3) Walk ALL_FILES and add metadata / organize to target folders
    for p in Path(ALL_FILES).iterdir():
        if p.is_file():
            ext = p.suffix.lower()
            if ext in {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.heic', '.heif', '.raw', '.cr2', '.nef', '.orf', '.sr2', '.arw', '.dng'}:
                process_image(p, Path(IMAGE_OUTPUT), Path(ALL_FILES), Path(ERROR_FOLDER))
            elif ext in {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.wmv', '.flv', '.mpeg', '.mpg', '.3gp', '.m4v', '.ts', '.mts', '.m2ts'}:
                process_video(p, Path(VIDEO_OUTPUT), Path(ALL_FILES), Path(ERROR_FOLDER))
            else:
                logging.info('Skipping unsupported: %s', p)

    # 4) Remove duplicates in PHOTO folder
    remove_duplicates(Path(IMAGE_OUTPUT))

    # 5) Split photos into zipped chunks (example max 1.5GB)
    split_into_zips(Path(IMAGE_OUTPUT), Path(PHOTOS_ZIP_OUTPUT), max_size_bytes=1500 * 1024 * 1024)


if __name__ == '__main__':
    setup_logging()
    run_pipeline()