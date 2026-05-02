import os
import glob
from typing import List
from agents import BaseAgent

class DataCollectionAgent(BaseAgent):
    """
    Kaplumbağa görsellerini belirtilen veri kaynağından (klasörden) 
    toplamakla görevli ajandır.
    """
    
    def __init__(self, data_dir: str):
        super().__init__()
        self.data_dir = data_dir

    def run(self, input_data: str = None):
        result = self.gather_turtle_images()
        self.log(f"{len(result)} adet görsel toplandı.")
        return result

    def validate_input(self, input_data) -> bool:
        return os.path.exists(self.data_dir)

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

# Single Responsibility Principle (Tek Sorumluluk Prensibi): Bu sınıf sadece ve sadece dosya okuma ve yol bulma işi yapıyor. Görüntüyü kırpmıyor, yapay zeka modeline sokmuyor.  

# Tip Belirtme (Type Hinting): -> List[str] gibi ifadeler kullanarak kodun ne döndüreceğini net bir şekilde belirttik. Bu, takım çalışmasında ve AI asistanların kodu okumasında büyük kolaylık sağlar.

# Hata Yönetimi (Error Handling): Klasörün olmaması veya içinin boş olması gibi durumlar için basit ama etkili kontroller (If/Else) ekledik.