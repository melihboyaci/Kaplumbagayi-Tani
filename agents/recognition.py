import numpy as np
from typing import List

# TensorFlow ve Keras kütüphanelerini içe aktarıyoruz
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input

class RecognitionAgent:
    """
    Ön işlenmiş kaplumbağa görsellerini alır ve önceden eğitilmiş bir 
    derin öğrenme modeli (ResNet50) kullanarak her görsel için 
    benzersiz bir sayısal özet (embedding/vektör) çıkarır.
    """
    def __init__(self):
        print("RecognitionAgent: ResNet50 modeli yükleniyor. Bu biraz sürebilir...")
        
        # include_top=False: Sınıflandırma (classification) katmanını çöpe atıyoruz.
        # Çünkü amacımız 1000 nesne arasından tahmin yapmak değil, sadece özellikleri almak.
        # pooling='avg': Çıkan karmaşık özellikleri tek boyutlu düz bir listeye (vektör) çevirir.
        self.model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
        
        print("RecognitionAgent: Model başarıyla yüklendi!")

    def extract_features(self, processed_images: List[np.ndarray]) -> List[np.ndarray]:
        """
        Görselleri modele sokar ve embedding (vektör) listesi döner.
        """
        features_list = []
        
        if not processed_images:
            print("Uyarı: Çıkarım yapılacak görsel bulunamadı.")
            return features_list

        for img in processed_images:
            # Keras modeli görüntüleri "batch" (grup) halinde bekler. 
            # Elimizde tek bir resim bile olsa şeklini (1, 224, 224, 3) formatına getirmeliyiz.
            img_batch = np.expand_dims(img, axis=0)
            
            # ResNet50'nin kendisine has bir renk standardı vardır, ona uygun hale getiriyoruz.
            img_preprocessed = preprocess_input(img_batch)
            
            # Modelden vektörü al (Özellik çıkarımı yap)
            feature_vector = self.model.predict(img_preprocessed, verbose=0)
            
            # Bulunan vektörü listeye ekle
            features_list.append(feature_vector[0])
            
        print(f"RecognitionAgent: {len(features_list)} görsel için sayısal özet (vektör) çıkarıldı.")
        
        return features_list

# Encapsulation (Kapsülleme): TensorFlow'un karmaşık tüm detayları (model yükleme, numpy boyutlandırma işlemleri vb.) bu sınıfın içine gizlendi. Ana kodumuz (main.py) TensorFlow'dan haberdar bile olmayacak. Sadece "Al sana resim, bana sayısal özet ver" diyecek. Bu sayede kodumuz çok temiz kalıyor.