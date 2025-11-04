from .dekorator import required_column, timer 
from typing import List, Dict, Any, Set
import statistics

# Zorunlu sütun isimleri
REQUIRED_FIELDS: Set[str] = {"name", "age", "city"}

@required_column(REQUIRED_FIELDS)
@timer
def clean_records(rows: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Gelen kayıtları temizler, dönüşümler uygular ve sadece geçerli kayıtları döndürür.
    """
    cleaned_data = []
    
    for row in rows:
        # 1. name ve city değerlerinin başındaki/sonundaki boşlukları temizle (kırp)
        name = row.get("name", "").strip()
        age_str = row.get("age", "").strip()
        city = row.get("city", "").strip()
        
        # 2. age Kontrolü: boş veya sayısal olmayanları kaldır
        if not age_str:
            continue  # age boşsa bu kaydı atla
            
        try:
            # age → int türüne dönüştür
            age = int(age_str)
        except ValueError:
            continue  # age sayısal değilse bu kaydı atla
            
        # 3. Geçerli veriyi kaydet
        cleaned_data.append({
            "name": name,
            "age": age,
            "city": city,
        })
        
    return cleaned_data

@timer
def stats(cleaned_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Temizlenmiş kayıtlar üzerinden istatistikleri hesaplar.
    """
    
    total_count = len(cleaned_rows)
    
    if total_count == 0:
        return {
            "valid_count": 0,
            "average_age": 0.0,
            "count_by_city": {},
        }

    ages = [r["age"] for r in cleaned_rows]
    
    # Ortalama Yaş Hesaplama
    avg_age = statistics.mean(ages) 
    
    # Şehirlere Göre Dağılım
    count_by_city = {}
    for r in cleaned_rows:
        city = r["city"]
        count_by_city[city] = count_by_city.get(city, 0) + 1
        
    return {
        "valid_count": total_count,
        # Ortalama yaşı 2 ondalık basamağa yuvarla
        "average_age": round(avg_age, 2), 
        "count_by_city": count_by_city,
    }

def build_report(st: Dict[str, Any]) -> str:
    """Üretilen istatistiklerden kısa bir rapor metni oluşturur."""
    lines = []
    lines.append("--- Veri Analiz Raporu ---")
    lines.append("")
    lines.append(f"Geçerli Kayıt Sayısı: {st['valid_count']}")
    lines.append(f"Ortalama Yaş: {st['average_age']} yıl")
    lines.append("-" * 25)
    lines.append("Şehirlere Göre Dağılım:")
    
    # Şehir dağılımını (c, n) şeklinde rapora ekle
    sorted_cities = sorted(st["count_by_city"].items(), key=lambda item: item[0])
    
    for city, count in sorted_cities:
        lines.append(f"  - {city}: {count} kişi")
        
    lines.append("-" * 25)
    lines.append("İşlem Başarıyla Tamamlandı.")
    
    return "\n".join(lines)