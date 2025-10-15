# Google Takeout Media Manager


A small, modular project to:
- Extract Takeout ZIPs
- Collect media files into a single folder
- Parse metadata (either from filename or JSON sidecars) and write EXIF/creation_time
- Convert unsupported image formats to JPEG and add EXIF
- Add video `creation_time` metadata via FFmpeg (stream-copy)
- Organize media into Photos / Videos / Audios
- Remove duplicates and split large photo folders into ZIP parts


## Requirements
- Python 3.9+
- pip packages: see `requirements.txt`
- FFmpeg installed and on PATH (for video metadata & copy)


## Quick start
1. Create a virtualenv and install requirements:
```bash
python -m venv .venv
.venv\Scripts\activate # Windows
pip install -r requirements.txt
