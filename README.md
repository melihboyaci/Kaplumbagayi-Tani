# 🐢 Kaplumbağa Tanıma Sistemi

## 📖 Proje Hakkında

Yazılım Mühendisliği dersi kapsamında geliştirilen bu sistem, deniz kaplumbağalarını **post-oküler scut** (göz çevresi pul) desenleri üzerinden bireysel olarak tanımlar. Geleneksel etiket yöntemlerine (flipper tag, PIT) alternatif olarak sunulan, **non-invaziv** bir fotoğraf tabanlı kimlik tespit sistemidir.

Sistem, bilinmeyen bir kaplumbağa görselini veritabanındaki kayıtlı bireylerle (1-to-N) karşılaştırarak en olası eşleşmeyi bulur.

---

## 🏗️ Mimari: Çok-Ajanlı Sistem

Her ajan tek bir sorumluluğa sahiptir ve `BaseAgent` abstract sınıfından miras alır. Orchestrator (`main.py`) ajanları sırayla koordine eder:

```
              📥 Kullanıcı Görseli
                      ↓
         ┌─────────────────────────┐
         │     🔍 AuditAgent       │  → Dosya kontrolü
         │                         │    (format, boyut, okunabilirlik)
         └─────────────────────────┘
                      ↓
         ┌─────────────────────────┐
         │  🎯 HeadDetectionAgent  │  → OpenCV contour
         │                         │    + Gemini Vision doğrulama
         └─────────────────────────┘
                      ↓
         ┌─────────────────────────┐
         │  ✂️  PreprocessingAgent │  → Center crop
         │                         │    + 224x224 normalize
         └─────────────────────────┘
                      ↓
         ┌─────────────────────────┐
         │   🧠 RecognitionAgent   │  → ResNet50
         │                         │    → 2048 boyutlu embedding
         └─────────────────────────┘
                      ↓
         ┌─────────────────────────┐
         │   📊 EvaluationAgent    │  → Cosine Similarity
         │                         │    → En yakın eşleşme
         └─────────────────────────┘
                      ↓
         ┌─────────────────────────┐
         │   📝 ReportingAgent     │  → Gemini ile
         │                         │    günlük rapor üretimi
         └─────────────────────────┘
                      ↓
                📋 Tespit Raporu
```

---

## 👥 Ajan Rolleri

| Ajan | Sorumluluk | LLM Kullanımı |
|------|-----------|----------------|
| 🔍 **AuditAgent** | Girdi dosyasının format, boyut, okunabilirlik ve çözünürlük kontrolü | ❌ Yok |
| 🎯 **HeadDetectionAgent** | Kaplumbağa kafasının tespiti ve kırpılması; kafa varlığının doğrulanması | ✅ Gemini 1.5 Flash (Vision) |
| ✂️ **PreprocessingAgent** | Görselin merkezden kırpılması, RGB'ye çevrilmesi, 224x224'e yeniden boyutlandırılması | ❌ Yok |
| 🧠 **RecognitionAgent** | ResNet50 ile 2048 boyutlu özellik vektörü (embedding) çıkarımı | ❌ Yok |
| 📊 **EvaluationAgent** | İki embedding arasındaki Cosine Similarity ile eşleşme kararı | ❌ Yok |
| 📝 **ReportingAgent** | Günlük sonuçları analiz edip `gelisim_raporu.md` dosyasına araştırmacı dilinde rapor yazar | ✅ Gemini 1.5 Flash (Text) |
| 📁 **DataCollectionAgent** | Belirtilen klasörden görsel dosya yollarını toplar | ❌ Yok |

---

## 🧱 SOLID Prensipleri

- **S — Single Responsibility Principle (Tek Sorumluluk)**
  Her ajan yalnızca tek bir iş yapar. Örneğin `PreprocessingAgent` yalnızca görüntü normalize eder; asla LLM çağırmaz veya dosya sistemini taramaz.

- **O — Open/Closed Principle (Açık/Kapalı)**
  `PreprocessingAgent.__init__(target_size=(224, 224))` gibi parametreler sayesinde farklı bir CNN modeline (örn. InceptionV3 → 299x299) geçmek için sınıfın içini **değiştirmek** gerekmez; yalnızca farklı parametreyle **genişletilir**.

- **L — Liskov Substitution Principle (Liskov İkamesi)**
  Tüm ajanlar `BaseAgent`'tan miras aldığı için Orchestrator'da bir ajanı başkasıyla değiştirmek pipeline'ı bozmaz (aynı `run()` ve `validate_input()` arayüzü).

- **I — Interface Segregation Principle (Arayüz Ayrımı)**
  `BaseAgent` yalnızca tüm ajanlar için gerekli olan minimal arayüzü tanımlar: `run()`, `validate_input()`, `log()`. Ajanlar kullanmadıkları metodlara zorlanmaz.

