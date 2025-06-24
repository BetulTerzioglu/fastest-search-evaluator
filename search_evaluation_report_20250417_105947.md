# Arama Motoru Değerlendirme Raporu

## 1. Giriş
Bu rapor, farklı arama API'lerinin ve kütüphanelerinin karşılaştırmalı bir değerlendirmesini sunmaktadır. Test edilen arama motorları: Google Search, Bing Search, Firecrawl Search, Tavily Search, Jina AI Search, DuckDuckGo Search, Quick Search

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
- **Ortalama yanıt süresi:** 0.30 saniye
- **Ücretsiz sorgu limiti ve fiyatlandırma:** $7 / 1000 sorgu (ilk 1000 sorgu/ay ücretsiz)
- **Rate limit:** 3 çağrı/saniye, 1000 çağrı/ay (ücretsiz)
- **Sonuç kalitesi:** (1-5 arası puan ve kısa yorum) *Manuel değerlendirme gerekiyor*
- **JSON örnek çıktı:** Sonuç bulunamadı

- **Entegre ederken yaşanan zorluklar veya kolaylıklar:** *Manuel değerlendirme gerekiyor*

### Firecrawl Search
- **API/Kütüphane Adı:** Firecrawl Search
- **Kullanılan endpoint:** https://www.firecrawl.dev/app
- **Ortalama yanıt süresi:** 1.00 saniye
- **Ücretsiz sorgu limiti ve fiyatlandırma:** Ücretsiz: 500 kredi, Hobby: $16/ay, Standard: $83/ay
- **Rate limit:** Plan'a bağlı olarak değişen kısıtlamalar
- **Sonuç kalitesi:** (1-5 arası puan ve kısa yorum) *Manuel değerlendirme gerekiyor*
- **JSON örnek çıktı:**

```json
{
  "title": "Python For Beginners | Python.org",
  "link": "https://www.python.org/about/gettingstarted/",
  "snippet": ""
}
```

- **Entegre ederken yaşanan zorluklar veya kolaylıklar:** *Manuel değerlendirme gerekiyor*

### Tavily Search
- **API/Kütüphane Adı:** Tavily Search
- **Kullanılan endpoint:** https://app.tavily.com/home
- **Ortalama yanıt süresi:** 0.75 saniye
- **Ücretsiz sorgu limiti ve fiyatlandırma:** Ücretsiz: 1000 sorgu/ay, Growth: $29/ay, Pro: $99/ay
- **Rate limit:** Ücretsiz plan: 1000 sorgu/ay
- **Sonuç kalitesi:** (1-5 arası puan ve kısa yorum) *Manuel değerlendirme gerekiyor*
- **JSON örnek çıktı:** Sonuç bulunamadı

- **Entegre ederken yaşanan zorluklar veya kolaylıklar:** *Manuel değerlendirme gerekiyor*

### Jina AI Search
- **API/Kütüphane Adı:** Jina AI Search
- **Kullanılan endpoint:** https://jina.ai/reader/
- **Ortalama yanıt süresi:** 12.13 saniye
- **Ücretsiz sorgu limiti ve fiyatlandırma:** Ücretsiz: Yok, Başlangıç: $5/ay 1M token, Pro: $49/ay 10M token
- **Rate limit:** Ücretsiz: 0 RPM, Başlangıç: 40 RPM, Pro: 400 RPM
- **Sonuç kalitesi:** (1-5 arası puan ve kısa yorum) *Manuel değerlendirme gerekiyor*
- **JSON örnek çıktı:** Sonuç bulunamadı

- **Entegre ederken yaşanan zorluklar veya kolaylıklar:** *Manuel değerlendirme gerekiyor*

