from functools import wraps
import time
from typing import Set

def timer(func):
    """Fonksiyonun çalışma süresini ölçer ve konsola yazar."""
    @wraps(func)
    def wrapper(*args,**kwargs):
        t0 = time.perf_counter() # Başlangıç zamanı
        result = func(*args,**kwargs)
        total_time = time.perf_counter()-t0
        print(f"[{func.__name__}] Çalışma Süresi: {total_time:.4f} saniye")
        return result
    return wrapper


def required_column(requireds: Set[str]):
    """Gelen kayıt listesinin (List[dict]) gerekli sütunları içerdiğini kontrol eden dekoratör."""
    def deco(func):
        @wraps(func)
        def wrapper(rows, *args,**kwargs):
            if not rows:
                # Veri seti boşsa, şema kontrolü yapılamaz
                raise ValueError("Boş veri seti veya dosya okunamadı.")
            
            # Düzeltme: Sütun isimlerini almak için .keys() metodu kullanılmalıdır.
            try:
                keys = set(rows[0].keys())
            except (IndexError, AttributeError):
                raise ValueError("Veri yapısı geçersiz. Sütun başlıkları bulunamadı.")
                
            missing = requireds - keys
            
            if missing:
                # Eksik zorunlu sütunlar varsa hata fırlat
                raise ValueError(f"Eksik zorunlu sütunlar: {', '.join(missing)}. Gerekli: {', '.join(requireds)}")
                
            return func(rows,*args,**kwargs)
        return wrapper
    return deco
