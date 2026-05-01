import os
from datetime import datetime

class ReportingAgent:
    """
    Sistemin değerlendirme sonuçlarını ve günlük gelişim loglarını 
    bir Markdown (.md) dosyasına otomatik olarak kaydeden Araştırmacı / Raporlayıcı ajandır.
    """
    def __init__(self, log_file: str = "gelisim_raporu.md"):
        self.log_file = log_file
        
        # Dosya yoksa başlık atarak oluştur
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", encoding="utf-8") as f:
                f.write("# Kaplumbağa Yüz Tanıma Projesi - Gelişim Raporu\n\n")
                f.write("> Bu dosya ReportingAgent tarafından otomatik olarak oluşturulmaktadır.\n\n")
                f.write("---\n\n")

    def log_evaluation_result(self, image1_path: str, image2_path: str, is_match: bool, similarity: float):
        """
        Değerlendirme ajanından gelen test sonuçlarını rapora ekler.
        """
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"### Test Sonucu ({datetime.now().strftime('%H:%M:%S')})\n")
            f.write(f"- **Görsel 1:** `{os.path.basename(image1_path)}`\n")
            f.write(f"- **Görsel 2:** `{os.path.basename(image2_path)}`\n")
            f.write(f"- **Benzerlik Skoru:** %{similarity * 100:.2f}\n")
            f.write(f"- **Karar:** {'✅ EŞLEŞTİ' if is_match else '❌ EŞLEŞMEDİ'}\n\n")
            
        print("ReportingAgent: Değerlendirme sonucu 'gelisim_raporu.md' dosyasına işlendi.")

    def log_daily_progress(self, day: int, actions: str, results: str, issues: str, improvements: str):
        """
        Ödev gereksinimi olan günlük gelişim loglarını formata uygun şekilde yazar.
        """
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"## Day {day}\n\n")
            f.write(f"**Ne yapıldı:**\n{actions}\n\n")
            f.write(f"**Ne sonuç alındı:**\n{results}\n\n")
            f.write(f"**Hangi problemler çıktı:**\n{issues}\n\n")
            f.write(f"**Ne iyileştirildi:**\n{improvements}\n\n")
            f.write("---\n\n")
            
        print(f"ReportingAgent: Gün {day} logu rapora eklendi.")

# Bağımlılıkların Tersine Çevrilmesi (Dependency Inversion) ve SRP: Raporlama işlemini EvaluationAgent'ın içine de yazabilirdik ama bu SRP'yi (Tek Sorumluluk Prensibi) bozardı. Ayrıca yarın .md formatından vazgeçip sonuçları bir veritabanına kaydetmek istersen, sadece ReportingAgent'ı değiştireceksin. Diğer ajanlar bu değişiklikten hiç etkilenmeyecek.