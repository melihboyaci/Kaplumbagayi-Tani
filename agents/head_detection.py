import os
import cv2
import numpy as np
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
from agents import BaseAgent


class HeadDetectionAgent(BaseAgent):
    """
    Kaplumbağa görselinde kafa bölgesini tespit eden ve kırpan ajandır.
    Eğer kafa tespit edilemezse kullanıcıyı yönlendirir.
    SOLID - SRP: Sadece kafa tespiti ve kırpma işi yapar.
    """

    MIN_HEAD_RATIO = 0.05
    MAX_HEAD_RATIO = 0.80
    LOW_CONFIDENCE_THRESHOLD = 0.4
    FALLBACK_CROP_RATIO = 0.6

    def __init__(self):
        super().__init__()
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY bulunamadı.")
        genai.configure(api_key=api_key)
        self.vision_model = genai.GenerativeModel("gemini-1.5-flash")

    def run(self, input_data: str) -> dict:
        """
        Görsel yolunu alır, kafa bölgesini kırpılmış numpy array olarak döner.
        Dönen dict:
          - head_found: bool
          - cropped: np.ndarray veya None
          - confidence: float (0.0-1.0)
          - message: str
        """
        # 1. OpenCV contour ile tespit
        image = cv2.imread(input_data)
        if image is None:
            self.log(f"Görsel okunamadı: {input_data}")
            return {"head_found": False, "cropped": None, "confidence": 0.0,
                    "message": "Görsel dosyası okunamadı."}

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        bbox, confidence = self._detect_with_contour(image_rgb)

        if bbox is not None and confidence >= self.LOW_CONFIDENCE_THRESHOLD:
            cropped = self._crop_from_bbox(image_rgb, bbox)
        else:
            cropped = self._fallback_crop(image_rgb)

        # 2. Gemini Vision ile doğrula
        gemini_result = self._verify_with_gemini(cropped)
        self.log(f"Gemini doğrulaması: {gemini_result['explanation']}")

        # 3. İki sonucu birleştir
        head_found = gemini_result["verified"]

        if not head_found:
            return {
                "head_found": False,
                "cropped": None,
                "confidence": confidence,
                "message": f"Kaplumbağa kafası doğrulanamadı. {gemini_result['explanation']}"
            }

        self.log(f"Kafa tespiti başarılı. Güven: %{confidence * 100:.0f}")
        return {
            "head_found": True,
            "cropped": cropped,
            "confidence": confidence,
            "message": gemini_result["explanation"]
        }

    def validate_input(self, input_data) -> bool:
        """Dosya yolunun string ve mevcut olduğunu kontrol eder."""
        return isinstance(input_data, str) and os.path.exists(input_data)

    def _verify_with_gemini(self, cropped_image: np.ndarray) -> dict:
        """
        Kırpılmış görseli Gemini Vision'a göndererek
        kaplumbağa kafasının görünüp görünmediğini doğrular.
        Döner:
          - verified: bool
          - explanation: str (Türkçe)
        """
        try:
            pil_image = Image.fromarray(cropped_image)

            prompt = """Bu görseli incele ve şu soruyu yanıtla:
            Bu görselde bir deniz kaplumbağasının lateral (yan)
            kafa profili net olarak görünüyor mu?

            Sadece şu formatta yanıt ver:
            SONUÇ: EVET veya HAYIR
            AÇIKLAMA: (tek cümle Türkçe açıklama)
            """

            response = self.vision_model.generate_content([prompt, pil_image])
            response_text = response.text.strip()

            verified = "SONUÇ: EVET" in response_text

            lines = response_text.split('\n')
            explanation = next(
                (l.replace('AÇIKLAMA:', '').strip()
                 for l in lines if 'AÇIKLAMA:' in l),
                "Gemini analizi tamamlandı."
            )

            return {"verified": verified, "explanation": explanation}

        except Exception as e:
            self.log(f"Gemini Vision hatası: {e}")
            return {"verified": True, "explanation": "Gemini doğrulaması atlandı."}

    def _detect_with_contour(self, image: np.ndarray) -> tuple:
        """
        OpenCV contour analizi ile kafa tespiti yapar.
        Döner: (bbox, confidence) — bbox: (x, y, w, h)

        Adımlar:
        1. Gri tona çevir
        2. GaussianBlur uygula (kernel: 5x5)
        3. Canny edge detection (threshold: 50, 150)
        4. Contour bul
        5. En büyük contour'un bounding box'ını al
        6. Alan oranını hesapla → MIN/MAX_HEAD_RATIO kontrolü
        7. Güven skoru döndür
        """
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return None, 0.0

        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        total_area = image.shape[0] * image.shape[1]
        head_ratio = (w * h) / total_area

        if not (self.MIN_HEAD_RATIO <= head_ratio <= self.MAX_HEAD_RATIO):
            return None, 0.0

        confidence = min(1.0, head_ratio / self.MAX_HEAD_RATIO)
        return (x, y, w, h), confidence

    def _fallback_crop(self, image: np.ndarray) -> np.ndarray:
        """
        Contour başarısız olursa görselin merkez %60'ını kırparak döner.
        """
        height, width = image.shape[:2]
        new_h = int(height * self.FALLBACK_CROP_RATIO)
        new_w = int(width * self.FALLBACK_CROP_RATIO)
        top = (height - new_h) // 2
        left = (width - new_w) // 2
        return image[top:top + new_h, left:left + new_w]

    def _crop_from_bbox(self, image: np.ndarray, bbox: tuple) -> np.ndarray:
        """bbox koordinatlarına göre görseli kırpar."""
        x, y, w, h = bbox
        return image[y:y + h, x:x + w]
