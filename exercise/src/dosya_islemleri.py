from pathlib import Path
from .dekorator import timer
import csv
import json
from typing import List, Dict, Any

@timer
def read_csv(path: str) -> List[Dict[str, str]]:
    """
    Belirtilen yoldan CSV dosyasını okur ve kayıtları sözlük listesi olarak döndürür.
    """
    try:
        # csv.DictReader sütun başlıklarını otomatik olarak alır.
        with Path(path).open("r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"HATA: Dosya bulunamadı: {path}")
        return []
    except Exception as e:
        print(f"HATA: CSV okuma hatası: {e}")
        return []

@timer
def write_json(path: str, obj: Dict[str, Any] | List[Dict[str, Any]]) -> None:
    """Belirtilen sözlük veya listeyi JSON dosyasına yazar."""
    try:
        # ensure_ascii=False Türkçe karakterleri korur, indent=4 okunabilirlik sağlar.
        with Path(path).open("w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"HATA: JSON yazma hatası: {e}")

@timer
def write_text(path: str, text: str) -> None:
    """Belirtilen metni TXT dosyasına yazar."""
    try:
        Path(path).write_text(text, encoding="utf-8")
    except Exception as e:
        print(f"HATA: TXT yazma hatası: {e}")