- **D — Dependency Inversion Principle (Bağımlılığın Tersine Çevrilmesi)**
  `Orchestrator` somut sınıflara değil, `BaseAgent` soyutlamasına bağımlıdır. Bu sayede ajanlar birbirine **gevşek bağlı** (loosely coupled) kalır; örneğin `RecognitionAgent` yarın VGG16'ya geçerse diğer ajanlar etkilenmez.

---

## ✨ Clean Code Kanıtı

- **Type Hint** — Fonksiyon imzalarında tüm parametre ve dönüş tipleri belirtilmiştir:
  ```python
  def compare_turtles(self, feature1: np.ndarray, feature2: np.ndarray) -> Tuple[bool, float]:
  ```

- **Docstring** — Her sınıf ve metod üçlü tırnak içinde amacını ve döndürdüğü değerleri açıklar:
  ```python
  """
  Kırpılmış görseli Gemini Vision'a göndererek
  kaplumbağa kafasının görünüp görünmediğini doğrular.
  """
  ```

- **BaseAgent Abstract Sınıfı** — `ABC` ve `@abstractmethod` ile tüm ajanlar için ortak bir sözleşme tanımlanmıştır (`agents/__init__.py`).

- **Sabitler UPPER_CASE** — Magic number kullanılmaz; sabitler sınıf seviyesinde anlamlı isimlerle tanımlanır:
  ```python
  MIN_HEAD_RATIO = 0.05
  LOW_CONFIDENCE_THRESHOLD = 0.4
  ```

- **Her Metod Maksimum 20 Satır** — Her metod tek bir işe odaklanır; uzun mantık `_private_helper()` metodlarına parçalanır.

- **`validate_input()` Her Ajanda** — Her ajan, `run()` çağrılmadan önce girdisinin geçerli olduğunu doğrular; hatalı girdi pipeline'a sızmaz.

---

## ⚙️ Kurulum

**1. Bağımlılıkları kur:**
```bash
pip install -r gereksinimler.txt
```

**2. Ortam değişkenlerini ayarla:** Proje kök dizinine `.env` dosyası oluştur ve içine Gemini API anahtarını ekle:
```env
GEMINI_API_KEY=senin_api_anahtarin_buraya
```

**3. Veri klasörlerini hazırla:**
- `data/database/` → Sisteme kayıtlı bireylerin görselleri (örn. `riza.jpeg`, `ayse.jpg`)
- `data/query/` → Kimliği tespit edilecek bilinmeyen görsel

**4. Sistemi çalıştır:**
```bash
python main.py
```

---

## 🔧 Teknik Detaylar

| Bileşen | Teknoloji |
|---------|-----------|
| 🧠 **Derin Öğrenme Modeli** | ResNet50 (ImageNet pretrained, `include_top=False`, `pooling='avg'`) |
| 📐 **Benzerlik Metriği** | Cosine Similarity (`scipy.spatial.distance.cosine`) |
| 🎯 **Eşleşme Eşiği** | %60 |
| 🔍 **Kafa Tespiti** | OpenCV Contour Analizi (Canny + findContours) + Gemini Vision doğrulaması |
| 📝 **Raporlama Modeli** | Gemini 1.5 Flash (Google Generative AI) |
| 🖼️ **Görsel İşleme** | OpenCV 4.x, Pillow |
| 📏 **Girdi Çözünürlüğü** | 224×224 piksel (RGB) |

---

## 🔬 Bilimsel Arka Plan

Bu sistem, **Chabrolle & Dumont-Dayot (2015)** tarafından önerilen **photo-ID** metodolojisine dayanır. Çalışmaya göre, deniz kaplumbağalarının göz çevresindeki **post-oküler scut** (pul) desenleri, bireyin yaşamı boyunca stabil kalır ve tıpkı insan parmak izi gibi bireye özgüdür.

Bu pulların **sayısı, geometrisi ve dizilim örüntüsü** genetik olarak belirlenir ve çevresel faktörlerden minimal düzeyde etkilenir. Bu sayede, kaplumbağaya fiziksel müdahale gerektiren flipper tag veya PIT gibi invaziv etiketleme yöntemlerine ihtiyaç duyulmadan, yalnızca yüksek çözünürlüklü yan profil fotoğrafı üzerinden güvenilir bireysel kimlik tespiti yapılabilir.

---

> 📅 *Bu proje Yazılım Mühendisliği dersi kapsamında, SOLID prensipleri ve Clean Code pratiklerini çok-ajanlı bir sistem üzerinden uygulamalı olarak göstermek amacıyla geliştirilmiştir.*
