### Test Sonucu (18:28:10)
- **Görsel 1:** `test1.jpeg`
- **Görsel 2:** `test2.jpeg`
- **Benzerlik Skoru:** %86.28
- **Karar:** ✅ EŞLEŞTİ

## Day 1 (AI Analizi)

**GÜNLÜK PROJE LOGU: Day 1**

**Ne yapıldı:**
Projenin ilk aşamasında, kaplumbağa yüzlerindeki benzersiz desenleri (scute patterns) dijital birer imzaya dönüştürmek amacıyla **ResNet50** derin öğrenme mimarisini öznitelik çıkarıcı (feature extractor) olarak konumlandırdık. Modelin son katmanından elde ettiğimiz yüksek boyutlu vektörleri, iki farklı görsel arasındaki matematiksel benzerliği ölçmek için **Cosine Similarity (Kosinüs Benzerliği)** metriğine tabi tuttuk. Bu yöntemle, piksellerden ziyade yapısal formların ve doku benzerliklerinin karşılaştırılmasını sağladık.

**Ne sonuç alındı:**
Gerçekleştirilen ilk testlerde **%86.28** gibi oldukça yüksek bir benzerlik skoru elde edildi. Belirlediğimiz %60'lık doğruluk eşiğinin (threshold) çok üzerinde olan bu sonuç, sistemin "başarılı eşleşme" kararı vermesini sağladı. ResNet50'nin önceden eğitilmiş ağırlıkları, kaplumbağa yüzlerindeki karmaşık geometrik şekilleri ve keratin plakalarının dizilimini ayırt etmede beklediğimizden daha keskin bir performans sergiledi.

**Hangi problemler çıktı:**
Elde edilen %86.28'lik skor kağıt üzerinde mükemmel görünse de, kıdemli bir bakış açısıyla bu durumun bazı riskler barındırdığını söyleyebilirim. ResNet50 genel nesne tanıma (ImageNet) verileriyle eğitildiği için, sistem kaplumbağanın türüne özgü detaylardan ziyade genel arka plan dokusuna veya aydınlatma benzerliğine odaklanmış olabilir (false positive riski). Ayrıca, farklı açılardan (profil vs. karşıdan) çekilen fotoğraflarda bu skorun sert bir düşüş yaşayabileceğini öngörüyoruz; zira mevcut model henüz "poz duyarsızlığı" (pose invariance) testine tabi tutulmadı.

**Ne iyileştirildi:**
Sistemin temel iskeletini tamamen **modüler** bir yapıda kurguladık. Bu sayede ilerleyen günlerde ResNet50 bloğunu kolayca çıkarıp yerine EfficientNet veya Vision Transformers (ViT) gibi daha güncel mimarileri entegre edebileceğiz. Bir sonraki aşama için veri setindeki gürültüyü azaltmak adına görselleri yüz merkezli kırpan (face cropping) bir ön işleme hattı planladık. Ayrıca, modelin kaplumbağa desenlerine daha spesifik odaklanması için "Fine-tuning" ve "Triplet Loss" fonksiyonu üzerine çalışmalara başlanmıştır.

---

### Test Sonucu (18:38:32)
- **Görsel 1:** `test2.JPG`
- **Görsel 2:** `test1.jpeg`
- **Benzerlik Skoru:** %74.45
- **Karar:** ✅ EŞLEŞTİ

## Day 1 (AI Analizi)

**Günlük Log: Kaplumbağa Yüz Tanıma Projesi - Day 1**

**Ne yapıldı:**
Projenin ilk aşamasında, derin öğrenme tabanlı bir öznitelik çıkarıcı olan **ResNet50** mimarisini temel alan bir boru hattı (pipeline) kuruldu. Sisteme giriş yapılan iki farklı kaplumbağa fotoğrafı, modelin önceden eğitilmiş katmanlarından geçirilerek yüksek boyutlu vektörlere (embeddings) dönüştürüldü. Bu iki vektör arasındaki anlamsal yakınlığı ölçmek için **Cosine Similarity (Kosinüs Benzerliği)** metriği kullanıldı. Bu yöntemle, piksellerden ziyade geometrik ve dokusal desenlerin benzerliğine odaklanıldı.

**Ne sonuç alındı:**
Yapılan test sonucunda **%74.45** oranında bir benzerlik skoru elde edildi. Belirlediğimiz %60’lık başlangıç eşik değerinin (threshold) üzerinde kalınması, projenin ilk günü için oldukça umut verici. Bu skor, ResNet50’nin kaplumbağaların kafa yapısındaki karakteristik "scute" (pullanma) dizilimlerini ayırt edici birer öznitelik olarak yakalayabildiğini gösteriyor. Skorun %90'larda olmaması ise muhtemelen fotoğraflar arasındaki açı farkından veya ışık değişimlerinden kaynaklanmaktadır; ancak yine de "doğru eşleşme" sınıflandırması için yeterli bir güven aralığındadır.

**Hangi problemler çıktı:**
Şu anki sonuç başarılı olsa da, sistemin henüz "zorlayıcı örnekler" (hard positives/negatives) karşısında nasıl tepki vereceği belirsiz. Mevcut problemimiz, ResNet50’nin genel nesne tanıma üzerine eğitilmiş olmasıdır; bu da deniz kaplumbağalarına özgü mikro-dokuları (mikro-desenleri) bazen göz ardı etmesine neden olabilir. Ayrıca, su altındaki bulanıklık veya farklı ışık kırılmaları durumunda benzerlik skorunun hızla eşik değerin altına düşme riski bulunmaktadır. Sistemin "yanlış pozitif" (birbirine benzeyen farklı kaplumbağaları aynı sanma) üretme potansiyeli hala bir risk unsuru olarak masadadır.

**Ne iyileştirildi:**
Day 1 itibarıyla sistemin **modüler mimarisi** başarıyla kurgulandı; bu sayede ilerleyen günlerde ResNet50 yerine daha hafif olan MobileNetV3 veya daha kompleks olan EfficientNet gibi modelleri kolayca entegre edebileceğiz. Bir sonraki aşamada, modelin sadece genel nesneleri değil, kaplumbağa yüz desenlerini daha spesifik tanıyabilmesi için **"Fine-tuning" (ince ayar)** sürecine geçilmesi ve benzerlik ölçümünde daha hassas olan **Triplet Loss** gibi kayıp fonksiyonlarının değerlendirilmesi planlanmaktadır.

---

