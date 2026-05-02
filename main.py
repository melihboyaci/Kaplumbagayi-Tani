import os
from agents.data_collection import DataCollectionAgent
from agents.preprocessing import PreprocessingAgent
from agents.recognition import RecognitionAgent
from agents.evaluation import EvaluationAgent
from agents.reporting import ReportingAgent
from agents.head_detection import HeadDetectionAgent
from agents.audit import AuditAgent

CURRENT_DAY = 3

class Orchestrator:
    """
    Tüm ajanları koordine eden, bilinmeyen bir kaplumbağa görselini alıp 
    veritabanındaki (database) kayıtlı bireylerle karşılaştırarak kimlik 
    tespiti yapan Ana Yönetici (Proje Yöneticisi) sınıfıdır.
    """
    def __init__(self):
        print("Sistem Başlatılıyor: Ajanlar yükleniyor...")
        self.audit_agent = AuditAgent()
        self.head_detection_agent = HeadDetectionAgent()
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

        # 3. Audit (Görsel Doğrulama) Ajanı Devrede
        audit_result = self.audit_agent.run(query_image_path)
        if not audit_result["passed"]:
            print(f"\n❌ Görsel Doğrulama Hatası: {audit_result['message']}")
            return

        # 4. Kafa Tespiti (Head Detection) Ajanı Devrede
        if not self.head_detection_agent.validate_input(query_image_path):
            print("HATA: Geçersiz görsel yolu!")
            return

        head_result = self.head_detection_agent.run(query_image_path)

        if not head_result["head_found"]:
            print(f"\n⚠️  {head_result['message']}")
            print("Lütfen kaplumbağanın kafasının net göründüğü")
            print("bir yan profil fotoğrafı yükleyin.")
            return

        if head_result["confidence"] < HeadDetectionAgent.LOW_CONFIDENCE_THRESHOLD:
            print(f"\n⚠️  Düşük güven skoru: %{head_result['confidence']*100:.0f}")
            print("Devam ediliyor ancak sonuç güvenilir olmayabilir.")

        # Kırpılmış kafa görselini preprocessing'e gönder
        # (dosya yolu yerine artık numpy array kullanacağız)
        query_processed = self.preprocessing_agent.run([head_result["cropped"]])[0]

        # 5. Ön İşleme (Preprocessing) Ajanı — Veritabanı Görselleri
        if not self.preprocessing_agent.validate_input(db_image_paths):
            print("HATA: Preprocessing için geçerli girdi yok!")
            return
        db_processed = self.preprocessing_agent.run(db_image_paths)

        # 6. Derin Öğrenme (Recognition) Ajanı Devrede - Vektörleri Çıkar
        query_processed_list = [query_processed]
        if not self.recognition_agent.validate_input(query_processed_list):
            print("HATA: Recognition için geçerli girdi yok!")
            return
        query_feature = self.recognition_agent.run(query_processed_list)[0]

        if not self.recognition_agent.validate_input(db_processed):
            print("HATA: Recognition için geçerli girdi yok!")
            return
        db_features = self.recognition_agent.run(db_processed)

        # 7. Değerlendirme (Evaluation) Ajanı Devrede - En İyi Eşleşmeyi Bul
        best_match_name = "Bilinmiyor"
        highest_score = 0.0

        for i, db_feature in enumerate(db_features):
            evaluation_input = (query_feature, db_feature)
            if not self.evaluation_agent.validate_input(evaluation_input):
                print("HATA: Evaluation için geçerli girdi yok!")
                return
            _, score = self.evaluation_agent.run(evaluation_input)
            
            # Eğer skor şu ana kadarki en yüksek skorsa, kaydet
            if score > highest_score:
                highest_score = score
                # Dosya adını kaplumbağa ismi olarak alıyoruz (Örn: "riza.jpeg" -> "Riza")
                best_match_name = db_files[i].split('.')[0].capitalize()

        # 8. Karar Aşaması
        is_match = highest_score >= self.evaluation_agent.similarity_threshold
        
        # Eğer benzerlik eşiği geçildiyse ismi ver, geçilmediyse "Yeni Birey" de
        final_identity = best_match_name if is_match else "YENİ BİREY (Sisteme Kayıtlı Değil)"
        
        print("\n--- TESPİT SONUCU ---")
        print(f"Tespit Edilen Kimlik: {final_identity}")
        print(f"Benzerlik Skoru: %{highest_score * 100:.2f}")
        print("---------------------\n")

        # 9. Raporlama (Reporting) Ajanı Devrede
        print("ReportingAgent, sonuçları analiz edip gelisim_raporu.md dosyasına yazıyor...")
        report_input = {
            "day": CURRENT_DAY,
            "similarity_score": highest_score,
            "is_match": is_match
        }
        if not self.reporting_agent.validate_input(report_input):
            print("HATA: Reporting için geçerli girdi yok!")
            return
        self.reporting_agent.run(report_input)

if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run_identification()

# Ödevinde "Clean Code" kısmını açıklarken şu detayı verebilirsin:
# "Eğer PreprocessingAgent, işlediği resmi doğrudan kendi içinde RecognitionAgent'a gönderseydi, kodlar birbirine yapışık (tightly coupled) olurdu. 
# Orkestratör sayesinde her ajan sadece kendi işini yapıyor, girdi alıyor ve çıktı veriyor. 
# Yarın kaplumbağa yerine insan yüzü tanımak istersek, ajanların içini değil, sadece Orkestratör'ün akışını değiştirmemiz yeterli olacak."