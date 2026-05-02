import cv2
import numpy as np
from typing import List, Tuple

class PreprocessingAgent:
    """
    Kaplumbağa görsellerini standart boyutlara (RGB) getirir ve 
    arka plan gürültüsünü azaltmak için merkeze odaklanan (Center Crop) 
    bir yüz kırpma işlemi uygular.
    """
    
    def __init__(self, target_size: Tuple[int, int] = (224, 224), crop_ratio: float = 0.8):
        self.target_size = target_size
        self.crop_ratio = crop_ratio # Resmin yüzde kaçlık merkez kısmını alacağımız (Day 2 güncellemesi)

    def process_images(self, image_paths: List[str]) -> List[np.ndarray]:
        processed_images = []
        
        for path in image_paths:
            img = cv2.imread(path)
            
            if img is None:
                print(f"Uyarı: {path} dosyası okunamadı, atlanıyor.")
                continue
                
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # --- DAY 2 İYİLEŞTİRMESİ: Center Crop (Merkezden Kırpma) ---
            # Arka planı azaltıp kaplumbağanın yüzüne odaklanmak için
            height, width = img_rgb.shape[:2]
            
            # Kırpılacak alanın sınırlarını belirliyoruz
            new_width = int(width * self.crop_ratio)
            new_height = int(height * self.crop_ratio)
            
            left = (width - new_width) // 2
            top = (height - new_height) // 2
            right = (width + new_width) // 2
            bottom = (height + new_height) // 2
            
            # Resmi merkezden kırpıyoruz
            img_cropped = img_rgb[top:bottom, left:right]
            # -----------------------------------------------------------
            
            # Kırpılmış resmi modelin istediği 224x224 boyutuna getir
            img_resized = cv2.resize(img_cropped, self.target_size)
            
            processed_images.append(img_resized)
            
        print(f"PreprocessingAgent: {len(processed_images)} görsel kırpılarak {self.target_size} boyutunda işlendi.")
        return processed_images

# Açık/Kapalı Prensibi (Open/Closed Principle - OCP): Dikkat edersen sınıfın __init__ metodunda target_size=(224, 224) parametresini tanımladık. Eğer ileride farklı bir yüz tanıma modeli (örneğin InceptionV3, ki 299x299 piksel bekler) kullanmak istersek, sınıfın içindeki kodu değiştirmek (modify) zorunda kalmayacağız. Sınıfı çağırırken sadece yeni bir parametre vererek kodumuzu genişletmiş (extend) olacağız. Bu, SOLID'in 'O' harfinin harika bir örneğidir.

# Bağımlılıkların İzole Edilmesi: OpenCV (cv2) gibi dış kütüphane bağımlılıklarını sadece bu ajana hapsettik. Veri toplayan veya raporlayan ajanlar görüntü işlemenin nasıl yapıldığını bilmek zorunda değil.   