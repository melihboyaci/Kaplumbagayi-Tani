import os
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

class ReportingAgent:
    """
    Sistemin sonuçlarını LLM (Büyük Dil Modeli) kullanarak analiz eden 
    ve bir araştırmacı diliyle Markdown (.md) raporu üreten zeki ajandır.
    """
    def __init__(self, log_file: str = "gelisim_raporu.md"):  
        load_dotenv()
        self.log_file = log_file
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY ortam değişkeni bulunamadı.")
            
        genai.configure(api_key=self.api_key)
        
        # Raporlamak için kullanacağımız AI modeli (En güncel stabil sürüm)
        self.model = genai.GenerativeModel('gemini-flash-latest')
        
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", encoding="utf-8") as f:
                f.write("# Kaplumbağa Yüz Tanıma Projesi - Gelişim Raporu\n\n")
                f.write("> Bu dosya AI destekli ReportingAgent tarafından oluşturulmaktadır.\n\n")
                f.write("---\n\n")

    def log_evaluation_result(self, image1_path: str, image2_path: str, is_match: bool, similarity: float):
        """Test sonuçlarını rapora ekler."""
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"### Test Sonucu ({datetime.now().strftime('%H:%M:%S')})\n")
            f.write(f"- **Görsel 1:** `{os.path.basename(image1_path)}`\n")
            f.write(f"- **Görsel 2:** `{os.path.basename(image2_path)}`\n")
            f.write(f"- **Benzerlik Skoru:** %{similarity * 100:.2f}\n")
            f.write(f"- **Karar:** {'✅ EŞLEŞTİ' if is_match else '❌ EŞLEŞMEDİ'}\n\n")

    def generate_ai_daily_log(self, day: int, similarity_score: float, is_match: bool):
        """
        Günün sonuçlarını alarak LLM'e gönderir ve araştırmacı dilinde
        ödev formatına uygun bir günlük değerlendirme raporu yazdırır.
        """
        print("ReportingAgent: Yapay zeka günün verilerini analiz edip raporu yazıyor...")
        
        # LLM'i yönlendirdiğimiz sistem komutu (Prompt)
        prompt = f"""
        Sen kıdemli bir yapay zeka araştırmacısısın. Kaplumbağa yüz tanıma projesinde çalışıyorsun.
        Bugün Day {day}. Sistem, ResNet50 modeli ve Cosine Similarity kullanarak iki kaplumbağa 
        fotoğrafını karşılaştırdı. Hedef doğruluk eşiği %60.
        
        Bugünkü Test Sonucu:
        - Benzerlik: %{similarity_score * 100:.2f}
        - Eşleşme Durumu: {"Başarılı" if is_match else "Başarısız"}
        
        Lütfen aşağıdaki formatta, durumu teknik ama anlaşılır bir dille yorumlayarak bir günlük log yaz:
        
        **Ne yapıldı:** (Kısaca ResNet50 ve Cosine Similarity kullanıldığını belirt)
        **Ne sonuç alındı:** (Skoru yorumla, iyi mi kötü mü, neden böyle çıkmış olabilir?)
        **Hangi problemler çıktı:** (Eğer skor düşükse nedenlerini, yüksekse sistemin nerede zorlanabileceğini yaz)
        **Ne iyileştirildi:** (Gelecek adımlar veya mimarinin modülerliği hakkında bilgi ver)
        """
        
        try:
            # LLM'den yanıtı al
            response = self.model.generate_content(prompt)
            ai_report = response.text
            
            # Üretilen raporu md dosyasına kaydet
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"## Day {day} (AI Analizi)\n\n")
                f.write(ai_report + "\n\n")
                f.write("---\n\n")
                
            print(f"ReportingAgent: Day {day} raporu AI tarafından başarıyla oluşturuldu!")
            
        except Exception as e:
            print(f"ReportingAgent Hata: AI rapor oluşturamadı. Hata detayı: {e}")