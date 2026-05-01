import cv2
import numpy as np
from typing import List, Tuple

class PreprocessingAgent:
    """
    Toplanan ham kaplumbağa görsellerini yapay zeka modelinin (ResNet50 vb.) 
    anlayabileceği standart boyutlara ve RGB formatına getiren ajandır.
    """
    
    def __init__(self, target_size: Tuple[int, int] = (224, 224)):
        # Modelin beklediği boyutu dışarıdan parametre olarak alıyoruz.
        self.target_size = target_size

    def process_images(self, image_paths: List[str]) -> List[np.ndarray]:
        """
        Görsel yollarını okur, boyutlandırır ve işlenmiş numpy dizileri döner.
        """
        processed_images = []
        
        for path in image_paths:
            # Resmi OpenCV ile oku (OpenCV varsayılan olarak BGR formatında okur)
            img = cv2.imread(path)
            
            if img is None:
                print(f"Uyarı: {path} dosyası okunamadı veya bozuk, atlanıyor.")
                continue
                
            # OpenCV'nin BGR formatını, standart olan RGB formatına çevir
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Resmi hedeflenen boyuta (örn: 224x224) yeniden boyutlandır
            img_resized = cv2.resize(img_rgb, self.target_size)
            
            processed_images.append(img_resized)
            
        print(f"PreprocessingAgent: Toplam {len(processed_images)} görsel {self.target_size} boyutunda işlendi.")
        
        return processed_images

# Açık/Kapalı Prensibi (Open/Closed Principle - OCP): Dikkat edersen sınıfın __init__ metodunda target_size=(224, 224) parametresini tanımladık. Eğer ileride farklı bir yüz tanıma modeli (örneğin InceptionV3, ki 299x299 piksel bekler) kullanmak istersek, sınıfın içindeki kodu değiştirmek (modify) zorunda kalmayacağız. Sınıfı çağırırken sadece yeni bir parametre vererek kodumuzu genişletmiş (extend) olacağız. Bu, SOLID'in 'O' harfinin harika bir örneğidir.

# Bağımlılıkların İzole Edilmesi: OpenCV (cv2) gibi dış kütüphane bağımlılıklarını sadece bu ajana hapsettik. Veri toplayan veya raporlayan ajanlar görüntü işlemenin nasıl yapıldığını bilmek zorunda değil.   