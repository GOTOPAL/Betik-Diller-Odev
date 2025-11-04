from .dosya_islemleri import read_csv, write_json, write_text
from .processing import clean_records, stats, build_report
from pathlib import Path 

def main():
    
    PROJECT_DIR = Path(__file__).parent.parent 
    
    DATA_DIR = PROJECT_DIR / "data"

    DATA_DIR.mkdir(exist_ok=True) 

    
    read_csv_path = DATA_DIR / "people.csv"
    write_cleaned_path = DATA_DIR / "cleaned_records.json"  # Temizlenmiş kayıtlar
    write_stats_path = DATA_DIR / "stats_output.json"      # İstatistikler
    write_report_path = DATA_DIR / "summary_report.txt"    # Rapor
    
    print("--- Veri İşleme Başlatıldı ---")
    print(f"Girdi dosyası aranıyor: {read_csv_path}")

    # Artık 'read_csv' fonksiyonuna tam dosya yolunu (str olarak) veriyoruz.
    rows = read_csv(str(read_csv_path))

    if not rows:
        print("İşlenecek veri bulunamadı. Program sonlandırılıyor.")
        return

    # Şema kontrolü ve 3. Kayıtları temizle/dönüştür
    try:
        cleaned_rows = clean_records(rows) 
    except ValueError as e:
        print(f"HATA: Veri Doğrulama Başarısız: {e}")
        return

    print(f"Toplam okunan kayıt: {len(rows)}")
    print(f"Temizlenmiş (Geçerli) kayıt: {len(cleaned_rows)}")
    
    if not cleaned_rows:
        print("Temizleme sonrası geçerli kayıt kalmadı. Program sonlandırılıyor.")
        return

    # İstatistik üret
    st = stats(cleaned_rows)
    print("İstatistikler Başarıyla Üretildi.")
    
    # Çıktıları yaz
    write_json(str(write_cleaned_path), cleaned_rows)
    write_json(str(write_stats_path), st)
    write_text(str(write_report_path), build_report(st))
    
    print(f"-> Çıktı dosyaları '{DATA_DIR.name}' klasörüne yazıldı:")
    print(f"   - {write_cleaned_path.name}")
    print(f"   - {write_stats_path.name}")
    print(f"   - {write_report_path.name}")
    print("\n--- İşlem Tamamlandı ---")

if __name__ == "__main__":
    main()
