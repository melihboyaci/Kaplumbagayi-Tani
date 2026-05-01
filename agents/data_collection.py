import os
import glob
from typing import List

class DataCollectionAgent:
    """
    Kaplumbağa görsellerini belirtilen veri kaynağından (klasörden) 
    toplamakla görevli ajandır.
    """
    
    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def gather_turtle_images(self) -> List[str]:
        """
        Belirtilen klasördeki görsellerin tam dosya yollarını bir liste olarak döner.
        """
        if not os.path.exists(self.data_dir):
            print(f"Hata: {self.data_dir} adında bir klasör bulunamadı!")
            return []

        # Desteklenen görsel formatları
        extensions = ('*.jpg', '*.jpeg', '*.png')
        image_paths = []
        
        for ext in extensions:
            search_pattern = os.path.join(self.data_dir, ext)
            image_paths.extend(glob.glob(search_pattern))
            
        if not image_paths:
            print(f"Uyarı: {self.data_dir} klasöründe kaplumbağa görseli bulunamadı.")
        else:
            print(f"DataCollectionAgent: Toplam {len(image_paths)} adet görsel başarıyla toplandı.")
            
        return image_paths