### DuckDuckGo Search
- **API/Kütüphane Adı:** DuckDuckGo Search
- **Kullanılan endpoint:** https://duckduckgo.com
- **Ortalama yanıt süresi:** 0.76 saniye
- **Ücretsiz sorgu limiti ve fiyatlandırma:** Ücretsiz
- **Rate limit:** Limitlenmemiş (ancak aşırı kullanım tespit edilirse IP kısıtlaması olabilir)
- **Sonuç kalitesi:** (1-5 arası puan ve kısa yorum) *Manuel değerlendirme gerekiyor*
- **JSON örnek çıktı:**

```json
{
  "title": "Welcome to Python.org",
  "link": "www.python.org",
  "snippet": "Python is a versatile and easy-to-learn programming language that lets you work quickly and integrate systems more effectively. Learn Python basics, download the latest version, access documentation, find jobs, events, success stories and more on the official website."
}
```

- **Entegre ederken yaşanan zorluklar veya kolaylıklar:** *Manuel değerlendirme gerekiyor*

### Quick Search
- **API/Kütüphane Adı:** Quick Search
- **Kullanılan endpoint:** https://api.duckduckgo.com
- **Ortalama yanıt süresi:** 0.36 saniye
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

## 4. Karşılaştırma Tablosu

| API               |   Hız (s) | Ücret                                                           | Limit                                                                        | Kalite (1-5)   | Kaynak Linki                                                  | Lisans Türü / Erişim Durumu   |
|:------------------|----------:|:----------------------------------------------------------------|:-----------------------------------------------------------------------------|:---------------|:--------------------------------------------------------------|:------------------------------|
| Google Search     |      0.2  | $5 / 1000 sorgu (ilk 100 sorgu/gün ücretsiz)                    | 100 sorgu/gün (ücretsiz), 10,000 sorgu/gün (ücretli)                         | N/A            | https://developers.google.com/custom-search                   | Kapalı, Ücretli               |
| Bing Search       |      0.3  | $7 / 1000 sorgu (ilk 1000 sorgu/ay ücretsiz)                    | 3 çağrı/saniye, 1000 çağrı/ay (ücretsiz)                                     | N/A            | https://www.microsoft.com/en-us/bing/apis/bing-web-search-api | Kapalı, Ücretli (Azure)       |
| Firecrawl Search  |      1    | Ücretsiz: 500 kredi, Hobby: $16/ay, Standard: $83/ay            | Plan'a bağlı olarak değişen kısıtlamalar                                     | N/A            | https://www.firecrawl.dev/app                                 | Kapalı, Ücretli               |
| Tavily Search     |      0.75 | Ücretsiz: 1000 sorgu/ay, Growth: $29/ay, Pro: $99/ay            | Ücretsiz plan: 1000 sorgu/ay                                                 | N/A            | https://app.tavily.com/home                                   | Kapalı, Ücretli (Freemium)    |
| Jina AI Search    |     12.13 | Ücretsiz: Yok, Başlangıç: $5/ay 1M token, Pro: $49/ay 10M token | Ücretsiz: 0 RPM, Başlangıç: 40 RPM, Pro: 400 RPM                             | N/A            | https://jina.ai/reader/                                       | Kapalı, Ücretli (Freemium)    |
| DuckDuckGo Search |      0.76 | Ücretsiz                                                        | Limitlenmemiş (ancak aşırı kullanım tespit edilirse IP kısıtlaması olabilir) | N/A            | https://duckduckgo.com                                        | Açık Kaynak, Ücretsiz         |
| Quick Search      |      0.36 | Ücretsiz                                                        | Limitlenmemiş (ancak aşırı kullanım tespit edilirse IP kısıtlaması olabilir) | N/A            | https://api.duckduckgo.com                                    | Açık Kaynak, Ücretsiz         |

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
from google_search import GoogleSearch

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
- API anahtarları güvenli bir şekilde saklanmalıdır (örn. çevresel değişkenler).
- Rate limit'lere dikkat edilmelidir, özellikle ücretli API'lerde.
- Tüm arama motorları aynı sonuç formatını döndürmesine rağmen, sonuçların kalitesi ve miktarı farklılık gösterebilir.
