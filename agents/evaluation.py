import numpy as np
from scipy.spatial.distance import cosine
from typing import Tuple
from agents import BaseAgent

class EvaluationAgent(BaseAgent):
    """
    RecognitionAgent tarafından çıkarılan özellik vektörlerini karşılaştırarak 
    kaplumbağaların aynı olup olmadığını değerlendirir.
    """
    
    def __init__(self, similarity_threshold: float = 0.60):
        super().__init__()
        # Ödevdeki %60 doğruluk/benzerlik hedefini eşik değeri olarak belirliyoruz.
        self.similarity_threshold = similarity_threshold

    def run(self, input_data: tuple):
        feature1, feature2 = input_data
        is_match, similarity = self.compare_turtles(feature1, feature2)
        self.log(f"Karşılaştırma tamamlandı. Eşleşme: {is_match}, Benzerlik: {similarity:.4f}")
        return is_match, similarity

    def validate_input(self, input_data) -> bool:
        return isinstance(input_data, tuple) and len(input_data) == 2

    def compare_turtles(self, feature1: np.ndarray, feature2: np.ndarray) -> Tuple[bool, float]:
        """
        İki vektör arasındaki Kosinüs Benzerliğini (Cosine Similarity) hesaplar.
        """
        # Scipy 'cosine' fonksiyonu uzaklığı (distance) verir. 
        # Benzerlik = 1 - uzaklık
        distance = cosine(feature1, feature2)
        similarity = 1 - distance
        
        # Benzerlik eşik değerimizi geçiyorsa "Aynı kaplumbağa" diyoruz.
        is_match = similarity >= self.similarity_threshold
        
        result_text = "EŞLEŞTİ" if is_match else "EŞLEŞMEDİ"
        print(f"EvaluationAgent: Benzerlik oranı %{similarity*100:.2f} -> Sonuç: {result_text}")
        
        return is_match, similarity

# Bu ajanda da scipy kütüphanesindeki karmaşık matematiksel hesaplamaları tek bir metodun içine hapsettik. Değerlendirme eşiğini (similarity_threshold = 0.60) dışarıdan parametrik olarak vererek sınıfı esnek hale getirdik.