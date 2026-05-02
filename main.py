import os
from agents.data_collection import DataCollectionAgent
from agents.preprocessing import PreprocessingAgent
from agents.recognition import RecognitionAgent
from agents.evaluation import EvaluationAgent
from agents.reporting import ReportingAgent

class Orchestrator:
    """
    Tüm ajanları koordine eden, bilinmeyen bir kaplumbağa görselini alıp 
    veritabanındaki (database) kayıtlı bireylerle karşılaştırarak kimlik 
    tespiti yapan Ana Yönetici (Proje Yöneticisi) sınıfıdır.
    """
    def __init__(self):
        print("Sistem Başlatılıyor: Ajanlar yükleniyor...")
        self.preprocessing_agent = PreprocessingAgent()
        self.recognition_agent = RecognitionAgent()
        self.evaluation_agent = EvaluationAgent(similarity_threshold=0.60) # %60 eşik değeri
        self.reporting_agent = ReportingAgent()
        
        # Yeni Klasör Yollarımız
        self.database_dir = "data/database"
        self.query_dir = "data/query"

    def run_identification(self):
        print("\n--- KAPLUMBAĞA KİMLİK TESPİT SİSTEMİ (1-to-N) ---")
        
        # 1. Sorgulanan (Bilinmeyen) Görseli Al
        query_files = [f for f in os.listdir(self.query_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.JPG'))]
        if not query_files:
            print("HATA: data/query/ klasöründe aranacak kaplumbağa bulunamadı!")
            return
            
        query_image_path = os.path.join(self.query_dir, query_files[0])
        print(f"\nSorgulanan Görsel: {query_files[0]}")

        # 2. Veritabanındaki (Bilinen) Kaplumbağaları Al
        db_files = [f for f in os.listdir(self.database_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.JPG'))]
        if not db_files:
            print("HATA: data/database/ klasöründe kayıtlı kaplumbağa yok!")
            return

        db_image_paths = [os.path.join(self.database_dir, f) for f in db_files]
        print(f"Veritabanı Taranıyor: {len(db_files)} kayıtlı birey bulundu.")

        # 3. Ön İşleme (Preprocessing) Ajanı Devrede
        # Day 2'deki Merkez Kırpma algoritmamız burada çalışacak
        query_processed = self.preprocessing_agent.process_images([query_image_path])[0]
        db_processed = self.preprocessing_agent.process_images(db_image_paths)

        # 4. Derin Öğrenme (Recognition) Ajanı Devrede - Vektörleri Çıkar
        query_feature = self.recognition_agent.extract_features([query_processed])[0]
        db_features = self.recognition_agent.extract_features(db_processed)

        # 5. Değerlendirme (Evaluation) Ajanı Devrede - En İyi Eşleşmeyi Bul
        best_match_name = "Bilinmiyor"
        highest_score = 0.0

        for i, db_feature in enumerate(db_features):
            _, score = self.evaluation_agent.compare_turtles(query_feature, db_feature)
            
            # Eğer skor şu ana kadarki en yüksek skorsa, kaydet
            if score > highest_score:
                highest_score = score
                # Dosya adını kaplumbağa ismi olarak alıyoruz (Örn: "riza.jpeg" -> "Riza")
                best_match_name = db_files[i].split('.')[0].capitalize()

        # 6. Karar Aşaması
        is_match = highest_score >= self.evaluation_agent.similarity_threshold
        
        # Eğer benzerlik eşiği geçildiyse ismi ver, geçilmediyse "Yeni Birey" de
        final_identity = best_match_name if is_match else "YENİ BİREY (Sisteme Kayıtlı Değil)"
        
        print("\n--- TESPİT SONUCU ---")
        print(f"Tespit Edilen Kimlik: {final_identity}")
        print(f"Benzerlik Skoru: %{highest_score * 100:.2f}")
        print("---------------------\n")

        # 7. Raporlama (Reporting) Ajanı Devrede
        # Day 2 olarak AI raporumuzu oluşturuyoruz
        print("ReportingAgent, sonuçları analiz edip gelisim_raporu.md dosyasına yazıyor...")
        self.reporting_agent.generate_ai_daily_log(
            day=2,
            similarity_score=highest_score,
            is_match=is_match
        )

if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run_identification()

# Ödevinde "Clean Code" kısmını açıklarken şu detayı verebilirsin:
# "Eğer PreprocessingAgent, işlediği resmi doğrudan kendi içinde RecognitionAgent'a gönderseydi, kodlar birbirine yapışık (tightly coupled) olurdu. 
# Orkestratör sayesinde her ajan sadece kendi işini yapıyor, girdi alıyor ve çıktı veriyor. 
# Yarın kaplumbağa yerine insan yüzü tanımak istersek, ajanların içini değil, sadece Orkestratör'ün akışını değiştirmemiz yeterli olacak."