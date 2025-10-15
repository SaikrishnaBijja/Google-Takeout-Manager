import zipfile
from pathlib import Path


def split_into_zips(source_folder: Path, output_folder: Path, max_size_bytes: int):
    files = []
    for f in source_folder.rglob('*'):
        if f.is_file():
            files.append((f, f.stat().st_size, f.relative_to(source_folder)))

    output_folder.mkdir(parents=True, exist_ok=True)
    part = 1
    current = []
    cur_size = 0

    for f, size, rel in files:
        if cur_size + size > max_size_bytes and current:
            name = output_folder / f'{source_folder.name}_{part}.zip'
            with zipfile.ZipFile(name, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file_path, _, relpath in current:
                    zf.write(file_path, relpath)
            part += 1
            current = []
            cur_size = 0
        current.append((f, size, rel))
        cur_size += size

    if current:
        name = output_folder / f'{source_folder.name}_{part}.zip'
        with zipfile.ZipFile(name, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path, _, relpath in current:
                zf.write(file_path, relpath)