import os
from PIL import Image
from agents import BaseAgent


class AuditAgent(BaseAgent):
    """
    Kullanıcıdan gelen görselin pipeline'a girmeden önce
    doğrulanmasından sorumlu ajandır.
    SOLID - SRP: Sadece girdi doğrulama işi yapar.
    """

    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
    MAX_FILE_SIZE_MB = 10
    MIN_IMAGE_SIZE_PX = 100

    def run(self, input_data: str) -> dict:
        """
        Görsel dosyasını tüm kontrollerden geçirir.
        Döner:
          - passed: bool
          - message: str  (Türkçe açıklama)
        """
        checks = (
            self._check_extension,
            self._check_file_size,
            self._check_image_readable,
            self._check_image_dimensions,
        )
        for check in checks:
            passed, message = check(input_data)
            if not passed:
                self.log(f"Doğrulama başarısız: {message}")
                return {"passed": False, "message": message}

        self.log("Görsel doğrulama başarılı.")
        return {"passed": True, "message": "Görsel doğrulama başarılı."}

    def validate_input(self, input_data) -> bool:
        """Girdi string mi kontrolü."""
        return isinstance(input_data, str)

    def _check_extension(self, file_path: str) -> tuple:
        """
        Dosya uzantısı ALLOWED_EXTENSIONS içinde mi?
        Döner: (passed: bool, message: str)
        """
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            allowed = ", ".join(sorted(self.ALLOWED_EXTENSIONS))
            return False, f"Desteklenmeyen uzantı '{ext}'. İzin verilenler: {allowed}."
        return True, "Uzantı geçerli."

    def _check_file_size(self, file_path: str) -> tuple:
        """
        Dosya boyutu MAX_FILE_SIZE_MB altında mı?
        Döner: (passed: bool, message: str)
        """
        if not os.path.exists(file_path):
            return False, f"Dosya bulunamadı: {file_path}"
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if size_mb > self.MAX_FILE_SIZE_MB:
            return False, f"Dosya çok büyük ({size_mb:.2f} MB). Maksimum {self.MAX_FILE_SIZE_MB} MB olmalı."
        return True, "Dosya boyutu uygun."

    def _check_image_readable(self, file_path: str) -> tuple:
        """
        Pillow ile açılabiliyor mu? (bozuk dosya kontrolü)
        Döner: (passed: bool, message: str)
        """
        try:
            with Image.open(file_path) as img:
                img.verify()
        except Exception as e:
            return False, f"Görsel okunamadı veya bozuk: {e}"
        return True, "Görsel okunabilir."

    def _check_image_dimensions(self, file_path: str) -> tuple:
        """
        Görsel en az MIN_IMAGE_SIZE_PX x MIN_IMAGE_SIZE_PX mi?
        Döner: (passed: bool, message: str)
        """
        with Image.open(file_path) as img:
            width, height = img.size
        if width < self.MIN_IMAGE_SIZE_PX or height < self.MIN_IMAGE_SIZE_PX:
            return False, (
                f"Görsel çok küçük ({width}x{height}). "
                f"Minimum {self.MIN_IMAGE_SIZE_PX}x{self.MIN_IMAGE_SIZE_PX} piksel olmalı."
            )
        return True, "Görsel boyutları uygun."
