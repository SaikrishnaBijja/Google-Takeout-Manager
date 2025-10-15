from datetime import datetime
from pathlib import Path
import re
import json
from typing import Optional

# Try multiple parsing strategies for creation timestamp

def parse_filename_date(fname: str, json_sidecar_folder: Path = None) -> Optional[datetime]:
    base = Path(fname).stem

    # 1) If a JSON sidecar exists with same base name, try to read photoTakenTime.formatted
    if json_sidecar_folder:
        candidate = json_sidecar_folder / (base + '.json')
        if candidate.exists():
            try:
                with open(candidate, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                formatted = data.get('photoTakenTime', {}).get('formatted')
                if formatted:
                    # Google format usually like: "January 1, 2020, 12:34:56 UTC"
                    formatted = formatted.replace('UTC', '').strip()
                    try:
                        return datetime.strptime(formatted, '%B %d, %Y, %H:%M:%S')
                    except Exception:
                        try:
                            return datetime.fromisoformat(formatted)
                        except Exception:
                            pass
            except Exception:
                pass

    s = base

    # 2) ISO-like segments or YYYY_MM_DD
    m = re.search(r'(\d{4})[-_](\d{2})[-_](\d{2})[T_ ]?(\d{2})?(?::|-)?(\d{2})?(?::|-)?(\d{2})?', s)
    if m:
        year = int(m.group(1))
        month = int(m.group(2))
        day = int(m.group(3))
        hour = int(m.group(4) or 0)
        minute = int(m.group(5) or 0)
        second = int(m.group(6) or 0)
        return datetime(year, month, day, hour, minute, second)

    # 3) Google style segments with month name: Img_01_Jan_2020_... or Video_...
    m2 = re.search(r'([0-3]?\d)_([A-Za-z]{3,9})_(\d{4})[_-]?(\d{2})?[_-]?(\d{2})?', s)
    if m2:
        day = int(m2.group(1))
        month_str = m2.group(2)
        year = int(m2.group(3))
        try:
            month = datetime.strptime(month_str[:3], '%b').month
            hour = int(m2.group(4) or 0)
            minute = int(m2.group(5) or 0)
            return datetime(year, month, day, hour, minute, 0)
        except Exception:
            pass

    return None

