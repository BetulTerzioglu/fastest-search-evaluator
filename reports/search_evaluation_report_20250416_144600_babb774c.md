# Arama Motoru Değerlendirme Raporu

## 1. Giriş
Bu rapor, farklı arama API'lerinin ve kütüphanelerinin karşılaştırmalı bir değerlendirmesini sunmaktadır. Test edilen arama motorları: Google Search, Bing Search, DuckDuckGo Search, Quick Search, Brave Search

## 2. Yöntem
- Her API aynı sorgu(lar) ile test edildi.
- Yanıt süreleri ölçüldü (her test için ortalama).
- JSON çıktılar işlenerek karşılaştırma yapıldı.
- Testler aynı ağ ortamında ve benzer saatlerde gerçekleştirildi.

## 3. Bireysel Değerlendirmeler
### Google Search
- **API/Kütüphane Adı:** Google Search
- **Kullanılan endpoint:** https://developers.google.com/custom-search
- **Ortalama yanıt süresi:** 0.20 saniye
- **Ücretsiz sorgu limiti ve fiyatlandırma:** $5 / 1000 sorgu (ilk 100 sorgu/gün ücretsiz)
- **Rate limit:** 100 sorgu/gün (ücretsiz), 10,000 sorgu/gün (ücretli)
- **Sonuç kalitesi:** (1-5 arası puan ve kısa yorum) *Manuel değerlendirme gerekiyor*
- **JSON örnek çıktı:** Sonuç bulunamadı

- **Entegre ederken yaşanan zorluklar veya kolaylıklar:** *Manuel değerlendirme gerekiyor*

### Bing Search
- **API/Kütüphane Adı:** Bing Search
- **Kullanılan endpoint:** https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
- **Ortalama yanıt süresi:** 0.37 saniye
- **Ücretsiz sorgu limiti ve fiyatlandırma:** $7 / 1000 sorgu (ilk 1000 sorgu/ay ücretsiz)
- **Rate limit:** 3 çağrı/saniye, 1000 çağrı/ay (ücretsiz)
- **Sonuç kalitesi:** (1-5 arası puan ve kısa yorum) *Manuel değerlendirme gerekiyor*
- **JSON örnek çıktı:** Sonuç bulunamadı

- **Entegre ederken yaşanan zorluklar veya kolaylıklar:** *Manuel değerlendirme gerekiyor*

### DuckDuckGo Search
- **API/Kütüphane Adı:** DuckDuckGo Search
- **Kullanılan endpoint:** https://duckduckgo.com
- **Ortalama yanıt süresi:** 0.36 saniye
- **Ücretsiz sorgu limiti ve fiyatlandırma:** Ücretsiz
- **Rate limit:** Limitlenmemiş (ancak aşırı kullanım tespit edilirse IP kısıtlaması olabilir)
- **Sonuç kalitesi:** (1-5 arası puan ve kısa yorum) *Manuel değerlendirme gerekiyor*
- **JSON örnek çıktı:** Sonuç bulunamadı

- **Entegre ederken yaşanan zorluklar veya kolaylıklar:** *Manuel değerlendirme gerekiyor*

### Quick Search
- **API/Kütüphane Adı:** Quick Search
- **Kullanılan endpoint:** https://api.duckduckgo.com
- **Ortalama yanıt süresi:** 0.28 saniye
- **Ücretsiz sorgu limiti ve fiyatlandırma:** Ücretsiz
- **Rate limit:** Limitlenmemiş (ancak aşırı kullanım tespit edilirse IP kısıtlaması olabilir)
- **Sonuç kalitesi:** (1-5 arası puan ve kısa yorum) *Manuel değerlendirme gerekiyor*
- **JSON örnek çıktı:**

```json
{
  "title": "Python (programming language)",
  "link": "https://en.wikipedia.org/wiki/Python_(programming_language)",
  "snippet": "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically type-checked and garbage-collected. It supports multiple programming paradigms, including structured, object-oriented and functional programming. It is often described as a \"batteries included\" language due to its comprehensive standard library. Guido van Rossum began working on Python in the late 1980s as a successor to the ABC programming language and first released it in 1991 as Python 0.9.0. Python 2.0 was released in 2000. Python 3.0, released in 2008, was a major revision not completely backward-compatible with earlier versions. Python 2.7.18, released in 2020, was the last release of Python 2. Python consistently ranks as one of the most popular programming languages, and has gained widespread use in the machine learning community."
}
```

