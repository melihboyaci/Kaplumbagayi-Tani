from agents.data_collection import DataCollectionAgent
from agents.preprocessing import PreprocessingAgent
from agents.recognition import RecognitionAgent
from agents.evaluation import EvaluationAgent
from agents.reporting import ReportingAgent

class Orchestrator:
    """
    Tüm ajanları yöneten, veri akışını sağlayan ve sistemi 
    adım adım çalıştıran Yönetici (Coordinator) Sınıftır.
    """
    def __init__(self):
        print("Orchestrator: Sistem başlatılıyor. Ajanlar göreve hazırlanıyor...\n")
        # Ajanları ayağa kaldırıyoruz
        self.data_agent = DataCollectionAgent(data_dir="data")
        self.prep_agent = PreprocessingAgent()
        self.recog_agent = RecognitionAgent()
        self.eval_agent = EvaluationAgent(similarity_threshold=0.60)    
        self.reporting_agent = ReportingAgent()
        
    def run_pipeline(self):
        print("--- KAPLUMBAĞA YÜZ TANIMA SÜRECİ BAŞLADI ---\n")
        
        # ADIM 1: Veri Toplama
        image_paths = self.data_agent.gather_turtle_images()
        if len(image_paths) < 2:
            print("Orchestrator: Karşılaştırma yapmak için 'data' klasöründe en az 2 resim olmalı!")
            return

        # ADIM 2: Görüntü Ön İşleme
        processed_imgs = self.prep_agent.process_images(image_paths)

        # ADIM 3: Özellik Çıkarımı (Yüz Tanıma)
        features = self.recog_agent.extract_features(processed_imgs)

        # ADIM 4 & 5: Değerlendirme ve Raporlama
        if len(features) >= 2:
            print("\n--- DEĞERLENDİRME AŞAMASI ---")
            is_match, similarity_score = self.eval_agent.compare_turtles(features[0], features[1])
            
            # Sonucu rapora yazdırıyoruz
            self.reporting_agent.log_evaluation_result(
                image1_path=image_paths[0], 
                image2_path=image_paths[1], 
                is_match=is_match, 
                similarity=similarity_score
            )
            
            # Günlük log örneği (Bunu her günün sonunda bir kere çalışacak şekilde koddan çağırabilirsin)
            self.reporting_agent.log_daily_progress(
                day=1,
                actions="Data, Preprocessing, Recognition, Evaluation ve Reporting ajanları kodlandı. Orkestratör mimarisi kuruldu.",
                results="ResNet50 modeli kullanılarak Cosine Similarity hesabı yapıldı ve %60 doğruluk eşiği belirlendi.",
                issues="Henüz gerçek veri ile test edilmedi.",
                improvements="Sistem tamamen modüler hale getirildi ve SOLID prensiplerine uygun tasarlandı."
            )

        print("\n--- SÜREÇ TAMAMLANDI ---")

if __name__ == "__main__":
    system = Orchestrator()
    system.run_pipeline()

# Ödevinde "Clean Code" kısmını açıklarken şu detayı verebilirsin:
# "Eğer PreprocessingAgent, işlediği resmi doğrudan kendi içinde RecognitionAgent'a gönderseydi, kodlar birbirine yapışık (tightly coupled) olurdu. 
# Orkestratör sayesinde her ajan sadece kendi işini yapıyor, girdi alıyor ve çıktı veriyor. 
# Yarın kaplumbağa yerine insan yüzü tanımak istersek, ajanların içini değil, sadece Orkestratör'ün akışını değiştirmemiz yeterli olacak."