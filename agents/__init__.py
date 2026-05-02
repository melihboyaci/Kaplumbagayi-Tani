from abc import ABC, abstractmethod
from datetime import datetime
import os

class BaseAgent(ABC):
    """
    Tüm ajanların miras aldığı temel abstract sınıf.
    SOLID - Dependency Inversion Principle (DIP) gereği,
    Orchestrator somut sınıflara değil bu soyut yapıya bağımlıdır.
    """

    LOG_FILE = "gelisim_raporu.md"
    LOG_DIR = "logs"

    def __init__(self):
        os.makedirs(self.LOG_DIR, exist_ok=True)

    @property
    def agent_name(self) -> str:
        """Ajan adını otomatik döner."""
        return self.__class__.__name__

    @abstractmethod
    def run(self, input_data):
        """Her ajanın implement etmesi zorunlu ana metod."""
        pass

    @abstractmethod
    def validate_input(self, input_data) -> bool:
        """Her ajanın implement etmesi zorunlu doğrulama metodu."""
        pass

    def log(self, message: str) -> None:
        """
        logs/daily_report.md dosyasına timestamp ile log yazar.
        Format: [2026-05-02 10:30:00] [AjanAdı] mesaj
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{self.agent_name}] {message}\n"
        log_path = os.path.join(self.LOG_DIR, "daily_report.md")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(log_entry.strip())