- **Entegre ederken yaşanan zorluklar veya kolaylıklar:** *Manuel değerlendirme gerekiyor*

### Brave Search
- **API/Kütüphane Adı:** Brave Search
- **Kullanılan endpoint:** https://search.brave.com/
- **Ortalama yanıt süresi:** 0.75 saniye
- **Ücretsiz sorgu limiti ve fiyatlandırma:** Ücretsiz: 2,000 sorgu/ay, Pro: $10/ay, Enterprise: Contact
- **Rate limit:** Ücretsiz: 2,000 sorgu/ay, Pro: 100,000 sorgu/ay
- **Sonuç kalitesi:** (1-5 arası puan ve kısa yorum) *Manuel değerlendirme gerekiyor*
- **JSON örnek çıktı:**

```json
{
  "title": "Python For Beginners | Python.org",
  "link": "https://www.python.org/about/gettingstarted/",
  "snippet": "The official home of the <strong>Python</strong> <strong>Programming</strong> Language"
}
```

- **Entegre ederken yaşanan zorluklar veya kolaylıklar:** *Manuel değerlendirme gerekiyor*

## 4. Karşılaştırma Tablosu

| API               |   Hız (s) | Ücret                                                      | Limit                                                                        | Kalite (1-5)   | Kaynak Linki                                                  | Lisans Türü / Erişim Durumu   |
|:------------------|----------:|:-----------------------------------------------------------|:-----------------------------------------------------------------------------|:---------------|:--------------------------------------------------------------|:------------------------------|
| Google Search     |      0.2  | $5 / 1000 sorgu (ilk 100 sorgu/gün ücretsiz)               | 100 sorgu/gün (ücretsiz), 10,000 sorgu/gün (ücretli)                         | N/A            | https://developers.google.com/custom-search                   | Kapalı, Ücretli               |
| Bing Search       |      0.37 | $7 / 1000 sorgu (ilk 1000 sorgu/ay ücretsiz)               | 3 çağrı/saniye, 1000 çağrı/ay (ücretsiz)                                     | N/A            | https://www.microsoft.com/en-us/bing/apis/bing-web-search-api | Kapalı, Ücretli (Azure)       |
| DuckDuckGo Search |      0.36 | Ücretsiz                                                   | Limitlenmemiş (ancak aşırı kullanım tespit edilirse IP kısıtlaması olabilir) | N/A            | https://duckduckgo.com                                        | Açık Kaynak, Ücretsiz         |
| Quick Search      |      0.28 | Ücretsiz                                                   | Limitlenmemiş (ancak aşırı kullanım tespit edilirse IP kısıtlaması olabilir) | N/A            | https://api.duckduckgo.com                                    | Açık Kaynak, Ücretsiz         |
| Brave Search      |      0.75 | Ücretsiz: 2,000 sorgu/ay, Pro: $10/ay, Enterprise: Contact | Ücretsiz: 2,000 sorgu/ay, Pro: 100,000 sorgu/ay                              | N/A            | https://search.brave.com/                                     | Kapalı, Ücretli (Freemium)    |

## 5. Öneriler
*Manuel değerlendirme gerekiyor. Aşağıdaki kullanım senaryolarına göre değerlendirilebilir:*

- **Demo amaçlı:** 
- **Yüksek hacimli kullanım:** 
- **Ticari kullanım:** 

## 6. Uygulama Notları
### Kod snippetları
*Belirli arama motorları için örnek kullanım kodları:*

```python
# Google arama örneği
from src.engines.google import GoogleSearch

google = GoogleSearch(api_key='API_KEY', cx='CUSTOM_SEARCH_ID')
results = google.search('python programming', num_results=5)
for result in results:
    print(f'Başlık: {result.title}')
    print(f'Link: {result.link}')
    print(f'Snippet: {result.snippet}')
    print('---')
```

### Ortak interface oluşturulması
Tüm arama motorları `SearchEngine` abstract sınıfını implement etmekte ve ortak bir arayüz sağlamaktadır. Bu sayede farklı arama motorları aynı şekilde kullanılabilir.

### Dikkat edilmesi gerekenler
- API anahtarları güvenli bir şekilde saklanmalıdır (örn. .env dosyası).
- Rate limit'lere dikkat edilmelidir, özellikle ücretli API'lerde.
- Tüm arama motorları aynı sonuç formatını döndürmesine rağmen, sonuçların kalitesi ve miktarı farklılık gösterebilir.
