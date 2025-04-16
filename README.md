# Search Engine Evaluator

Bu proje, farklı arama motorlarının performansını karşılaştırmak ve değerlendirmek için tasarlanmış modüler bir kütüphanedir.

## Özellikler

- Çeşitli arama motorlarını (Google, Bing, vb.) karşılaştırma
- Arama motoru performansını değerlendirme (hız, sonuç kalitesi)
- Karşılaştırmalı raporlar oluşturma
- Kolay genişletilebilir modüler tasarım

## Kurulum

1. Depoyu klonlayın:

```bash
git clone https://github.com/yourusername/search-engine-evaluator.git
cd search-engine-evaluator
```

2. Gerekli bağımlılıkları kurun:

```bash
pip install -r requirements.txt
```

3. `.env` dosyasını oluşturun ve API anahtarlarınızı ekleyin:

```
GOOGLE_API_KEY=your_api_key
GOOGLE_CX=your_custom_search_id
```

## Kullanım

Basit kullanım örneği:

```python
from src.evaluator import SearchEngineEvaluator
from src.engines.google import GoogleSearch

# Değerlendiriciyi oluştur
evaluator = SearchEngineEvaluator()

# Bir arama motoru ekle
google_engine = GoogleSearch(api_key="your_api_key", cx="your_cx")
evaluator.register_engine(google_engine)

# Testi çalıştır
evaluator.run_test("python programming", num_results=5)

# Rapor oluştur
report_file = evaluator.generate_report()
print(f"Rapor oluşturuldu: {report_file}")
```

Daha fazla örnek için `examples/` dizinine bakın.

## Desteklenen Arama Motorları

- Google Search
- (Diğer arama motorları daha sonra eklenecek)

## Yeni Arama Motorları Ekleme

Yeni bir arama motoru eklemek için `src/engines/` dizinine yeni bir modül ekleyin ve `BaseAPISearch` sınıfından türetin:

```python
from src.engines.base import BaseAPISearch
from src.core import SearchResult

class YeniAramaMotoru(BaseAPISearch):
    def __init__(self, api_key=None):
        super().__init__(
            name="Yeni Arama Motoru",
            source_url="https://api.yeniarama.com",
            license_type="Ticari",
            api_key_env_name="YENI_API_KEY",
            api_key=api_key
        )
        
    def search(self, query, num_results=10):
        # Arama mantığını burada uygulayın
        # ...
        return results  # SearchResult nesnelerinin listesi
```

## Lisans

MIT License 